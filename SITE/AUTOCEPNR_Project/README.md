# Latam Auto-Filler

**Spec-Driven Development Implementation**  
Automated form filling system for Latam "Estouro de Classe" requests from Sabre Interact v2.1 screens.

## 🎯 Overview

The Latam Auto-Filler is a Windows standalone application that automates the process of filling Latam's "Estouro de Classe" forms using data extracted from Sabre Interact v2.1 screens via OCR technology.

### Key Features

- **📋 Spec-Driven Development**: Built according to detailed specification.md requirements
- **👁️ OCR Processing**: EasyOCR integration for Sabre font detection
- **🤖 Browser Automation**: Playwright for Chrome/Edge form filling
- **🎨 Transparent UI**: Always-on-top overlay for user feedback
- **✅ Business Rules**: Comprehensive validation engine
- **🔄 Human-like Delays**: 200ms delays between field fills to avoid detection

## 📋 System Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.11 or higher
- **Credit**: 0.3419 (as specified)
- **Browser**: Chrome or Edge (for automation)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd AUTOCEPNR_Project

# Run setup (installs dependencies and configures environment)
python setup.py

# Or manual installation:
pip install -r requirements.txt
python -m playwright install
```

### 2. Basic Usage

```bash
# Start with UI (recommended)
python main.py

# Start without UI
python main.py --no-ui

# Process specific image
python main.py --image path/to/sabre_screenshot.png

# Process from clipboard (CTRL+V)
python main.py --clipboard

# Test mode
python main.py --test
```

### 3. Testing

```bash
# Run comprehensive test suite
python test_system.py

# Test installation only
python setup.py --test-only
```

## 🏗️ Architecture

The system follows a modular 4-layer architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                   │
├─────────────────────────────────────────────────────────┤
│  Overlay Window  │  Status Indicator  │  Main Application │
├─────────────────────────────────────────────────────────┤
│                  Automation Layer                        │
├─────────────────────────────────────────────────────────┤
│  Browser Manager  │  Form Filler  │  Image Processor     │
├─────────────────────────────────────────────────────────┤
│                    Core Logic Layer                      │
├─────────────────────────────────────────────────────────┤
│  Rules Engine  │  SabreScreen  │  LatamForm  │  OCR      │
├─────────────────────────────────────────────────────────┤
│                   Configuration                        │
├─────────────────────────────────────────────────────────┤
│  Sabre Mapping  │  Name Correction  │  Business Rules    │
└─────────────────────────────────────────────────────────┘
```

### Core Modules

#### 🔧 **Core Module** (`src/core/`)
- **RulesEngine**: Business logic validation and PIC rules
- **SabreScreen**: Sabre screen capture and field extraction
- **LatamForm**: Browser automation and form filling

#### 🖼️ **OCR Module** (`src/ocr/`)
- **SabreOCR**: EasyOCR integration for Sabre fonts
- **ImageProcessor**: Image input handling (clipboard/file)

#### 🤖 **Automation Module** (`src/automation/`)
- **BrowserManager**: Playwright browser management
- **FormFiller**: Complete workflow orchestration

#### 🎨 **UI Module** (`src/ui/`)
- **OverlayWindow**: Transparent feedback interface
- **StatusIndicator**: Status tracking and notifications

## 📄 Specification Compliance

The implementation strictly follows the `docs/specification.md` requirements:

### ✅ Field Mappings (13/13)
All fields from Sabre to Latam form are implemented:

| Sabre Field | Latam Field | Status |
|-------------|-------------|--------|
| Código de PNR | form:txt_pnrCdg | ✅ |
| Ciudad | form:ciudadPrioridadNombreCiudad_input | ✅ |
| País | form:ciudadPrioridadNombrePais | ✅ |
| Depto | form:departamentos_label | ✅ |
| Razón | form:razonEnabled_label | ✅ |
| Autorizador | form:authorizerEnabled_label | ✅ |
| Núm. Segmento | form:txt_segmentNum | ✅ |
| Carrier | form:carrierEnabled_label | ✅ |
| Vuelo | form:txt_vuelotNum | ✅ |
| Clase | form:classEnabled_label | ✅ |
| Fecha de Vuelo | form:dateFlight_input | ✅ |
| Segmento | form:txt_segment | ✅ |
| Pax | form:pax_paxID_label | ✅ |
| Cto Des. | form:txt_ctoDes | ✅ |

### ✅ Business Rules
- **PIC Authorization**: Validates PIC_S23, PIC_S24, PIC_S25 codes
- **Class Restrictions**: Only Q, S, Y classes eligible for upgrade
- **Flight Status**: Only HK or SA status allowed
- **Name Corrections**: 7 types of corrections from correcao_de_nome.txt

### ✅ OCR Requirements
- **Input Methods**: CTRL+V clipboard and file upload
- **Font Detection**: Monospace font optimization for Sabre
- **Format Validation**: Detects Sabre Interact v2.1 patterns
- **Confidence Scoring**: Field-level confidence tracking

### ✅ Automation Requirements
- **Browser Support**: Chrome/Edge via Playwright
- **Human Delays**: 200ms between field fills
- **Tab Management**: Automatic Latam form detection
- **Error Handling**: Comprehensive validation and retry logic

## 🔧 Configuration

### Field Mappings
Located in `rules/sabre_mapping.json`:

```json
{
  "reserva_info": {
    "pnr": {
      "sabre_label": "Reserva - ",
      "form_selector": "input[id='form:txt_pnrCdg']",
      "regex": "Reserva - ([A-Z0-9]{6})"
    }
  }
}
```

### Name Correction Rules
Located in `rules/correcao_de_nome.txt`:

- **Type 1**: Orthographic (max 3 letter differences)
- **Type 2**: Inverted names
- **Type 3**: Addition without substitution
- **Type 4**: Duplication removal
- **Type 5**: Agname (JR, Neto, Filho)
- **Type 6**: Legal changes (requires documentation)
- **Type 7**: Other (requires documentation)

## 🧪 Testing

The system includes comprehensive testing:

```bash
# Run all tests
python test_system.py

# Expected output:
# Latam Auto-Filler Test Suite
# ==========================================
# Test Results: 9/9 passed
# ✓ All tests passed!
```

### Test Coverage
- ✅ Rules Engine validation
- ✅ SabreScreen object creation
- ✅ LatamForm field mappings
- ✅ ImageProcessor functionality
- ✅ StatusIndicator operations
- ✅ OverlayWindow properties
- ✅ Field mappings from specification
- ✅ Business rules validation
- ✅ Name correction rules

## 📊 Usage Examples

### Processing from Clipboard
1. Take screenshot of Sabre Interact v2.1 screen
2. Copy to clipboard (CTRL+C)
3. Run: `python main.py --clipboard`
4. System extracts text and fills form automatically

### Processing from File
```bash
python main.py --image "C:/screenshots/sabre_20260227.png"
```

### Programmatic Usage
```python
from main import LatamAutoFiller

app = LatamAutoFiller()
await app.initialize()

# Process image
result = await app.process_image("clipboard")

# Fill form
if result["success"]:
    form_result = await app.fill_form(result["fields"])
```

## 🐛 Troubleshooting

### Common Issues

**OCR Not Working**
- Ensure EasyOCR models are downloaded
- Check image quality (minimum 800x600 resolution)
- Verify Sabre screen format detection

**Browser Automation Fails**
- Ensure Chrome/Edge is installed
- Check Playwright browser installation
- Verify Latam form URL accessibility

**Field Validation Errors**
- Check Sabre screen contains all required fields
- Verify PNR format (6 alphanumeric characters)
- Confirm flight status is HK or SA

### Logs
Check `latam_autofiller.log` for detailed error information.

## 🔒 Security Notes

- **Offline Operation**: No external network requests (except VPN for Latam access)
- **Local Processing**: All OCR and validation happens locally
- **No Data Storage**: Temporary processing only
- **Credit Usage**: Optimized for minimal credit consumption

## 🤝 Contributing

1. Follow Spec-Driven Development methodology
2. Update `docs/specification.md` for new features
3. Add corresponding tests in `test_system.py`
4. Maintain backward compatibility
5. Update this README for user-facing changes

## 📄 License

This project is licensed under the terms specified in the project documentation.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review test results with `python test_system.py`
3. Examine logs in `latam_autofiller.log`
4. Verify specification compliance in `docs/specification.md`

---

**Built with ❤️ using Spec-Driven Development**