<<<<<<< HEAD:AUTOCEPNR_Project/src/core/rules_engine.py
"""
Rules Engine for Latam Auto-Filler
Handles business logic validation, PIC rules, and class restrictions
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationResult:
    """Result of validation process"""
    is_valid: bool
    error_message: Optional[str] = None
    suggested_action: Optional[str] = None


class RulesEngine:
    """Business rules validation engine"""
    
    def __init__(self, rules_file: str = "rules/sabre_mapping.json"):
        """
        Initialize rules engine with configuration files
        
        Args:
            rules_file: Path to Sabre mapping configuration
        """
        self.rules_file = rules_file
        self.mapping_config = self._load_mapping_config()
        
    def _load_mapping_config(self) -> Dict:
        """Load Sabre to Latam field mapping configuration"""
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Mapping configuration not found: {self.rules_file}")
    
    def validate_estouro_classe(self, extracted_data: Dict) -> ValidationResult:
        """
        Validate if "Estouro de Classe" is permitted based on business rules
        
        Args:
            extracted_data: Data extracted from Sabre screen
            
        Returns:
            ValidationResult with validation status
        """
        # Rule: Only allow upgrade if class is Q, S, Y and has PIC authorization
        class_original = extracted_data.get('classe', '').upper()
        auth_code = extracted_data.get('auth_code', '').upper()
        
        # Check if class is eligible for upgrade
        if class_original not in ['Q', 'S', 'Y']:
            return ValidationResult(
                is_valid=False,
                error_message=f"Classe {class_original} não é elegível para estouro de classe",
                suggested_action="Verificar classe original da reserva"
            )
        
        # Check PIC authorization
        if not self._validate_pic_authorization(auth_code):
            return ValidationResult(
                is_valid=False,
                error_message=f"Código de autorização {auth_code} não permite estouro de classe",
                suggested_action="Verificar autorização PIC no Sabre"
            )
        
        return ValidationResult(is_valid=True)
    
    def _validate_pic_authorization(self, auth_code: str) -> bool:
        """Validate PIC authorization code"""
        # According to specification: PIC_S23 allows Premium Economy upgrade
        valid_codes = ['PIC_S23', 'PIC_S24', 'PIC_S25']
        return auth_code in valid_codes
    
    def validate_pnr_format(self, pnr: str) -> ValidationResult:
        """Validate PNR format (6 alphanumeric characters)"""
        if not pnr or len(pnr) != 6:
            return ValidationResult(
                is_valid=False,
                error_message=f"PNR inválido: {pnr}",
                suggested_action="Verificar formato do PNR (6 caracteres alfanuméricos)"
            )
        
        if not re.match(r'^[A-Z0-9]{6}$', pnr):
            return ValidationResult(
                is_valid=False,
                error_message=f"PNR contém caracteres inválidos: {pnr}",
                suggested_action="PNR deve conter apenas letras maiúsculas e números"
            )
        
        return ValidationResult(is_valid=True)
    
    def validate_flight_status(self, status: str) -> ValidationResult:
        """Validate flight status for estouro de classe"""
        # According to specification: Only HK or SA status allowed
        valid_statuses = ['HK', 'SA']
        if status.upper() not in valid_statuses:
            return ValidationResult(
                is_valid=False,
                error_message=f"Status de voo {status} não permite estouro de classe",
                suggested_action="Apenas status HK ou SA são permitidos"
            )
        
        return ValidationResult(is_valid=True)
    
    def validate_date_format(self, date_str: str) -> Tuple[bool, str]:
        """
        Validate and convert date format from Sabre (13MAR) to Brazilian format (13/03/2026)
        
        Args:
            date_str: Date string from Sabre (e.g., "13MAR")
            
        Returns:
            Tuple of (is_valid, formatted_date_or_error)
        """
        try:
            # Convert month abbreviation to number
            month_map = {
                'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04',
                'MAI': '05', 'JUN': '06', 'JUL': '07', 'AGO': '08',
                'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'
            }
            
            if len(date_str) != 5 or not date_str[:2].isdigit():
                return False, "Formato de data inválido"
            
            day = date_str[:2]
            month_abbr = date_str[2:].upper()
            
            if month_abbr not in month_map:
                return False, f"Mês inválido: {month_abbr}"
            
            month = month_map[month_abbr]
            year = datetime.now().year
            
            formatted_date = f"{day}/{month}/{year}"
            return True, formatted_date
            
        except Exception as e:
            return False, f"Erro ao processar data: {str(e)}"
    
    def validate_carrier_code(self, carrier: str) -> ValidationResult:
        """Validate carrier code mapping"""
        valid_carriers = ['LA', 'LP', '4C', 'JJ']
        if carrier.upper() not in valid_carriers:
            return ValidationResult(
                is_valid=False,
                error_message=f"Carrier {carrier} não mapeado",
                suggested_action=f"Carrier deve ser um dos: {', '.join(valid_carriers)}"
            )
        
        return ValidationResult(is_valid=True)
    
    def get_field_mapping(self, field_name: str) -> Optional[Dict]:
        """Get HTML field mapping for a Sabre field"""
        for section_name, section_data in self.mapping_config.items():
            if field_name in section_data:
                return section_data[field_name]
        return None
    
    def validate_name_correction(self, old_name: str, new_name: str) -> ValidationResult:
        """
        Validate name correction based on correction rules
        Implements the 7 types of corrections from correcao_de_nome.txt
        """
        # Remove titles and normalize
        old_clean = self._normalize_name(old_name)
        new_clean = self._normalize_name(new_name)
        
        if old_clean == new_clean:
            return ValidationResult(is_valid=True)
        
        # Check for type 1: Orthographic (max 3 letter differences)
        if self._is_orthographic_correction(old_clean, new_clean):
            return ValidationResult(is_valid=True)
        
        # Check for type 2: Inverted names
        if self._is_inverted_names(old_clean, new_clean):
            return ValidationResult(is_valid=True)
        
        # Check for type 3: Addition without substitution
        if self._is_addition_correction(old_clean, new_clean):
            return ValidationResult(is_valid=True)
        
        # Check for type 4: Duplication removal
        if self._is_duplication_correction(old_clean, new_clean):
            return ValidationResult(is_valid=True)
        
        # Check for type 5: Agname (JR, Neto, etc.)
        if self._is_agname_correction(old_clean, new_clean):
            return ValidationResult(is_valid=True)
        
        return ValidationResult(
            is_valid=False,
            error_message="Correção de nome requer documentação comprobatória",
            suggested_action="Anexar documentação para mudança legal (casamento, divórcio, etc.)"
        )
    
    def _normalize_name(self, name: str) -> str:
        """Remove titles and normalize name"""
        titles = ['MS', 'MR', 'MSTR', 'JR', 'NETO', 'FILHO']
        name_upper = name.upper()
        
        for title in titles:
            name_upper = name_upper.replace(title, '')
        
        return ' '.join(name_upper.split())  # Remove extra spaces
    
    def _is_orthographic_correction(self, old_name: str, new_name: str) -> bool:
        """
        Check if correction is orthographic using character similarity ratio.
        Examples: GONSALES->GONZALEZ (75%), SILVA->SYLVA (80%)
        Threshold: >70% similarity indicates orthographic variation
        """
        from difflib import SequenceMatcher
        
        # Use sequence matching; accept if >70% similar (allows up to ~2-3 char diffs in 8-char name)
        similarity = SequenceMatcher(None, old_name, new_name).ratio()
        
        # Orthographic corrections typically have high similarity
        return similarity > 0.70
    
    def _is_inverted_names(self, old_name: str, new_name: str) -> bool:
        """Check if names are simply inverted"""
        # Try splitting by space or slash
        for separator in [' ', '/']:
            if separator in old_name or separator in new_name:
                old_parts = old_name.split(separator) if separator in old_name else [old_name]
                new_parts = new_name.split(separator) if separator in new_name else [new_name]
                
                if len(old_parts) == len(new_parts) and len(old_parts) > 1:
                    # Check if it's just order inversion
                    if old_parts == new_parts[::-1]:
                        return True
        
        return False
    
    def _is_addition_correction(self, old_name: str, new_name: str) -> bool:
        """Check if correction is addition without substitution"""
        # Split by both space and slash for compatibility with FIRSTNAME/LASTNAME format
        old_parts = set(old_name.replace('/', ' ').split())
        new_parts = set(new_name.replace('/', ' ').split())
        
        # All old parts must be in new name
        return old_parts.issubset(new_parts) and len(new_parts) > len(old_parts)
    
    def _is_duplication_correction(self, old_name: str, new_name: str) -> bool:
        """Check if correction removes duplication"""
        old_parts = old_name.split()
        new_parts = new_name.split()
        
        # Check if new name is old name with duplicates removed
        return new_parts == list(dict.fromkeys(old_parts))  # Remove duplicates while preserving order
    
    def _is_agname_correction(self, old_name: str, new_name: str) -> bool:
        """Check if correction is agname addition/removal"""
        agnames = ['JR', 'NETO', 'FILHO', 'SR']
        
        old_has_agname = any(agname in old_name.upper() for agname in agnames)
        new_has_agname = any(agname in new_name.upper() for agname in agnames)
        
        # If one has agname and other doesn't, it's likely agname correction
=======
"""
Rules Engine for Latam Auto-Filler
Handles business logic validation, PIC rules, and class restrictions
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationResult:
    """Result of validation process"""
    is_valid: bool
    error_message: Optional[str] = None
    suggested_action: Optional[str] = None


class RulesEngine:
    """Business rules validation engine"""
    
    def __init__(self, rules_file: str = "rules/sabre_mapping.json"):
        """
        Initialize rules engine with configuration files
        
        Args:
            rules_file: Path to Sabre mapping configuration
        """
        self.rules_file = rules_file
        self.mapping_config = self._load_mapping_config()
        
    def _load_mapping_config(self) -> Dict:
        """Load Sabre to Latam field mapping configuration"""
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Mapping configuration not found: {self.rules_file}")
    
    def validate_estouro_classe(self, extracted_data: Dict) -> ValidationResult:
        """
        Validate if "Estouro de Classe" is permitted based on business rules
        
        Args:
            extracted_data: Data extracted from Sabre screen
            
        Returns:
            ValidationResult with validation status
        """
        # Rule: Only allow upgrade if class is Q, S, Y and has PIC authorization
        class_original = extracted_data.get('classe', '').upper()
        auth_code = extracted_data.get('auth_code', '').upper()
        
        # Check if class is eligible for upgrade
        if class_original not in ['Q', 'S', 'Y']:
            return ValidationResult(
                is_valid=False,
                error_message=f"Classe {class_original} não é elegível para estouro de classe",
                suggested_action="Verificar classe original da reserva"
            )
        
        # Check PIC authorization
        if not self._validate_pic_authorization(auth_code):
            return ValidationResult(
                is_valid=False,
                error_message=f"Código de autorização {auth_code} não permite estouro de classe",
                suggested_action="Verificar autorização PIC no Sabre"
            )
        
        return ValidationResult(is_valid=True)
    
    def _validate_pic_authorization(self, auth_code: str) -> bool:
        """Validate PIC authorization code"""
        # According to specification: PIC_S23 allows Premium Economy upgrade
        valid_codes = ['PIC_S23', 'PIC_S24', 'PIC_S25']
        return auth_code in valid_codes
    
    def validate_pnr_format(self, pnr: str) -> ValidationResult:
        """Validate PNR format (6 alphanumeric characters)"""
        if not pnr or len(pnr) != 6:
            return ValidationResult(
                is_valid=False,
                error_message=f"PNR inválido: {pnr}",
                suggested_action="Verificar formato do PNR (6 caracteres alfanuméricos)"
            )
        
        if not re.match(r'^[A-Z0-9]{6}$', pnr):
            return ValidationResult(
                is_valid=False,
                error_message=f"PNR contém caracteres inválidos: {pnr}",
                suggested_action="PNR deve conter apenas letras maiúsculas e números"
            )
        
        return ValidationResult(is_valid=True)
    
    def validate_flight_status(self, status: str) -> ValidationResult:
        """Validate flight status for estouro de classe"""
        # According to specification: Only HK or SA status allowed
        valid_statuses = ['HK', 'SA']
        if status.upper() not in valid_statuses:
            return ValidationResult(
                is_valid=False,
                error_message=f"Status de voo {status} não permite estouro de classe",
                suggested_action="Apenas status HK ou SA são permitidos"
            )
        
        return ValidationResult(is_valid=True)
    
    def validate_date_format(self, date_str: str) -> Tuple[bool, str]:
        """
        Validate and convert date format from Sabre (13MAR) to Brazilian format (13/03/2026)
        
        Args:
            date_str: Date string from Sabre (e.g., "13MAR")
            
        Returns:
            Tuple of (is_valid, formatted_date_or_error)
        """
        try:
            # Convert month abbreviation to number
            month_map = {
                'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04',
                'MAI': '05', 'JUN': '06', 'JUL': '07', 'AGO': '08',
                'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'
            }
            
            if len(date_str) != 5 or not date_str[:2].isdigit():
                return False, "Formato de data inválido"
            
            day = date_str[:2]
            month_abbr = date_str[2:].upper()
            
            if month_abbr not in month_map:
                return False, f"Mês inválido: {month_abbr}"
            
            month = month_map[month_abbr]
            year = datetime.now().year
            
            formatted_date = f"{day}/{month}/{year}"
            return True, formatted_date
            
        except Exception as e:
            return False, f"Erro ao processar data: {str(e)}"
    
    def validate_carrier_code(self, carrier: str) -> ValidationResult:
        """Validate carrier code mapping"""
        valid_carriers = ['LA', 'LP', '4C', 'JJ']
        if carrier.upper() not in valid_carriers:
            return ValidationResult(
                is_valid=False,
                error_message=f"Carrier {carrier} não mapeado",
                suggested_action=f"Carrier deve ser um dos: {', '.join(valid_carriers)}"
            )
        
        return ValidationResult(is_valid=True)
    
    def get_field_mapping(self, field_name: str) -> Optional[Dict]:
        """Get HTML field mapping for a Sabre field"""
        for section_name, section_data in self.mapping_config.items():
            if field_name in section_data:
                return section_data[field_name]
        return None
    
    def validate_name_correction(self, old_name: str, new_name: str) -> ValidationResult:
        """
        Validate name correction based on correction rules
        Implements the 7 types of corrections from correcao_de_nome.txt
        """
        # Remove titles and normalize
        old_clean = self._normalize_name(old_name)
        new_clean = self._normalize_name(new_name)
        
        if old_clean == new_clean:
            return ValidationResult(is_valid=True)
        
        # Check for type 1: Orthographic (max 3 letter differences)
        if self._is_orthographic_correction(old_clean, new_clean):
            return ValidationResult(is_valid=True)
        
        # Check for type 2: Inverted names
        if self._is_inverted_names(old_clean, new_clean):
            return ValidationResult(is_valid=True)
        
        # Check for type 3: Addition without substitution
        if self._is_addition_correction(old_clean, new_clean):
            return ValidationResult(is_valid=True)
        
        # Check for type 4: Duplication removal
        if self._is_duplication_correction(old_clean, new_clean):
            return ValidationResult(is_valid=True)
        
        # Check for type 5: Agname (JR, Neto, etc.)
        if self._is_agname_correction(old_clean, new_clean):
            return ValidationResult(is_valid=True)
        
        return ValidationResult(
            is_valid=False,
            error_message="Correção de nome requer documentação comprobatória",
            suggested_action="Anexar documentação para mudança legal (casamento, divórcio, etc.)"
        )
    
    def _normalize_name(self, name: str) -> str:
        """Remove titles and normalize name"""
        titles = ['MS', 'MR', 'MSTR', 'JR', 'NETO', 'FILHO']
        name_upper = name.upper()
        
        for title in titles:
            name_upper = name_upper.replace(title, '')
        
        return ' '.join(name_upper.split())  # Remove extra spaces
    
    def _is_orthographic_correction(self, old_name: str, new_name: str) -> bool:
        """Check if correction is orthographic (max 3 letter differences)"""
        # Simple character difference count
        max_diffs = 3
        diff_count = 0
        
        # Pad shorter string with spaces for comparison
        max_len = max(len(old_name), len(new_name))
        old_padded = old_name.ljust(max_len)
        new_padded = new_name.ljust(max_len)
        
        for old_char, new_char in zip(old_padded, new_padded):
            if old_char != new_char:
                diff_count += 1
                if diff_count > max_diffs:
                    return False
        
        return diff_count <= max_diffs
    
    def _is_inverted_names(self, old_name: str, new_name: str) -> bool:
        """Check if names are simply inverted"""
        old_parts = old_name.split()
        new_parts = new_name.split()
        
        if len(old_parts) != len(new_parts):
            return False
        
        # Check if it's just order inversion
        return old_parts == new_parts[::-1]
    
    def _is_addition_correction(self, old_name: str, new_name: str) -> bool:
        """Check if correction is addition without substitution"""
        old_parts = set(old_name.split())
        new_parts = set(new_name.split())
        
        # All old parts must be in new name
        return old_parts.issubset(new_parts) and len(new_parts) > len(old_parts)
    
    def _is_duplication_correction(self, old_name: str, new_name: str) -> bool:
        """Check if correction removes duplication"""
        old_parts = old_name.split()
        new_parts = new_name.split()
        
        # Check if new name is old name with duplicates removed
        return new_parts == list(dict.fromkeys(old_parts))  # Remove duplicates while preserving order
    
    def _is_agname_correction(self, old_name: str, new_name: str) -> bool:
        """Check if correction is agname addition/removal"""
        agnames = ['JR', 'NETO', 'FILHO', 'SR']
        
        old_has_agname = any(agname in old_name.upper() for agname in agnames)
        new_has_agname = any(agname in new_name.upper() for agname in agnames)
        
        # If one has agname and other doesn't, it's likely agname correction
>>>>>>> 7a10112 (FirstlProjectSDDMetodologia):SITE/AUTOCEPNR_Project/src/core/rules_engine.py
        return old_has_agname != new_has_agname