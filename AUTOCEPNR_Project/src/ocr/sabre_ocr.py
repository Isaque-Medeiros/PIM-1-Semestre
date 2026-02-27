"""
SabreOCR Module
Handles EasyOCR integration for Sabre Interact v2.1 font detection and text extraction
"""

import cv2
import numpy as np
from PIL import Image
import easyocr
from typing import Dict, List, Tuple, Optional, Any
import re
import logging

from ..core.rules_engine import RulesEngine


class SabreOCR:
    """OCR processor optimized for Sabre Interact v2.1 monospace fonts"""
    
    def __init__(self, rules_engine: RulesEngine):
        """
        Initialize SabreOCR with rules engine
        
        Args:
            rules_engine: RulesEngine instance for validation
        """
        self.rules_engine = rules_engine
        self.reader = None
        self.is_initialized = False
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def initialize(self) -> bool:
        """
        Initialize EasyOCR reader with Sabre-optimized settings
        
        Returns:
            True if initialized successfully, False otherwise
        """
        try:
            # Initialize EasyOCR with English and Portuguese
            # Sabre uses monospace fonts, so we optimize for that
            self.reader = easyocr.Reader(
                ['en', 'pt'],  # English and Portuguese
                gpu=False,     # Use CPU for Windows standalone
                model_storage_directory='models',
                user_network_directory='user_networks'
            )
            self.is_initialized = True
            self.logger.info("EasyOCR initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error initializing EasyOCR: {e}")
            return False
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR results with Sabre fonts
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Preprocessed image
        """
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            # Enhance contrast for monospace fonts
            # Sabre fonts are typically high contrast, so we optimize for that
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            
            # Noise reduction
            denoised = cv2.medianBlur(enhanced, 3)
            
            # Sharpening for monospace fonts
            kernel = np.array([[-1, -1, -1],
                              [-1,  9, -1],
                              [-1, -1, -1]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            
            # Binarization for better text detection
            _, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return binary
            
        except Exception as e:
            self.logger.error(f"Error in image preprocessing: {e}")
            return image
    
    def extract_text(self, image: np.ndarray) -> str:
        """
        Extract text from Sabre screen image
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Extracted text as string
        """
        if not self.is_initialized:
            if not self.initialize():
                return ""
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Use EasyOCR to extract text
            # Sabre Interact v2.1 has specific layout, so we can optimize detection
            results = self.reader.readtext(
                processed_image,
                detail=0,           # Return only text
                paragraph=True,     # Group text into paragraphs
                min_size=10,        # Minimum text size
                text_threshold=0.7, # Confidence threshold
                low_text=0.4,       # Text detection threshold
                link_threshold=0.4, # Link threshold
                canvas_size=2560,   # Maximum canvas size
                mag_ratio=1.5       # Magnification ratio
            )
            
            # Join results and clean up
            extracted_text = " ".join(results) if results else ""
            
            # Clean up common Sabre OCR issues
            extracted_text = self._clean_sabre_text(extracted_text)
            
            self.logger.info(f"Extracted text: {extracted_text[:100]}...")
            return extracted_text
            
        except Exception as e:
            self.logger.error(f"Error in text extraction: {e}")
            return ""
    
    def _clean_sabre_text(self, text: str) -> str:
        """
        Clean up OCR text specific to Sabre Interact patterns
        
        Args:
            text: Raw OCR text
            
        Returns:
            Cleaned text
        """
        try:
            # Remove excessive whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Fix common Sabre font OCR issues
            # Sabre uses monospace fonts that can be misread
            replacements = {
                '0': 'O',  # Zero to O
                '1': 'I',  # One to I
                '5': 'S',  # Five to S
                '8': 'B',  # Eight to B
            }
            
            # Be conservative with replacements - only fix obvious cases
            for wrong, correct in replacements.items():
                # Only replace if it makes sense in context
                text = re.sub(r'\b' + wrong + r'\b', correct, text)
            
            # Fix common Sabre field patterns
            # Reservation pattern
            text = re.sub(r'Reserva\s*-\s*([A-Z0-9]{6})', r'Reserva - \1', text)
            
            # Flight number pattern
            text = re.sub(r'([A-Z]{2})\s*(\d{3,4})', r'\1 \2', text)
            
            # Date pattern
            text = re.sub(r'(\d{2})([A-Z]{3})', r'\1\2', text)
            
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"Error cleaning text: {e}")
            return text
    
    def detect_sabre_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect regions of interest in Sabre screen for targeted OCR
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of bounding boxes (x, y, w, h)
        """
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            # Find text regions using contour detection
            # Sabre has structured layout with clear text blocks
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            regions = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter by size and aspect ratio (Sabre text blocks)
                if w > 50 and h > 20 and w/h < 20:  # Reasonable text block size
                    regions.append((x, y, w, h))
            
            # Sort regions by y-coordinate (top to bottom)
            regions.sort(key=lambda r: r[1])
            
            return regions
            
        except Exception as e:
            self.logger.error(f"Error detecting Sabre regions: {e}")
            return []
    
    def extract_field_from_region(self, image: np.ndarray, region: Tuple[int, int, int, int]) -> str:
        """
        Extract text from a specific region of the image
        
        Args:
            image: Input image as numpy array
            region: Bounding box (x, y, w, h)
            
        Returns:
            Extracted text from region
        """
        try:
            x, y, w, h = region
            region_image = image[y:y+h, x:x+w]
            
            # Extract text from region
            processed_region = self.preprocess_image(region_image)
            results = self.reader.readtext(
                processed_region,
                detail=0,
                paragraph=False,
                min_size=5
            )
            
            return " ".join(results) if results else ""
            
        except Exception as e:
            self.logger.error(f"Error extracting field from region: {e}")
            return ""
    
    def validate_sabre_format(self, extracted_text: str) -> bool:
        """
        Validate if extracted text matches Sabre Interact v2.1 format
        
        Args:
            extracted_text: Text extracted from image
            
        Returns:
            True if format is valid Sabre format, False otherwise
        """
        try:
            # Check for characteristic Sabre patterns
            sabre_patterns = [
                r'Reserva\s*-\s*[A-Z0-9]{6}',  # Reservation pattern
                r'Nomes',                      # Passenger names
                r'Voo\s*\(CIA\)',             # Flight carrier
                r'Voo\s*\(Numero\)',          # Flight number
                r'Cls',                       # Class
                r'De-Para',                   # Route
                r'Data',                      # Date
                r'Stp\s*Nbr',                 # Status
            ]
            
            found_patterns = 0
            for pattern in sabre_patterns:
                if re.search(pattern, extracted_text, re.IGNORECASE):
                    found_patterns += 1
            
            # Consider it valid Sabre format if we find at least 5 patterns
            return found_patterns >= 5
            
        except Exception as e:
            self.logger.error(f"Error validating Sabre format: {e}")
            return False
    
    def get_confidence_map(self, image: np.ndarray) -> Dict[str, float]:
        """
        Get confidence scores for different text regions
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Dictionary mapping field names to confidence scores
        """
        if not self.is_initialized:
            return {}
        
        try:
            # Get detailed OCR results with confidence
            processed_image = self.preprocess_image(image)
            results = self.reader.readtext(
                processed_image,
                detail=1,  # Return detailed results
                paragraph=False
            )
            
            confidence_map = {}
            
            # Analyze confidence for key Sabre fields
            for result in results:
                text = result[1]
                confidence = result[2]
                
                # Map text to field names based on content
                if re.match(r'Reserva\s*-\s*[A-Z0-9]{6}', text, re.IGNORECASE):
                    confidence_map['pnr'] = confidence
                elif 'Nomes' in text:
                    confidence_map['passenger_name'] = confidence
                elif re.match(r'[A-Z]{2}\s+\d{3,4}', text):
                    confidence_map['flight_info'] = confidence
                elif re.match(r'\d{2}[A-Z]{3}', text):
                    confidence_map['date'] = confidence
            
            return confidence_map
            
        except Exception as e:
            self.logger.error(f"Error getting confidence map: {e}")
            return {}