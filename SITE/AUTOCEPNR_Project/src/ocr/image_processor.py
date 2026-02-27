<<<<<<< HEAD:AUTOCEPNR_Project/src/ocr/image_processor.py
"""
ImageProcessor Module
Handles image input from clipboard and file uploads for Sabre screen processing
"""

import os
import cv2
import numpy as np
from PIL import Image
import pyperclip

# pyautogui requires an X display; import lazily to avoid headless errors
try:
    import pyautogui
except Exception:
    pyautogui = None
from typing import Optional, Tuple, Union, List
import logging
from pathlib import Path

from .sabre_ocr import SabreOCR
from ..core.rules_engine import RulesEngine


class ImageProcessor:
    """Processor for handling image input and preprocessing"""
    
    def __init__(self, rules_engine: RulesEngine):
        """
        Initialize ImageProcessor with rules engine
        
        Args:
            rules_engine: RulesEngine instance for validation
        """
        self.rules_engine = rules_engine
        self.sabre_ocr = SabreOCR(rules_engine)
        self.logger = logging.getLogger(__name__)
        
        # Supported image formats
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        
    def load_from_clipboard(self) -> Optional[np.ndarray]:
        """
        Load image from clipboard (CTRL+V)
        
        Returns:
            Image as numpy array if successful, None otherwise
        """
        try:
            # Try to get image from clipboard
            clipboard_data = pyperclip.paste()
            
            if isinstance(clipboard_data, Image.Image):
                # PIL Image directly from clipboard
                return np.array(clipboard_data)
            
            elif isinstance(clipboard_data, str) and clipboard_data.startswith('http'):
                # URL in clipboard - not supported for now
                self.logger.warning("Clipboard contains URL, not image")
                return None
            
            else:
                # Try to get screenshot as fallback (only if pyautogui available)
                self.logger.info("No image in clipboard")
                if pyautogui is not None:
                    self.logger.info("taking screenshot")
                    screenshot = pyautogui.screenshot()
                    return np.array(screenshot)
                else:
                    self.logger.info("pyautogui unavailable; cannot take screenshot")
                    return None
                
        except Exception as e:
            self.logger.error(f"Error loading from clipboard: {e}")
            return None
    
    def load_from_file(self, file_path: Union[str, Path]) -> Optional[np.ndarray]:
        """
        Load image from file
        
        Args:
            file_path: Path to image file
            
        Returns:
            Image as numpy array if successful, None otherwise
        """
        try:
            file_path = Path(file_path)
            
            # Validate file exists and has supported format
            if not file_path.exists():
                self.logger.error(f"File not found: {file_path}")
                return None
            
            if file_path.suffix.lower() not in self.supported_formats:
                self.logger.error(f"Unsupported file format: {file_path.suffix}")
                return None
            
            # Load image using OpenCV
            image = cv2.imread(str(file_path))
            
            if image is None:
                self.logger.error(f"Could not load image from: {file_path}")
                return None
            
            # Convert BGR to RGB (OpenCV loads as BGR)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            self.logger.info(f"Successfully loaded image from: {file_path}")
            return image_rgb
            
        except Exception as e:
            self.logger.error(f"Error loading from file {file_path}: {e}")
            return None
    
    def validate_image_quality(self, image: np.ndarray) -> Tuple[bool, str]:
        """
        Validate image quality for OCR processing
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Tuple of (is_valid, quality_message)
        """
        try:
            # Check image dimensions
            height, width = image.shape[:2]
            
            if width < 800 or height < 600:
                return False, "Image resolution too low (minimum 800x600)"
            
            # Check if image is too dark or too bright
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) == 3 else image
            mean_brightness = np.mean(gray)
            
            if mean_brightness < 30:
                return False, "Image too dark for OCR processing"
            elif mean_brightness > 220:
                return False, "Image too bright for OCR processing"
            
            # Check for excessive noise (simple variance check)
            variance = np.var(gray)
            if variance < 100:
                return False, "Image appears to be blank or uniform color"
            
            return True, "Image quality acceptable for OCR"
            
        except Exception as e:
            self.logger.error(f"Error validating image quality: {e}")
            return False, f"Error validating image: {e}"
    
    def preprocess_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image specifically for Sabre OCR
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Preprocessed image
        """
        try:
            # Convert to RGB if needed
            if len(image.shape) == 2:
                # Grayscale to RGB
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif image.shape[2] == 4:
                # RGBA to RGB
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
            
            # Resize if too large (for performance)
            height, width = image.shape[:2]
            max_dimension = 1920
            
            if max(width, height) > max_dimension:
                scale = max_dimension / max(width, height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            # Apply Sabre-specific preprocessing
            return self.sabre_ocr.preprocess_image(image)
            
        except Exception as e:
            self.logger.error(f"Error in OCR preprocessing: {e}")
            return image
    
    def extract_text_from_image(self, image: np.ndarray) -> str:
        """
        Extract text from preprocessed image using SabreOCR
        
        Args:
            image: Preprocessed image as numpy array
            
        Returns:
            Extracted text as string
        """
        try:
            # Validate image quality first
            is_valid, message = self.validate_image_quality(image)
            if not is_valid:
                self.logger.warning(f"Image quality issue: {message}")
                # Continue anyway, but log the issue
            
            # Preprocess for OCR
            processed_image = self.preprocess_for_ocr(image)
            
            # Extract text using SabreOCR
            extracted_text = self.sabre_ocr.extract_text(processed_image)
            
            # Validate Sabre format
            if extracted_text and self.sabre_ocr.validate_sabre_format(extracted_text):
                self.logger.info("Successfully extracted text from Sabre screen")
            elif extracted_text:
                self.logger.warning("Extracted text but format validation failed")
            
            return extracted_text
            
        except Exception as e:
            self.logger.error(f"Error extracting text from image: {e}")
            return ""
    
    def get_image_info(self, image: np.ndarray) -> dict:
        """
        Get information about the image
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Dictionary with image information
        """
        try:
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1
            
            # Calculate basic statistics
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            mean_brightness = float(np.mean(gray))
            std_brightness = float(np.std(gray))
            
            return {
                'width': width,
                'height': height,
                'channels': channels,
                'mean_brightness': mean_brightness,
                'std_brightness': std_brightness,
                'size_mb': (width * height * channels) / (1024 * 1024),
                'format_valid': width > 0 and height > 0
            }
            
        except Exception as e:
            self.logger.error(f"Error getting image info: {e}")
            return {}
    
    def save_debug_image(self, image: np.ndarray, filename: str) -> bool:
        """
        Save debug image for troubleshooting
        
        Args:
            image: Image to save
            filename: Output filename
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            debug_dir = Path("debug_images")
            debug_dir.mkdir(exist_ok=True)
            
            output_path = debug_dir / filename
            
            # Convert RGB to BGR for OpenCV saving
            if len(image.shape) == 3:
                bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            else:
                bgr_image = image
            
            cv2.imwrite(str(output_path), bgr_image)
            self.logger.info(f"Debug image saved to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving debug image: {e}")
            return False
    
    def process_image_input(self, input_source: Union[str, np.ndarray, None] = None) -> Tuple[Optional[np.ndarray], str]:
        """
        Main method to process image input from various sources
        
        Args:
            input_source: Can be:
                         - None: Try clipboard first, then screenshot
                         - String: File path or "clipboard"
                         - numpy array: Direct image array
            
        Returns:
            Tuple of (processed_image, extracted_text)
        """
        try:
            image = None
            extracted_text = ""
            
            # Determine input source
            if input_source is None:
                # Try clipboard first, then screenshot
                image = self.load_from_clipboard()
                if image is None:
                    self.logger.info("No image in clipboard, taking screenshot")
                    image = np.array(pyautogui.screenshot())
            
            elif isinstance(input_source, str):
                if input_source.lower() == "clipboard":
                    image = self.load_from_clipboard()
                else:
                    # Assume it's a file path
                    image = self.load_from_file(input_source)
            
            elif isinstance(input_source, np.ndarray):
                # Direct image array
                image = input_source.copy()
            
            else:
                self.logger.error(f"Unsupported input source type: {type(input_source)}")
                return None, ""
            
            if image is None:
                self.logger.error("Could not load image from any source")
                return None, ""
            
            # Get image info for logging
            image_info = self.get_image_info(image)
            self.logger.info(f"Loaded image: {image_info}")
            
            # Validate image quality
            is_valid, quality_msg = self.validate_image_quality(image)
            if not is_valid:
                self.logger.warning(f"Image quality issue: {quality_msg}")
            
            # Extract text
            extracted_text = self.extract_text_from_image(image)
            
            # Save debug images if needed
            if extracted_text:
                self.save_debug_image(image, "original_input.png")
                processed = self.preprocess_for_ocr(image)
                self.save_debug_image(processed, "processed_for_ocr.png")
            
            return image, extracted_text
            
        except Exception as e:
            self.logger.error(f"Error processing image input: {e}")
=======
"""
ImageProcessor Module
Handles image input from clipboard and file uploads for Sabre screen processing
"""

import os
import cv2
import numpy as np
from PIL import Image
import pyperclip
import pyautogui
from typing import Optional, Tuple, Union, List
import logging
from pathlib import Path

from .sabre_ocr import SabreOCR
from ..core.rules_engine import RulesEngine


class ImageProcessor:
    """Processor for handling image input and preprocessing"""
    
    def __init__(self, rules_engine: RulesEngine):
        """
        Initialize ImageProcessor with rules engine
        
        Args:
            rules_engine: RulesEngine instance for validation
        """
        self.rules_engine = rules_engine
        self.sabre_ocr = SabreOCR(rules_engine)
        self.logger = logging.getLogger(__name__)
        
        # Supported image formats
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        
    def load_from_clipboard(self) -> Optional[np.ndarray]:
        """
        Load image from clipboard (CTRL+V)
        
        Returns:
            Image as numpy array if successful, None otherwise
        """
        try:
            # Try to get image from clipboard
            clipboard_data = pyperclip.paste()
            
            if isinstance(clipboard_data, Image.Image):
                # PIL Image directly from clipboard
                return np.array(clipboard_data)
            
            elif isinstance(clipboard_data, str) and clipboard_data.startswith('http'):
                # URL in clipboard - not supported for now
                self.logger.warning("Clipboard contains URL, not image")
                return None
            
            else:
                # Try to get screenshot as fallback
                self.logger.info("No image in clipboard, taking screenshot")
                screenshot = pyautogui.screenshot()
                return np.array(screenshot)
                
        except Exception as e:
            self.logger.error(f"Error loading from clipboard: {e}")
            return None
    
    def load_from_file(self, file_path: Union[str, Path]) -> Optional[np.ndarray]:
        """
        Load image from file
        
        Args:
            file_path: Path to image file
            
        Returns:
            Image as numpy array if successful, None otherwise
        """
        try:
            file_path = Path(file_path)
            
            # Validate file exists and has supported format
            if not file_path.exists():
                self.logger.error(f"File not found: {file_path}")
                return None
            
            if file_path.suffix.lower() not in self.supported_formats:
                self.logger.error(f"Unsupported file format: {file_path.suffix}")
                return None
            
            # Load image using OpenCV
            image = cv2.imread(str(file_path))
            
            if image is None:
                self.logger.error(f"Could not load image from: {file_path}")
                return None
            
            # Convert BGR to RGB (OpenCV loads as BGR)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            self.logger.info(f"Successfully loaded image from: {file_path}")
            return image_rgb
            
        except Exception as e:
            self.logger.error(f"Error loading from file {file_path}: {e}")
            return None
    
    def validate_image_quality(self, image: np.ndarray) -> Tuple[bool, str]:
        """
        Validate image quality for OCR processing
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Tuple of (is_valid, quality_message)
        """
        try:
            # Check image dimensions
            height, width = image.shape[:2]
            
            if width < 800 or height < 600:
                return False, "Image resolution too low (minimum 800x600)"
            
            # Check if image is too dark or too bright
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) == 3 else image
            mean_brightness = np.mean(gray)
            
            if mean_brightness < 30:
                return False, "Image too dark for OCR processing"
            elif mean_brightness > 220:
                return False, "Image too bright for OCR processing"
            
            # Check for excessive noise (simple variance check)
            variance = np.var(gray)
            if variance < 100:
                return False, "Image appears to be blank or uniform color"
            
            return True, "Image quality acceptable for OCR"
            
        except Exception as e:
            self.logger.error(f"Error validating image quality: {e}")
            return False, f"Error validating image: {e}"
    
    def preprocess_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image specifically for Sabre OCR
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Preprocessed image
        """
        try:
            # Convert to RGB if needed
            if len(image.shape) == 2:
                # Grayscale to RGB
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif image.shape[2] == 4:
                # RGBA to RGB
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
            
            # Resize if too large (for performance)
            height, width = image.shape[:2]
            max_dimension = 1920
            
            if max(width, height) > max_dimension:
                scale = max_dimension / max(width, height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            # Apply Sabre-specific preprocessing
            return self.sabre_ocr.preprocess_image(image)
            
        except Exception as e:
            self.logger.error(f"Error in OCR preprocessing: {e}")
            return image
    
    def extract_text_from_image(self, image: np.ndarray) -> str:
        """
        Extract text from preprocessed image using SabreOCR
        
        Args:
            image: Preprocessed image as numpy array
            
        Returns:
            Extracted text as string
        """
        try:
            # Validate image quality first
            is_valid, message = self.validate_image_quality(image)
            if not is_valid:
                self.logger.warning(f"Image quality issue: {message}")
                # Continue anyway, but log the issue
            
            # Preprocess for OCR
            processed_image = self.preprocess_for_ocr(image)
            
            # Extract text using SabreOCR
            extracted_text = self.sabre_ocr.extract_text(processed_image)
            
            # Validate Sabre format
            if extracted_text and self.sabre_ocr.validate_sabre_format(extracted_text):
                self.logger.info("Successfully extracted text from Sabre screen")
            elif extracted_text:
                self.logger.warning("Extracted text but format validation failed")
            
            return extracted_text
            
        except Exception as e:
            self.logger.error(f"Error extracting text from image: {e}")
            return ""
    
    def get_image_info(self, image: np.ndarray) -> dict:
        """
        Get information about the image
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Dictionary with image information
        """
        try:
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1
            
            # Calculate basic statistics
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            mean_brightness = float(np.mean(gray))
            std_brightness = float(np.std(gray))
            
            return {
                'width': width,
                'height': height,
                'channels': channels,
                'mean_brightness': mean_brightness,
                'std_brightness': std_brightness,
                'size_mb': (width * height * channels) / (1024 * 1024),
                'format_valid': width > 0 and height > 0
            }
            
        except Exception as e:
            self.logger.error(f"Error getting image info: {e}")
            return {}
    
    def save_debug_image(self, image: np.ndarray, filename: str) -> bool:
        """
        Save debug image for troubleshooting
        
        Args:
            image: Image to save
            filename: Output filename
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            debug_dir = Path("debug_images")
            debug_dir.mkdir(exist_ok=True)
            
            output_path = debug_dir / filename
            
            # Convert RGB to BGR for OpenCV saving
            if len(image.shape) == 3:
                bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            else:
                bgr_image = image
            
            cv2.imwrite(str(output_path), bgr_image)
            self.logger.info(f"Debug image saved to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving debug image: {e}")
            return False
    
    def process_image_input(self, input_source: Union[str, np.ndarray, None] = None) -> Tuple[Optional[np.ndarray], str]:
        """
        Main method to process image input from various sources
        
        Args:
            input_source: Can be:
                         - None: Try clipboard first, then screenshot
                         - String: File path or "clipboard"
                         - numpy array: Direct image array
            
        Returns:
            Tuple of (processed_image, extracted_text)
        """
        try:
            image = None
            extracted_text = ""
            
            # Determine input source
            if input_source is None:
                # Try clipboard first, then screenshot
                image = self.load_from_clipboard()
                if image is None:
                    self.logger.info("No image in clipboard, taking screenshot")
                    image = np.array(pyautogui.screenshot())
            
            elif isinstance(input_source, str):
                if input_source.lower() == "clipboard":
                    image = self.load_from_clipboard()
                else:
                    # Assume it's a file path
                    image = self.load_from_file(input_source)
            
            elif isinstance(input_source, np.ndarray):
                # Direct image array
                image = input_source.copy()
            
            else:
                self.logger.error(f"Unsupported input source type: {type(input_source)}")
                return None, ""
            
            if image is None:
                self.logger.error("Could not load image from any source")
                return None, ""
            
            # Get image info for logging
            image_info = self.get_image_info(image)
            self.logger.info(f"Loaded image: {image_info}")
            
            # Validate image quality
            is_valid, quality_msg = self.validate_image_quality(image)
            if not is_valid:
                self.logger.warning(f"Image quality issue: {quality_msg}")
            
            # Extract text
            extracted_text = self.extract_text_from_image(image)
            
            # Save debug images if needed
            if extracted_text:
                self.save_debug_image(image, "original_input.png")
                processed = self.preprocess_for_ocr(image)
                self.save_debug_image(processed, "processed_for_ocr.png")
            
            return image, extracted_text
            
        except Exception as e:
            self.logger.error(f"Error processing image input: {e}")
>>>>>>> 7a10112 (FirstlProjectSDDMetodologia):SITE/AUTOCEPNR_Project/src/ocr/image_processor.py
            return None, ""