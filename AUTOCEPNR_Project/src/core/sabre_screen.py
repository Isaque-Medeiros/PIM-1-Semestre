"""
SabreScreen Object
Handles image capture, OCR processing, and field extraction from Sabre Interact v2.1
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import cv2
import numpy as np
from PIL import Image
import pyperclip
import pyautogui

from .rules_engine import RulesEngine, ValidationResult


@dataclass
class SabreField:
    """Represents a field extracted from Sabre screen"""
    name: str
    value: str
    confidence: float
    position: Tuple[int, int, int, int]  # x, y, width, height


class SabreScreen:
    """Object representing a Sabre Interact screen capture and its extracted data"""
    
    def __init__(self, rules_engine: RulesEngine):
        """
        Initialize SabreScreen with rules engine
        
        Args:
            rules_engine: RulesEngine instance for validation
        """
        self.rules_engine = rules_engine
        self.raw_image: Optional[np.ndarray] = None
        self.extracted_text: str = ""
        self.extracted_fields: Dict[str, SabreField] = {}
        self.timestamp: datetime = datetime.now()
        self.is_valid_screen: bool = False
        
    def load_from_clipboard(self) -> bool:
        """
        Load image from clipboard (CTRL+V)
        
        Returns:
            True if image loaded successfully, False otherwise
        """
        try:
            # Get image from clipboard
            image = pyperclip.paste()
            if isinstance(image, Image.Image):
                self.raw_image = np.array(image)
                return True
            else:
                # Try to get screenshot if clipboard doesn't have image
                self.raw_image = pyautogui.screenshot()
                self.raw_image = np.array(self.raw_image)
                return True
        except Exception as e:
            print(f"Error loading from clipboard: {e}")
            return False
    
    def load_from_file(self, file_path: str) -> bool:
        """
        Load image from file
        
        Args:
            file_path: Path to image file
            
        Returns:
            True if image loaded successfully, False otherwise
        """
        try:
            self.raw_image = cv2.imread(file_path)
            if self.raw_image is None:
                raise ValueError(f"Could not load image from {file_path}")
            return True
        except Exception as e:
            print(f"Error loading from file: {e}")
            return False
    
    def detect_sabre_pattern(self) -> bool:
        """
        Detect if the image contains Sabre Interact v2.1 pattern
        
        Returns:
            True if Sabre pattern detected, False otherwise
        """
        if self.raw_image is None:
            return False
        
        try:
            # Convert to grayscale for text detection
            gray = cv2.cvtColor(self.raw_image, cv2.COLOR_BGR2GRAY)
            
            # Look for characteristic Sabre patterns
            sabre_indicators = [
                r'Reserva\s*-\s*[A-Z0-9]{6}',  # Reservation pattern
                r'Nomes',  # Passenger names header
                r'Voo\s*\(CIA\)',  # Flight carrier header
                r'Voo\s*\(Numero\)',  # Flight number header
                r'Cls',  # Class header
                r'De-Para',  # Route header
                r'Data',  # Date header
                r'Stp\s*Nbr',  # Status header
            ]
            
            # Use OCR to extract text for pattern matching
            extracted_text = self._extract_text_with_ocr()
            self.extracted_text = extracted_text
            
            # Check for Sabre indicators
            found_indicators = 0
            for pattern in sabre_indicators:
                if re.search(pattern, extracted_text, re.IGNORECASE):
                    found_indicators += 1
            
            # Consider it Sabre if we find at least 5 indicators
            self.is_valid_screen = found_indicators >= 5
            return self.is_valid_screen
            
        except Exception as e:
            print(f"Error detecting Sabre pattern: {e}")
            return False
    
    def _extract_text_with_ocr(self) -> str:
        """
        Extract text from image using OCR
        
        Returns:
            Extracted text as string
        """
        try:
            # This would integrate with EasyOCR in the OCR module
            # For now, return extracted text from the image
            # This is a placeholder that will be implemented in the OCR module
            return self.extracted_text
        except Exception as e:
            print(f"Error in OCR extraction: {e}")
            return ""
    
    def parse_fields(self) -> Dict[str, SabreField]:
        """
        Parse and extract all fields from Sabre screen
        
        Returns:
            Dictionary of extracted fields
        """
        if not self.is_valid_screen:
            return {}
        
        try:
            # Extract individual fields using regex patterns
            fields = {}
            
            # PNR Code
            pnr_match = re.search(r'Reserva\s*-\s*([A-Z0-9]{6})', self.extracted_text)
            if pnr_match:
                fields['pnr'] = SabreField(
                    name='pnr',
                    value=pnr_match.group(1).upper(),
                    confidence=0.95,
                    position=(0, 0, 0, 0)  # Would be actual coordinates
                )
            
            # Passenger Name
            name_match = re.search(r'Nomes\s*\n\s*([^\n]+)', self.extracted_text)
            if name_match:
                fields['passenger_name'] = SabreField(
                    name='passenger_name',
                    value=name_match.group(1).strip(),
                    confidence=0.90,
                    position=(0, 0, 0, 0)
                )
            
            # Flight Information (multiple lines)
            flight_lines = re.findall(r'([A-Z]{2})\s+(\d{3,4})\s+([A-Z])\s+([A-Z]{3}-[A-Z]{3})\s+(\d{2}[A-Z]{3})\s+([A-Z]{2,3})', self.extracted_text)
            if flight_lines:
                # Take first flight line for now
                carrier, flight_num, classe, trecho, data_voo, status = flight_lines[0]
                fields.update({
                    'carrier': SabreField('carrier', carrier, 0.95, (0, 0, 0, 0)),
                    'flight_num': SabreField('flight_num', flight_num, 0.95, (0, 0, 0, 0)),
                    'classe': SabreField('classe', classe, 0.95, (0, 0, 0, 0)),
                    'trecho': SabreField('trecho', trecho, 0.95, (0, 0, 0, 0)),
                    'data_voo': SabreField('data_voo', data_voo, 0.95, (0, 0, 0, 0)),
                    'status': SabreField('status', status, 0.95, (0, 0, 0, 0))
                })
            
            # Ticket Number
            tkt_match = re.search(r'TE\s+(\d{3}-\d{10})', self.extracted_text)
            if tkt_match:
                fields['ticket_number'] = SabreField(
                    name='ticket_number',
                    value=tkt_match.group(1),
                    confidence=0.90,
                    position=(0, 0, 0, 0)
                )
            
            # Authorization Code
            auth_match = re.search(r'Auth\s*Code\s*:\s*([A-Z0-9_]+)', self.extracted_text)
            if auth_match:
                fields['auth_code'] = SabreField(
                    name='auth_code',
                    value=auth_match.group(1),
                    confidence=0.85,
                    position=(0, 0, 0, 0)
                )
            
            self.extracted_fields = fields
            return fields
            
        except Exception as e:
            print(f"Error parsing fields: {e}")
            return {}
    
    def validate_integrity(self) -> List[ValidationResult]:
        """
        Validate extracted data integrity using business rules
        
        Returns:
            List of validation results
        """
        results = []
        
        # Validate PNR
        if 'pnr' in self.extracted_fields:
            pnr_result = self.rules_engine.validate_pnr_format(self.extracted_fields['pnr'].value)
            results.append(pnr_result)
        
        # Validate flight status
        if 'status' in self.extracted_fields:
            status_result = self.rules_engine.validate_flight_status(self.extracted_fields['status'].value)
            results.append(status_result)
        
        # Validate carrier
        if 'carrier' in self.extracted_fields:
            carrier_result = self.rules_engine.validate_carrier_code(self.extracted_fields['carrier'].value)
            results.append(carrier_result)
        
        # Validate estouro de classe eligibility
        if 'classe' in self.extracted_fields and 'auth_code' in self.extracted_fields:
            estouro_result = self.rules_engine.validate_estouro_classe({
                'classe': self.extracted_fields['classe'].value,
                'auth_code': self.extracted_fields['auth_code'].value
            })
            results.append(estouro_result)
        
        return results
    
    def get_field_value(self, field_name: str) -> Optional[str]:
        """
        Get value of a specific field
        
        Args:
            field_name: Name of the field
            
        Returns:
            Field value if found, None otherwise
        """
        if field_name in self.extracted_fields:
            return self.extracted_fields[field_name].value
        return None
    
    def get_all_fields(self) -> Dict[str, str]:
        """
        Get all extracted fields as a simple dictionary
        
        Returns:
            Dictionary of field names and values
        """
        return {name: field.value for name, field in self.extracted_fields.items()}
    
    def get_field_confidence(self, field_name: str) -> float:
        """
        Get confidence score for a specific field
        
        Args:
            field_name: Name of the field
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        if field_name in self.extracted_fields:
            return self.extracted_fields[field_name].confidence
        return 0.0
    
    def is_complete(self) -> bool:
        """
        Check if all required fields for estouro de classe are present
        
        Returns:
            True if all required fields are present, False otherwise
        """
        required_fields = ['pnr', 'carrier', 'flight_num', 'classe', 'data_voo', 'trecho', 'status']
        return all(field in self.extracted_fields for field in required_fields)
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Get summary of screen processing
        
        Returns:
            Dictionary with processing information
        """
        return {
            'timestamp': self.timestamp.isoformat(),
            'is_valid_sabre': self.is_valid_screen,
            'field_count': len(self.extracted_fields),
            'fields': {name: field.value for name, field in self.extracted_fields.items()},
            'confidences': {name: field.confidence for name, field in self.extracted_fields.items()},
            'is_complete': self.is_complete()
        }