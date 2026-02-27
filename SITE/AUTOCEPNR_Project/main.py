"""
Main Application Entry Point
Latam Auto-Filler - Spec-Driven Development Implementation
"""

import asyncio
import sys
import os
import logging
import argparse
import signal
from typing import Optional, Dict, Any
import threading
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.rules_engine import RulesEngine
from src.core.sabre_screen import SabreScreen
from src.core.latam_form import LatamForm
from src.ocr.image_processor import ImageProcessor
from src.automation.browser_manager import BrowserManager
from src.automation.form_filler import FormFiller
from src.ui.overlay_window import OverlayWindow
from src.ui.status_indicator import StatusIndicator


class LatamAutoFiller:
    """Main application class for Latam Auto-Filler"""
    
    def __init__(self):
        """Initialize the application"""
        self.logger = self._setup_logging()
        self.logger.info("Initializing Latam Auto-Filler...")
        
        # Core components
        self.rules_engine = RulesEngine()
        self.sabre_screen = SabreScreen(self.rules_engine)
        self.latam_form = LatamForm(self.rules_engine)
        self.image_processor = ImageProcessor(self.rules_engine)
        self.browser_manager = BrowserManager(self.rules_engine)
        self.form_filler = FormFiller(self.rules_engine)
        
        # UI components
        self.overlay_window = OverlayWindow("Latam Auto-Filler")
        self.status_indicator = StatusIndicator()
        
        # Application state
        self.is_running = False
        self.is_processing = False
        self.processing_task = None
        
        # Configuration
        self.config = {
            'auto_start_browser': True,
            'auto_focus_form': True,
            'enable_ui': True,
            'ocr_timeout': 30,
            'form_timeout': 60,
            'human_delay': 0.2
        }
        
        # Setup callbacks
        self._setup_callbacks()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('latam_autofiller.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger(__name__)
    
    def _setup_callbacks(self):
        """Setup callback functions between components"""
        # Status indicator callbacks
        self.status_indicator.set_status_callback(self._on_status_change)
        self.status_indicator.set_progress_callback(self._on_progress_change)
        self.status_indicator.set_notification_callback(self._on_notification)
        
        # Overlay window callbacks
        self.overlay_window.set_update_callback(self._on_ui_action)
    
    def _on_status_change(self, status, message):
        """Handle status changes"""
        self.logger.info(f"Status changed: {status.value} - {message}")
        if self.overlay_window.is_running():
            self.overlay_window.update_status(message)
    
    def _on_progress_change(self, progress):
        """Handle progress changes"""
        self.logger.debug(f"Progress: {progress}%")
        if self.overlay_window.is_running():
            self.overlay_window.update_progress(progress)
    
    def _on_notification(self, message, level):
        """Handle notifications"""
        self.logger.info(f"Notification: {message}")
        if self.overlay_window.is_running():
            self.overlay_window.add_log_entry(message, level.value)
    
    def _on_ui_action(self, action):
        """Handle UI button actions"""
        self.logger.info(f"UI action: {action}")
        
        if action == 'start':
            self.start_processing()
        elif action == 'stop':
            self.stop_processing()
        elif action == 'clear':
            self.clear_status()
    
    async def initialize(self) -> bool:
        """
        Initialize all components
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing components...")
            
            # Initialize browser if needed
            if self.config['auto_start_browser']:
                browser_success = await self.browser_manager.initialize()
                if not browser_success:
                    self.logger.warning("Browser initialization failed, continuing without automation")
            
            # Focus on Latam form if needed
            if self.config['auto_focus_form']:
                latam_form = await self.browser_manager.focus_latam_tab()
                if latam_form:
                    self.latam_form = latam_form
                    self.form_filler.initialize_components(self.latam_form)
                    self.logger.info("Latam form focused successfully")
                else:
                    self.logger.warning("No Latam form found, automation will be limited")
            
            # Initialize OCR
            ocr_success = self.image_processor.sabre_ocr.initialize()
            if not ocr_success:
                self.logger.error("OCR initialization failed")
                return False
            
            self.logger.info("Components initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during initialization: {e}")
            return False
    
    def start_processing(self):
        """Start processing workflow"""
        if self.is_processing:
            self.logger.warning("Already processing")
            return
        
        self.is_processing = True
        self.status_indicator.start_processing("Iniciando processamento...")
        
        # Run processing in background thread
        processing_thread = threading.Thread(target=self._run_processing)
        processing_thread.daemon = True
        processing_thread.start()
    
    def _run_processing(self):
        """Run the processing workflow"""
        try:
            # Process complete workflow
            result = asyncio.run(self.form_filler.process_complete_workflow())
            
            # Handle result
            if result.success:
                self.status_indicator.stop_processing(True, "Processamento concluído com sucesso!")
                self.logger.info("Workflow completed successfully")
            else:
                error_msg = result.error_message or "Erro desconhecido"
                self.status_indicator.stop_processing(False, f"Processamento falhou: {error_msg}")
                self.logger.error(f"Workflow failed: {error_msg}")
                
        except Exception as e:
            self.status_indicator.stop_processing(False, f"Erro durante processamento: {str(e)}")
            self.logger.error(f"Processing error: {e}")
        finally:
            self.is_processing = False
    
    def stop_processing(self):
        """Stop processing workflow"""
        self.is_processing = False
        self.status_indicator.set_processing(False)
        self.logger.info("Processing stopped by user")
    
    def clear_status(self):
        """Clear status and logs"""
        self.status_indicator.reset()
        if self.overlay_window.is_running():
            self.overlay_window.clear_status()
        self.logger.info("Status cleared")
    
    async def process_image(self, image_source: Any = None) -> Dict[str, Any]:
        """
        Process a single image
        
        Args:
            image_source: Image source (clipboard, file path, or numpy array)
            
        Returns:
            Processing result
        """
        try:
            self.status_indicator.start_processing("Processando imagem...")
            
            # Process image
            image, extracted_text = self.image_processor.process_image_input(image_source)
            
            if not extracted_text:
                self.status_indicator.stop_processing(False, "Nenhum texto extraído da imagem")
                return {"success": False, "error": "No text extracted"}
            
            # Create SabreScreen and parse fields
            self.sabre_screen.raw_image = image
            self.sabre_screen.extracted_text = extracted_text
            self.sabre_screen.is_valid_screen = self.sabre_screen.detect_sabre_pattern()
            
            if not self.sabre_screen.is_valid_screen:
                self.status_indicator.stop_processing(False, "Formato de tela Sabre inválido")
                return {"success": False, "error": "Invalid Sabre format"}
            
            extracted_fields = self.sabre_screen.parse_fields()
            validation_results = self.sabre_screen.validate_integrity()
            
            # Check for critical failures
            critical_failures = [r for r in validation_results if not r.is_valid]
            if critical_failures:
                self.status_indicator.stop_processing(False, f"Falhas críticas: {len(critical_failures)}")
                return {"success": False, "error": "Critical validation failures", "failures": critical_failures}
            
            self.status_indicator.stop_processing(True, "Imagem processada com sucesso!")
            
            return {
                "success": True,
                "extracted_text": extracted_text,
                "fields": {name: field.value for name, field in extracted_fields.items()},
                "validation_results": validation_results
            }
            
        except Exception as e:
            self.status_indicator.stop_processing(False, f"Erro ao processar imagem: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def fill_form(self, extracted_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Fill Latam form with extracted data
        
        Args:
            extracted_data: Extracted data from Sabre screen
            
        Returns:
            Form filling result
        """
        try:
            if not self.latam_form or not self.latam_form.is_form_loaded:
                return {"success": False, "error": "Latam form not loaded"}
            
            self.status_indicator.start_processing("Preenchendo formulário...")
            
            # Fill form
            fill_results = await self.latam_form.fill_all(extracted_data)
            submission_result = await self.latam_form.submit_form()
            
            success = all(r.is_valid for r in fill_results) and submission_result.is_valid
            
            if success:
                self.status_indicator.stop_processing(True, "Formulário preenchido com sucesso!")
            else:
                self.status_indicator.stop_processing(False, "Falha ao preencher formulário")
            
            return {
                "success": success,
                "field_results": fill_results,
                "submission_result": submission_result
            }
            
        except Exception as e:
            self.status_indicator.stop_processing(False, f"Erro ao preencher formulário: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def show_ui(self):
        """Show the overlay UI"""
        if self.config['enable_ui']:
            self.overlay_window.create_window()
            self.overlay_window.show()
    
    def hide_ui(self):
        """Hide the overlay UI"""
        if self.overlay_window.is_running():
            self.overlay_window.hide()
    
    def run(self, show_ui: bool = True):
        """
        Run the main application
        
        Args:
            show_ui: Whether to show the UI
        """
        try:
            self.logger.info("Starting Latam Auto-Filler application...")
            self.is_running = True
            
            # Initialize components
            init_success = asyncio.run(self.initialize())
            if not init_success:
                self.logger.error("Failed to initialize components")
                return
            
            # Show UI if requested
            if show_ui:
                self.show_ui()
                self.logger.info("UI started")
            
            # Run main loop
            self._main_loop()
            
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
        except Exception as e:
            self.logger.error(f"Application error: {e}")
        finally:
            self.cleanup()
    
    def _main_loop(self):
        """Main application loop"""
        try:
            while self.is_running:
                # Update status periodically
                if self.overlay_window.is_running():
                    status_info = self.status_indicator.get_status_info()
                    self.overlay_window.update_status(status_info['message'])
                
                time.sleep(1)
                
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.logger.info("Cleaning up resources...")
            
            # Stop processing
            self.is_processing = False
            
            # Cleanup browser
            if self.browser_manager:
                asyncio.run(self.browser_manager.cleanup())
            
            # Hide UI
            if self.overlay_window.is_running():
                self.overlay_window.destroy()
            
            self.is_running = False
            self.logger.info("Cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def export_report(self) -> Dict[str, Any]:
        """Export application report"""
        return {
            "application_info": {
                "name": "Latam Auto-Filler",
                "version": "1.0.0",
                "status": "running" if self.is_running else "stopped",
                "processing": self.is_processing
            },
            "components": {
                "rules_engine": "initialized",
                "sabre_screen": "initialized", 
                "latam_form": "initialized",
                "image_processor": "initialized",
                "browser_manager": "initialized",
                "form_filler": "initialized"
            },
            "status": self.status_indicator.export_status_report(),
            "config": self.config
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Latam Auto-Filler - Spec-Driven Development Implementation")
    parser.add_argument('--no-ui', action='store_true', help='Run without UI')
    parser.add_argument('--image', type=str, help='Process specific image file')
    parser.add_argument('--clipboard', action='store_true', help='Process image from clipboard')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    
    args = parser.parse_args()
    
    # Create application
    app = LatamAutoFiller()
    
    try:
        if args.image:
            # Process specific image
            result = asyncio.run(app.process_image(args.image))
            print(f"Image processing result: {result}")
            
        elif args.clipboard:
            # Process from clipboard
            result = asyncio.run(app.process_image("clipboard"))
            print(f"Clipboard processing result: {result}")
            
        elif args.test:
            # Test mode
            print("Running in test mode...")
            init_success = asyncio.run(app.initialize())
            print(f"Initialization: {'Success' if init_success else 'Failed'}")
            
        else:
            # Normal mode
            app.run(show_ui=not args.no_ui)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()