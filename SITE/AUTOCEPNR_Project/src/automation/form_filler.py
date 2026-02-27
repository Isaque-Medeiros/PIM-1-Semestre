"""
FormFiller Module
Handles the complete form filling workflow with validation and error handling
"""

import asyncio
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging

from ..core.latam_form import LatamForm
from ..core.rules_engine import RulesEngine, ValidationResult
from ..core.sabre_screen import SabreScreen
from ..ocr.image_processor import ImageProcessor


@dataclass
class FillResult:
    """Result of form filling operation"""
    success: bool
    field_results: List[ValidationResult]
    submission_result: Optional[ValidationResult] = None
    error_message: Optional[str] = None
    processing_time: float = 0.0


class FormFiller:
    """Complete form filling workflow manager"""
    
    def __init__(self, rules_engine: RulesEngine):
        """
        Initialize FormFiller with rules engine
        
        Args:
            rules_engine: RulesEngine instance for validation
        """
        self.rules_engine = rules_engine
        self.latam_form: Optional[LatamForm] = None
        self.sabre_screen: Optional[SabreScreen] = None
        self.image_processor: Optional[ImageProcessor] = None
        self.logger = logging.getLogger(__name__)
        
        # Configuration
        self.human_delay = 0.2  # 200ms delay between fields as specified
        self.max_retries = 3
        self.timeout = 60  # 60 seconds timeout for operations
        
    def initialize_components(self, latam_form: LatamForm):
        """
        Initialize form filler with LatamForm instance
        
        Args:
            latam_form: LatamForm instance
        """
        self.latam_form = latam_form
        self.sabre_screen = SabreScreen(self.rules_engine)
        self.image_processor = ImageProcessor(self.rules_engine)
        
    async def process_complete_workflow(self, image_source: Any = None) -> FillResult:
        """
        Process complete workflow: OCR -> Validation -> Form Filling -> Submission
        
        Args:
            image_source: Image source (clipboard, file path, or numpy array)
            
        Returns:
            FillResult with complete workflow results
        """
        start_time = time.time()
        
        try:
            # Step 1: Process image and extract text
            self.logger.info("Starting complete workflow...")
            image, extracted_text = self.image_processor.process_image_input(image_source)
            
            if not extracted_text:
                return FillResult(
                    success=False,
                    field_results=[],
                    error_message="No text extracted from image",
                    processing_time=time.time() - start_time
                )
            
            # Step 2: Create SabreScreen and parse fields
            self.sabre_screen.raw_image = image
            self.sabre_screen.extracted_text = extracted_text
            self.sabre_screen.is_valid_screen = self.sabre_screen.detect_sabre_pattern()
            
            if not self.sabre_screen.is_valid_screen:
                return FillResult(
                    success=False,
                    field_results=[],
                    error_message="Invalid Sabre screen format detected",
                    processing_time=time.time() - start_time
                )
            
            # Parse fields from extracted text
            extracted_fields = self.sabre_screen.parse_fields()
            
            # Step 3: Validate extracted data
            validation_results = self.sabre_screen.validate_integrity()
            
            # Check for critical validation failures
            critical_failures = [r for r in validation_results if not r.is_valid]
            if critical_failures:
                return FillResult(
                    success=False,
                    field_results=validation_results,
                    error_message=f"Critical validation failures: {len(critical_failures)}",
                    processing_time=time.time() - start_time
                )
            
            # Step 4: Focus on Latam form
            if not self.latam_form or not self.latam_form.is_form_loaded:
                self.logger.warning("Latam form not focused, attempting to focus...")
                # Try to focus on form (this would be handled by BrowserManager)
                # For now, assume form is already focused
            
            if not self.latam_form or not self.latam_form.is_form_loaded:
                return FillResult(
                    success=False,
                    field_results=validation_results,
                    error_message="Latam form not available or not loaded",
                    processing_time=time.time() - start_time
                )
            
            # Step 5: Fill form fields
            field_mapping = self._map_sabre_to_latam(extracted_fields)
            fill_results = await self.latam_form.fill_all(field_mapping)
            
            # Step 6: Submit form
            submission_result = await self.latam_form.submit_form()
            
            # Step 7: Compile results
            total_success = all(r.is_valid for r in fill_results) and submission_result.is_valid
            
            return FillResult(
                success=total_success,
                field_results=fill_results,
                submission_result=submission_result,
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error(f"Error in complete workflow: {e}")
            return FillResult(
                success=False,
                field_results=[],
                error_message=f"Workflow error: {str(e)}",
                processing_time=time.time() - start_time
            )
    
    def _map_sabre_to_latam(self, sabre_fields: Dict[str, Any]) -> Dict[str, str]:
        """
        Map Sabre fields to Latam form fields according to specification
        
        Args:
            sabre_fields: Extracted fields from Sabre screen
            
        Returns:
            Mapped fields for Latam form
        """
        mapped_fields = {}
        
        # Map fields according to specification.md
        field_mappings = {
            'pnr': 'pnr',
            'carrier': 'carrier', 
            'flight_num': 'vuelo',
            'classe': 'classe',
            'data_voo': 'data_voo',
            'trecho': 'segmento',
            'status': 'num_segmento',
            'passenger_name': 'pax'
        }
        
        for sabre_field, latam_field in field_mappings.items():
            if sabre_field in sabre_fields:
                mapped_fields[latam_field] = sabre_fields[sabre_field].value
        
        # Add static/default values for fields that need selection
        # These would be handled by the LatamForm based on business rules
        mapped_fields['cidade'] = 'SCL'  # Example default
        mapped_fields['departamento'] = 'Departamento Técnico'
        mapped_fields['razao'] = 'PIC - Upgrade'
        mapped_fields['autorizador'] = 'Supervisor Autorizado'
        mapped_fields['cto_des'] = 'UPGRADE'  # Example default
        
        return mapped_fields
    
    async def fill_single_field(self, field_name: str, value: str) -> ValidationResult:
        """
        Fill a single field with validation
        
        Args:
            field_name: Name of the field to fill
            value: Value to fill in the field
            
        Returns:
            ValidationResult of the fill operation
        """
        try:
            if not self.latam_form or not self.latam_form.is_form_loaded:
                return ValidationResult(False, "Formulário não carregado", "Focar no formulário Latam")
            
            # Get field configuration
            field_config = self.latam_form.field_mappings.get(field_name)
            if not field_config:
                return ValidationResult(False, f"Campo {field_name} não mapeado", "Verificar mapeamento de campos")
            
            # Fill the field
            result = await self.latam_form._fill_field(field_name, value, field_config)
            
            # Add human delay
            await asyncio.sleep(self.human_delay)
            
            return result
            
        except Exception as e:
            return ValidationResult(False, f"Erro ao preencher campo {field_name}: {e}", "Verificar conexão e formulário")
    
    async def validate_form_completion(self) -> Dict[str, Any]:
        """
        Validate form completion status
        
        Returns:
            Dictionary with completion status
        """
        try:
            if not self.latam_form:
                return {"status": "no_form", "message": "Nenhum formulário carregado"}
            
            if not self.latam_form.is_form_loaded:
                return {"status": "form_not_loaded", "message": "Formulário não carregado"}
            
            # Get form status
            form_status = await self.latam_form.get_form_status()
            
            # Check if all required fields are filled
            required_fields = ['pnr', 'carrier', 'vuelo', 'classe', 'data_voo', 'segmento']
            filled_fields = []
            empty_fields = []
            
            for field in required_fields:
                if field in form_status.get('fields', {}):
                    value = form_status['fields'][field]
                    if value and value.strip():
                        filled_fields.append(field)
                    else:
                        empty_fields.append(field)
            
            completion_percentage = (len(filled_fields) / len(required_fields)) * 100
            
            return {
                "status": "form_loaded",
                "completion_percentage": completion_percentage,
                "filled_fields": filled_fields,
                "empty_fields": empty_fields,
                "total_required": len(required_fields),
                "form_url": form_status.get('url', 'Unknown')
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def retry_failed_fields(self, fill_results: List[ValidationResult], 
                                 extracted_data: Dict[str, str]) -> List[ValidationResult]:
        """
        Retry filling failed fields
        
        Args:
            fill_results: Results from initial fill attempt
            extracted_data: Original extracted data
            
        Returns:
            Updated fill results
        """
        try:
            retry_results = []
            
            for result in fill_results:
                if not result.is_valid:
                    # Get field name from error message or result
                    field_name = self._extract_field_name_from_result(result)
                    
                    if field_name and field_name in extracted_data:
                        # Retry filling the field
                        retry_result = await self.fill_single_field(field_name, extracted_data[field_name])
                        retry_results.append(retry_result)
                    else:
                        retry_results.append(result)
                else:
                    retry_results.append(result)
            
            return retry_results
            
        except Exception as e:
            self.logger.error(f"Error retrying failed fields: {e}")
            return fill_results
    
    def _extract_field_name_from_result(self, result: ValidationResult) -> Optional[str]:
        """
        Extract field name from validation result
        
        Args:
            result: ValidationResult object
            
        Returns:
            Field name if found, None otherwise
        """
        if result.error_message:
            # Try to extract field name from error message
            # This is a simple implementation - could be enhanced
            if "campo" in result.error_message.lower():
                parts = result.error_message.split()
                for i, part in enumerate(parts):
                    if part.lower() == "campo" and i + 1 < len(parts):
                        return parts[i + 1].replace(":", "").replace(".", "")
        
        return None
    
    async def get_workflow_status(self) -> Dict[str, Any]:
        """
        Get current workflow status
        
        Returns:
            Dictionary with workflow status information
        """
        try:
            status = {
                "components_initialized": {
                    "latam_form": self.latam_form is not None,
                    "sabre_screen": self.sabre_screen is not None,
                    "image_processor": self.image_processor is not None
                },
                "form_status": None,
                "sabre_status": None
            }
            
            # Get form status if available
            if self.latam_form:
                form_status = await self.latam_form.get_form_status()
                status["form_status"] = form_status
            
            # Get Sabre status if available
            if self.sabre_screen:
                sabre_status = self.sabre_screen.get_processing_summary()
                status["sabre_status"] = sabre_status
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting workflow status: {e}")
            return {"error": str(e)}