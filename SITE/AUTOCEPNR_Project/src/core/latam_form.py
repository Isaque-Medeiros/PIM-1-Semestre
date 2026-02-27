"""
LatamForm Object
Handles browser automation and form filling for Latam Estouro de Classe form
"""

import asyncio
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import json

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from .rules_engine import RulesEngine, ValidationResult


@dataclass
class FormField:
    """Represents a form field with its selector and value"""
    name: str
    selector: str
    value: str
    field_type: str = "input"  # input, select, label
    delay: float = 0.2  # 200ms delay as specified


class LatamForm:
    """Object representing the Latam Estouro de Classe form and browser automation"""
    
    def __init__(self, rules_engine: RulesEngine, browser_type: str = "chromium"):
        """
        Initialize LatamForm with rules engine and browser type
        
        Args:
            rules_engine: RulesEngine instance for validation
            browser_type: Browser type (chromium, firefox, webkit)
        """
        self.rules_engine = rules_engine
        self.browser_type = browser_type
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.is_form_loaded: bool = False
        self.form_url: Optional[str] = None
        
        # Field mappings from specification.md
        self.field_mappings = {
            'pnr': {
                'selector': 'input[id="form:txt_pnrCdg"]',
                'transform': lambda x: x.upper()
            },
            'cidade': {
                'selector': 'input[id="form:ciudadPrioridadNombreCiudad_input"]',
                'transform': lambda x: x
            },
            'pais': {
                'selector': 'input[id="form:ciudadPrioridadNombrePais"]',
                'read_only': True
            },
            'departamento': {
                'selector': 'label[id="form:departamentos_label"]',
                'type': 'select'
            },
            'razao': {
                'selector': 'label[id="form:razonEnabled_label"]',
                'type': 'select'
            },
            'autorizador': {
                'selector': 'label[id="form:authorizerEnabled_label"]',
                'type': 'select'
            },
            'num_segmento': {
                'selector': 'input[id="form:txt_segmentNum"]',
                'transform': lambda x: str(x)
            },
            'carrier': {
                'selector': 'label[id="form:carrierEnabled_label"]',
                'type': 'select'
            },
            'vuelo': {
                'selector': 'input[id="form:txt_vuelotNum"]',
                'transform': lambda x: re.sub(r'[^\d]', '', str(x))[:4]
            },
            'classe': {
                'selector': 'label[id="form:classEnabled_label"]',
                'type': 'select'
            },
            'data_voo': {
                'selector': 'input[id="form:dateFlight_input"]',
                'transform': self._format_date_brazilian
            },
            'segmento': {
                'selector': 'input[id="form:txt_segment"]',
                'transform': lambda x: x.replace('-', '/')
            },
            'pax': {
                'selector': 'label[id="form:pax_paxID_label"]',
                'type': 'select'
            },
            'cto_des': {
                'selector': 'input[id="form:txt_ctoDes"]',
                'transform': lambda x: x
            }
        }
    
    async def initialize_browser(self) -> bool:
        """
        Initialize browser and create context
        
        Returns:
            True if browser initialized successfully, False otherwise
        """
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright[self.browser_type].launch(headless=False)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            return True
        except Exception as e:
            print(f"Error initializing browser: {e}")
            return False
    
    async def focus_active_tab(self) -> bool:
        """
        Focus on the active browser tab (Chrome/Edge)
        
        Returns:
            True if tab focused successfully, False otherwise
        """
        try:
            if self.page is None:
                return False
            
            # Check if page is already loaded and focused
            if self.page.url and "latam" in self.page.url.lower():
                self.form_url = self.page.url
                self.is_form_loaded = await self._check_form_loaded()
                return True
            
            # Try to find Latam form in existing tabs
            pages = self.context.pages
            for page in pages:
                if page.url and "latam" in page.url.lower():
                    self.page = page
                    self.form_url = page.url
                    self.is_form_loaded = await self._check_form_loaded()
                    return True
            
            return False
        except Exception as e:
            print(f"Error focusing tab: {e}")
            return False
    
    async def _check_form_loaded(self) -> bool:
        """
        Check if the Latam form is loaded and ready
        
        Returns:
            True if form is loaded, False otherwise
        """
        try:
            if self.page is None:
                return False
            
            # Check for form elements
            pnr_field = await self.page.query_selector('input[id="form:txt_pnrCdg"]')
            return pnr_field is not None
        except Exception as e:
            print(f"Error checking form loaded: {e}")
            return False
    
    async def fill_all(self, extracted_data: Dict[str, str]) -> List[ValidationResult]:
        """
        Fill all form fields with extracted data
        
        Args:
            extracted_data: Dictionary of extracted Sabre data
            
        Returns:
            List of validation results
        """
        if not self.is_form_loaded:
            return [ValidationResult(False, "Formulário não carregado", "Focar no formulário Latam")]
        
        results = []
        
        try:
            # Fill each field according to mapping
            for field_name, field_config in self.field_mappings.items():
                if field_name in extracted_data:
                    result = await self._fill_field(field_name, extracted_data[field_name], field_config)
                    results.append(result)
                    
                    # Human-like delay between fields (200ms as specified)
                    await asyncio.sleep(0.2)
            
            return results
            
        except Exception as e:
            print(f"Error filling form: {e}")
            return [ValidationResult(False, f"Erro ao preencher formulário: {e}", "Verificar conexão e formulário")]
    
    async def _fill_field(self, field_name: str, value: str, field_config: Dict) -> ValidationResult:
        """
        Fill a specific field with value
        
        Args:
            field_name: Name of the field
            value: Value to fill
            field_config: Field configuration from mapping
            
        Returns:
            ValidationResult of the fill operation
        """
        try:
            selector = field_config['selector']
            
            # Apply transformations if specified
            if 'transform' in field_config:
                value = field_config['transform'](value)
            
            # Handle different field types
            if field_config.get('type') == 'select' or 'label' in selector:
                # For select/label elements, click and select
                await self.page.click(selector)
                await self.page.wait_for_timeout(100)  # Small delay after click
                
                # Type the value to select it
                await self.page.keyboard.type(value)
                await self.page.keyboard.press('Enter')
                
            elif field_config.get('read_only'):
                # For read-only fields, just validate they're filled
                element = await self.page.query_selector(selector)
                if element:
                    current_value = await element.get_attribute('value') or await element.inner_text()
                    if not current_value or current_value.strip() == "":
                        return ValidationResult(False, f"Campo {field_name} não preenchido", "Verificar preenchimento automático")
            
            else:
                # For input fields, clear and type
                await self.page.fill(selector, "")
                await self.page.type(selector, value, delay=50)  # 50ms delay between keystrokes
            
            return ValidationResult(True)
            
        except Exception as e:
            return ValidationResult(False, f"Erro ao preencher campo {field_name}: {e}", "Verificar se o campo está visível")
    
    def _format_date_brazilian(self, date_str: str) -> str:
        """
        Format date from Sabre format to Brazilian format
        
        Args:
            date_str: Date string from Sabre (e.g., "13MAR")
            
        Returns:
            Formatted date string (e.g., "13/03/2026")
        """
        is_valid, formatted_date = self.rules_engine.validate_date_format(date_str)
        return formatted_date if is_valid else date_str
    
    async def submit_form(self) -> ValidationResult:
        """
        Submit the filled form
        
        Returns:
            ValidationResult of submission
        """
        try:
            if not self.is_form_loaded:
                return ValidationResult(False, "Formulário não carregado", "Focar no formulário Latam")
            
            # Look for submit button
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Enviar")',
                'button:has-text("Submit")',
                '#submit',
                '.submit'
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = await self.page.query_selector(selector)
                    if submit_button:
                        break
                except:
                    continue
            
            if submit_button:
                await self.page.click(submit_button)
                await self.page.wait_for_timeout(1000)  # Wait for submission
                
                # Check for success indicators
                success_indicators = [
                    'text="Sucesso"',
                    'text="Success"',
                    'text="Formulário enviado"',
                    '.success',
                    '.confirmation'
                ]
                
                for indicator in success_indicators:
                    try:
                        if await self.page.query_selector(indicator):
                            return ValidationResult(True)
                    except:
                        continue
                
                return ValidationResult(True, "Formulário submetido (verificar confirmação manualmente)")
            else:
                return ValidationResult(False, "Botão de envio não encontrado", "Verificar se o formulário está completo")
                
        except Exception as e:
            return ValidationResult(False, f"Erro ao submeter formulário: {e}", "Verificar conexão e formulário")
    
    async def get_form_status(self) -> Dict[str, Any]:
        """
        Get current form status and field values
        
        Returns:
            Dictionary with form status information
        """
        try:
            if self.page is None:
                return {"status": "browser_not_initialized"}
            
            if not self.is_form_loaded:
                return {"status": "form_not_loaded"}
            
            # Check field values
            field_values = {}
            for field_name, field_config in self.field_mappings.items():
                try:
                    selector = field_config['selector']
                    element = await self.page.query_selector(selector)
                    if element:
                        value = await element.get_attribute('value') or await element.inner_text()
                        field_values[field_name] = value.strip() if value else ""
                except:
                    field_values[field_name] = None
            
            return {
                "status": "form_loaded",
                "url": self.page.url,
                "fields": field_values,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def close(self):
        """Close browser and cleanup"""
        try:
            if self.browser:
                await self.browser.close()
        except:
            pass