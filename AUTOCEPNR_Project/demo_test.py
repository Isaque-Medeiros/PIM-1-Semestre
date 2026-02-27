#!/usr/bin/env python3
"""
Demo Test Script for Latam Auto-Filler
Quick demonstration of the system functionality
"""

import sys
import os
import asyncio
import time
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def test_imports():
    """Test if all modules can be imported"""
    print_section("Testing Module Imports")
    
    modules_to_test = [
        ("Core Modules", [
            "src.core.rules_engine",
            "src.core.sabre_screen", 
            "src.core.latam_form"
        ]),
        ("OCR Modules", [
            "src.ocr.sabre_ocr",
            "src.ocr.image_processor"
        ]),
        ("Automation Modules", [
            "src.automation.browser_manager",
            "src.automation.form_filler"
        ]),
        ("UI Modules", [
            "src.ui.overlay_window",
            "src.ui.status_indicator"
        ])
    ]
    
    all_imports_success = True
    
    for category, modules in modules_to_test:
        print(f"\n{category}:")
        for module in modules:
            try:
                __import__(module)
                print(f"  ✅ {module}")
            except ImportError as e:
                print(f"  ❌ {module} - {e}")
                all_imports_success = False
    
    return all_imports_success

def test_rules_engine():
    """Test Rules Engine functionality"""
    print_section("Testing Rules Engine")
    
    try:
        from src.core.rules_engine import RulesEngine
        
        rules = RulesEngine()
        
        # Test PNR validation
        pnr_valid = rules.validate_pnr_format("ABC123")
        pnr_invalid = rules.validate_pnr_format("INVALID")
        
        print(f"  PNR Validation:")
        print(f"    Valid PNR (ABC123): {'✅' if pnr_valid.is_valid else '❌'}")
        print(f"    Invalid PNR (INVALID): {'✅' if not pnr_invalid.is_valid else '❌'}")
        
        # Test date validation
        date_valid, date_formatted = rules.validate_date_format("13MAR")
        print(f"  Date Validation:")
        print(f"    Valid Date (13MAR): {'✅' if date_valid else '❌'} -> {date_formatted}")
        
        # Test carrier validation
        carrier_valid = rules.validate_carrier_code("LA")
        carrier_invalid = rules.validate_carrier_code("XX")
        
        print(f"  Carrier Validation:")
        print(f"    Valid Carrier (LA): {'✅' if carrier_valid.is_valid else '❌'}")
        print(f"    Invalid Carrier (XX): {'✅' if not carrier_invalid.is_valid else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_field_mappings():
    """Test field mappings from specification"""
    print_section("Testing Field Mappings")
    
    try:
        from src.core.latam_form import LatamForm
        from src.core.rules_engine import RulesEngine
        
        rules = RulesEngine()
        latam_form = LatamForm(rules)
        
        # Required fields from specification
        required_fields = [
            'pnr', 'cidade', 'pais', 'departamento', 'razao',
            'autorizador', 'num_segmento', 'carrier', 'vuelo',
            'classe', 'data_voo', 'segmento', 'pax', 'cto_des'
        ]
        
        print(f"  Field Mappings:")
        all_mapped = True
        for field in required_fields:
            if field in latam_form.field_mappings:
                selector = latam_form.field_mappings[field]['selector']
                print(f"    ✅ {field}: {selector}")
            else:
                print(f"    ❌ {field}: Not mapped")
                all_mapped = False
        
        # Test specific mappings
        pnr_selector = latam_form.field_mappings['pnr']['selector']
        expected_pnr = 'input[id="form:txt_pnrCdg"]'
        
        print(f"\n  Specification Compliance:")
        print(f"    PNR Selector: {'✅' if pnr_selector == expected_pnr else '❌'}")
        print(f"      Expected: {expected_pnr}")
        print(f"      Actual:   {pnr_selector}")
        
        return all_mapped
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_ui_components():
    """Test UI components"""
    print_section("Testing UI Components")
    
    try:
        from src.ui.overlay_window import OverlayWindow
        from src.ui.status_indicator import StatusIndicator
        
        # Test Overlay Window
        overlay = OverlayWindow("Test")
        print(f"  Overlay Window:")
        print(f"    Title: {'✅' if overlay.title == 'Test' else '❌'}")
        print(f"    Not visible initially: {'✅' if not overlay.is_visible else '❌'}")
        print(f"    Default opacity: {'✅' if overlay.opacity == 0.9 else '❌'}")
        
        # Test Status Indicator
        status = StatusIndicator()
        print(f"\n  Status Indicator:")
        print(f"    Not processing initially: {'✅' if not status.is_processing else '❌'}")
        print(f"    Progress 0 initially: {'✅' if status.progress == 0 else '❌'}")
        
        # Test status operations
        status.start_processing("Test")
        processing_started = status.is_processing
        status.stop_processing(True, "Test completed")
        processing_stopped = not status.is_processing
        
        print(f"    Start processing: {'✅' if processing_started else '❌'}")
        print(f"    Stop processing: {'✅' if processing_stopped else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_business_rules():
    """Test business rules"""
    print_section("Testing Business Rules")
    
    try:
        from src.core.rules_engine import RulesEngine
        
        rules = RulesEngine()
        
        # Test PIC authorization
        pic_valid = rules._validate_pic_authorization("PIC_S23")
        pic_invalid = rules._validate_pic_authorization("INVALID")
        
        print(f"  PIC Authorization:")
        print(f"    Valid PIC (PIC_S23): {'✅' if pic_valid else '❌'}")
        print(f"    Invalid PIC (INVALID): {'✅' if not pic_invalid else '❌'}")
        
        # Test class restrictions
        valid_classes = ['Q', 'S', 'Y']
        invalid_classes = ['F', 'J', 'W']
        
        print(f"\n  Class Restrictions:")
        all_valid_classes = True
        for cls in valid_classes:
            result = rules.validate_estouro_classe({'classe': cls, 'auth_code': 'PIC_S23'})
            print(f"    Class {cls}: {'✅' if result.is_valid else '❌'}")
            if not result.is_valid:
                all_valid_classes = False
        
        all_invalid_classes = True
        for cls in invalid_classes:
            result = rules.validate_estouro_classe({'classe': cls, 'auth_code': 'PIC_S23'})
            print(f"    Class {cls}: {'✅' if not result.is_valid else '❌'}")
            if result.is_valid:
                all_invalid_classes = False
        
        # Test flight status
        valid_statuses = ['HK', 'SA']
        invalid_statuses = ['XX', 'YY']
        
        print(f"\n  Flight Status:")
        all_valid_statuses = True
        for status in valid_statuses:
            result = rules.validate_flight_status(status)
            print(f"    Status {status}: {'✅' if result.is_valid else '❌'}")
            if not result.is_valid:
                all_valid_statuses = False
        
        all_invalid_statuses = True
        for status in invalid_statuses:
            result = rules.validate_flight_status(status)
            print(f"    Status {status}: {'✅' if not result.is_valid else '❌'}")
            if result.is_valid:
                all_invalid_statuses = False
        
        return all_valid_classes and all_invalid_classes and all_valid_statuses and all_invalid_statuses
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_name_correction():
    """Test name correction rules"""
    print_section("Testing Name Correction Rules")
    
    try:
        from src.core.rules_engine import RulesEngine
        
        rules = RulesEngine()
        
        # Test orthographic correction
        ortho_tests = [
            ("GONSALES", "GONZALEZ", True),
            ("SILVA", "SILBA", True),
        ]
        
        print(f"  Orthographic Correction:")
        all_ortho_valid = True
        for old_name, new_name, should_be_valid in ortho_tests:
            result = rules.validate_name_correction(old_name, new_name)
            is_valid = result.is_valid == should_be_valid
            print(f"    {old_name} -> {new_name}: {'✅' if is_valid else '❌'}")
            if not is_valid:
                all_ortho_valid = False
        
        # Test inverted names
        inverted_result = rules.validate_name_correction("LUISA/GALVEZ", "GALVEZ/LUISA")
        print(f"\n  Inverted Names:")
        print(f"    LUISA/GALVEZ -> GALVEZ/LUISA: {'✅' if inverted_result.is_valid else '❌'}")
        
        # Test addition without substitution
        addition_result = rules.validate_name_correction("SILVA/ALBERTO", "SILVA/LUIS ALBERTO")
        print(f"    SILVA/ALBERTO -> SILVA/LUIS ALBERTO: {'✅' if addition_result.is_valid else '❌'}")
        
        return all_ortho_valid and inverted_result.is_valid and addition_result.is_valid
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def show_project_structure():
    """Show project structure"""
    print_section("Project Structure")
    
    structure = """
📁 AUTOCEPNR_Project/
├── 📄 main.py                    # Main application entry point
├── 📄 requirements.txt           # Python dependencies
├── 📄 setup.py                   # Installation script
├── 📄 test_system.py             # Basic test suite
├── 📄 test_comprehensive.py      # Comprehensive test suite
├── 📄 build_executable.py        # PyInstaller build script
├── 📄 README.md                  # User documentation
├── 📄 TROUBLESHOOTING.md         # Troubleshooting guide
├── 📁 docs/                      # Specification and documentation
│   └── 📄 specification.md       # Detailed system specification
├── 📁 rules/                     # Business rules and mappings
│   ├── 📄 sabre_mapping.json     # Field mapping configuration
│   └── 📄 correcao_de_nome.txt   # Name correction rules
├── 📁 src/                       # Source code
│   ├── 📁 core/                  # Core business logic
│   │   ├── 🔧 rules_engine.py    # Business rules validation
│   │   ├── 🖼️ sabre_screen.py    # Sabre screen processing
│   │   └── 🤖 latam_form.py      # Browser automation
│   ├── 📁 ocr/                   # OCR processing
│   │   ├── 🖼️ sabre_ocr.py       # EasyOCR integration
│   │   └── 🖼️ image_processor.py # Image input handling
│   ├── 📁 automation/            # Automation layer
│   │   ├── 🤖 browser_manager.py # Browser management
│   │   └── 🤖 form_filler.py     # Form filling workflow
│   └── 📁 ui/                    # User interface
│       ├── 🎨 overlay_window.py  # Transparent overlay
│       └── 📊 status_indicator.py # Status tracking
└── 📁 FotosProjeto/              # Project images
    └── 📷 EspecificacaoInicial.png
"""
    
    print(structure)

def main():
    """Main demo function"""
    print_header("Latam Auto-Filler - Demo Test")
    print("🚀 Quick demonstration of the complete system")
    
    # Show project structure
    show_project_structure()
    
    # Run tests
    tests = [
        ("Module Imports", test_imports),
        ("Rules Engine", test_rules_engine),
        ("Field Mappings", test_field_mappings),
        ("UI Components", test_ui_components),
        ("Business Rules", test_business_rules),
        ("Name Correction", test_name_correction),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"\n❌ {test_name} failed with error: {e}")
            results[test_name] = False
    
    # Show summary
    print_header("Demo Test Summary")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"\n📊 Test Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} | {test_name}")
    
    print(f"\n🎯 Overall Status: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All demo tests passed!")
        print("✅ The Latam Auto-Filler system is ready for use!")
        print("\n📋 Next Steps:")
        print("  1. Run: python setup.py (install dependencies)")
        print("  2. Run: python main.py (start the application)")
        print("  3. Test with: python test_comprehensive.py (full test suite)")
        print("  4. Build executable: python build_executable.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed!")
        print("Please check the errors above and fix any issues.")
    
    print_header("Demo Complete")

if __name__ == "__main__":
    main()