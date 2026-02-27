#!/usr/bin/env python3
"""
Test script for Latam Auto-Filler
Tests all components and functionality
"""

import sys
import os
import asyncio
import time
import logging
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.rules_engine import RulesEngine, ValidationResult
from src.core.sabre_screen import SabreScreen
from src.core.latam_form import LatamForm
from src.ocr.image_processor import ImageProcessor
from src.automation.browser_manager import BrowserManager
from src.automation.form_filler import FormFiller
from src.ui.overlay_window import OverlayWindow
from src.ui.status_indicator import StatusIndicator


class TestRunner:
    """Test runner for Latam Auto-Filler"""
    
    def __init__(self):
        """Initialize test runner"""
        self.logger = self._setup_logging()
        self.test_results = []
        
    def _setup_logging(self):
        """Setup test logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - TEST - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def log_test(self, test_name, success, message=""):
        """Log test result"""
        status = "PASS" if success else "FAIL"
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message
        })
        self.logger.info(f"[{status}] {test_name}: {message}")
    
    def test_rules_engine(self):
        """Test Rules Engine"""
        try:
            rules_engine = RulesEngine()
            
            # Test PNR validation
            valid_pnr_result = rules_engine.validate_pnr_format("ABC123")
            invalid_pnr_result = rules_engine.validate_pnr_format("invalid")
            
            assert valid_pnr_result.is_valid, "Valid PNR should be accepted"
            assert not invalid_pnr_result.is_valid, "Invalid PNR should be rejected"
            
            # Test date validation
            valid_date, formatted_date = rules_engine.validate_date_format("13MAR")
            assert valid_date, "Valid date should be accepted"
            assert formatted_date == "13/03/2026", f"Date should be formatted correctly: {formatted_date}"
            
            # Test carrier validation
            valid_carrier = rules_engine.validate_carrier_code("LA")
            invalid_carrier = rules_engine.validate_carrier_code("XX")
            
            assert valid_carrier.is_valid, "Valid carrier should be accepted"
            assert not invalid_carrier.is_valid, "Invalid carrier should be rejected"
            
            self.log_test("Rules Engine", True, "All validation tests passed")
            return True
            
        except Exception as e:
            self.log_test("Rules Engine", False, f"Error: {e}")
            return False
    
    def test_sabre_screen(self):
        """Test SabreScreen object"""
        try:
            rules_engine = RulesEngine()
            sabre_screen = SabreScreen(rules_engine)
            
            # Test object creation
            assert sabre_screen.rules_engine is not None, "Rules engine should be set"
            assert not sabre_screen.is_valid_screen, "Screen should not be valid initially"
            
            # Test field creation
            from src.core.sabre_screen import SabreField
            test_field = SabreField("test", "value", 0.9, (0, 0, 100, 50))
            assert test_field.name == "test", "Field name should be set"
            assert test_field.value == "value", "Field value should be set"
            assert test_field.confidence == 0.9, "Field confidence should be set"
            
            self.log_test("SabreScreen", True, "Object creation and field tests passed")
            return True
            
        except Exception as e:
            self.log_test("SabreScreen", False, f"Error: {e}")
            return False
    
    def test_latam_form(self):
        """Test LatamForm object"""
        try:
            rules_engine = RulesEngine()
            latam_form = LatamForm(rules_engine)
            
            # Test object creation
            assert latam_form.rules_engine is not None, "Rules engine should be set"
            assert latam_form.browser_type == "chromium", "Default browser type should be chromium"
            
            # Test field mappings
            assert "pnr" in latam_form.field_mappings, "PNR field should be mapped"
            assert "carrier" in latam_form.field_mappings, "Carrier field should be mapped"
            
            pnr_mapping = latam_form.field_mappings["pnr"]
            assert pnr_mapping["selector"] == 'input[id="form:txt_pnrCdg"]', "PNR selector should be correct"
            assert "transform" in pnr_mapping, "PNR should have transform function"
            
            self.log_test("LatamForm", True, "Object creation and field mapping tests passed")
            return True
            
        except Exception as e:
            self.log_test("LatamForm", False, f"Error: {e}")
            return False
    
    def test_image_processor(self):
        """Test ImageProcessor"""
        try:
            rules_engine = RulesEngine()
            image_processor = ImageProcessor(rules_engine)
            
            # Test object creation
            assert image_processor.rules_engine is not None, "Rules engine should be set"
            assert image_processor.sabre_ocr is not None, "SabreOCR should be initialized"
            
            # Test supported formats
            assert ".png" in image_processor.supported_formats, "PNG should be supported"
            assert ".jpg" in image_processor.supported_formats, "JPG should be supported"
            
            self.log_test("ImageProcessor", True, "Object creation tests passed")
            return True
            
        except Exception as e:
            self.log_test("ImageProcessor", False, f"Error: {e}")
            return False
    
    def test_status_indicator(self):
        """Test StatusIndicator"""
        try:
            status_indicator = StatusIndicator()
            
            # Test initial state
            assert not status_indicator.is_processing, "Should not be processing initially"
            assert status_indicator.progress == 0, "Progress should be 0 initially"
            
            # Test status setting
            status_indicator.set_status(status_indicator.current_status, "Test message", 50)
            assert status_indicator.progress == 50, "Progress should be updated"
            
            # Test processing state
            status_indicator.start_processing("Test processing")
            assert status_indicator.is_processing, "Should be processing"
            assert status_indicator.current_status.value == "processing", "Status should be processing"
            
            status_indicator.stop_processing(True, "Test completed")
            assert not status_indicator.is_processing, "Should not be processing after stop"
            
            self.log_test("StatusIndicator", True, "All status tests passed")
            return True
            
        except Exception as e:
            self.log_test("StatusIndicator", False, f"Error: {e}")
            return False
    
    def test_overlay_window(self):
        """Test OverlayWindow (without showing)"""
        try:
            overlay = OverlayWindow("Test Window")
            
            # Test object creation
            assert overlay.title == "Test Window", "Title should be set"
            assert not overlay.is_visible, "Window should not be visible initially"
            assert overlay.opacity == 0.9, "Default opacity should be 0.9"
            
            # Test position
            overlay.set_position(100, 200)
            assert overlay.position == (100, 200), "Position should be updated"
            
            # Test opacity
            overlay.set_opacity(0.8)
            assert overlay.opacity == 0.8, "Opacity should be updated"
            
            self.log_test("OverlayWindow", True, "Object creation and property tests passed")
            return True
            
        except Exception as e:
            self.log_test("OverlayWindow", False, f"Error: {e}")
            return False
    
    def test_field_mappings(self):
        """Test field mappings from specification"""
        try:
            rules_engine = RulesEngine()
            latam_form = LatamForm(rules_engine)
            
            # Test all required field mappings from specification.md
            required_fields = [
                'pnr', 'cidade', 'pais', 'departamento', 'razao', 
                'autorizador', 'num_segmento', 'carrier', 'vuelo',
                'classe', 'data_voo', 'segmento', 'pax', 'cto_des'
            ]
            
            for field in required_fields:
                assert field in latam_form.field_mappings, f"Field {field} should be mapped"
                
                mapping = latam_form.field_mappings[field]
                assert "selector" in mapping, f"Field {field} should have selector"
                assert isinstance(mapping["selector"], str), f"Selector for {field} should be string"
            
            # Test specific mappings from specification
            assert latam_form.field_mappings["pnr"]["selector"] == 'input[id="form:txt_pnrCdg"]'
            assert latam_form.field_mappings["carrier"]["selector"] == 'label[id="form:carrierEnabled_label"]'
            assert latam_form.field_mappings["vuelo"]["selector"] == 'input[id="form:txt_vuelotNum"]'
            
            self.log_test("Field Mappings", True, "All field mappings from specification are correct")
            return True
            
        except Exception as e:
            self.log_test("Field Mappings", False, f"Error: {e}")
            return False
    
    def test_business_rules(self):
        """Test business rules from specification"""
        try:
            rules_engine = RulesEngine()
            
            # Test estouro de classe validation
            valid_data = {
                'classe': 'Y',
                'auth_code': 'PIC_S23'
            }
            invalid_data = {
                'classe': 'F',
                'auth_code': 'INVALID'
            }
            
            valid_result = rules_engine.validate_estouro_classe(valid_data)
            invalid_result = rules_engine.validate_estouro_classe(invalid_data)
            
            assert valid_result.is_valid, "Valid estouro de classe should be accepted"
            assert not invalid_result.is_valid, "Invalid estouro de classe should be rejected"
            
            # Test flight status validation
            hk_result = rules_engine.validate_flight_status("HK")
            sa_result = rules_engine.validate_flight_status("SA")
            invalid_status = rules_engine.validate_flight_status("XX")
            
            assert hk_result.is_valid, "HK status should be valid"
            assert sa_result.is_valid, "SA status should be valid"
            assert not invalid_status.is_valid, "Invalid status should be rejected"
            
            self.log_test("Business Rules", True, "All business rule validations passed")
            return True
            
        except Exception as e:
            self.log_test("Business Rules", False, f"Error: {e}")
            return False
    
    def test_name_correction_rules(self):
        """Test name correction rules from correcao_de_nome.txt"""
        try:
            rules_engine = RulesEngine()
            
            # Test type 1: Orthographic correction (max 3 letter differences)
            ortho_result = rules_engine.validate_name_correction("GONSALES", "GONZALEZ")
            assert ortho_result.is_valid, "Orthographic correction should be valid"
            
            # Test type 2: Inverted names
            inverted_result = rules_engine.validate_name_correction("LUISA/GALVEZ", "GALVEZ/LUISA")
            assert inverted_result.is_valid, "Inverted names should be valid"
            
            # Test type 3: Addition without substitution
            addition_result = rules_engine.validate_name_correction("SILVA/ALBERTO", "SILVA/LUIS ALBERTO")
            assert addition_result.is_valid, "Addition correction should be valid"
            
            # Test invalid correction (requires documentation)
            invalid_result = rules_engine.validate_name_correction("MARTINES", "MARTINEZ")
            assert not invalid_result.is_valid, "Invalid correction should require documentation"
            
            self.log_test("Name Correction Rules", True, "All name correction rules passed")
            return True
            
        except Exception as e:
            self.log_test("Name Correction Rules", False, f"Error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("Latam Auto-Filler Test Suite")
        print("=" * 50)
        
        tests = [
            self.test_rules_engine,
            self.test_sabre_screen,
            self.test_latam_form,
            self.test_image_processor,
            self.test_status_indicator,
            self.test_overlay_window,
            self.test_field_mappings,
            self.test_business_rules,
            self.test_name_correction_rules
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                self.log_test(test.__name__, False, f"Unexpected error: {e}")
        
        print("\n" + "=" * 50)
        print(f"Test Results: {passed}/{total} passed")
        
        if passed == total:
            print("✓ All tests passed!")
            return True
        else:
            print("✗ Some tests failed!")
            print("\nFailed tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
            return False
    
    def print_test_summary(self):
        """Print detailed test summary"""
        print("\nDetailed Test Results:")
        print("-" * 50)
        
        for result in self.test_results:
            status = "PASS" if result['success'] else "FAIL"
            print(f"{status:4} | {result['test']:20} | {result['message']}")


def main():
    """Main test function"""
    test_runner = TestRunner()
    
    try:
        success = test_runner.run_all_tests()
        test_runner.print_test_summary()
        
        if success:
            print("\n✓ System validation completed successfully!")
            print("The Latam Auto-Filler implementation is ready for use.")
            return 0
        else:
            print("\n✗ System validation failed!")
            print("Please fix the issues before using the application.")
            return 1
            
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())