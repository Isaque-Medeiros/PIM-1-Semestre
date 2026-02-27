"""
BrowserManager Module
Handles Playwright browser management and tab focusing for Latam form automation
"""

import asyncio
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import logging

from playwright.async_api import async_playwright, Browser, BrowserContext, Page, BrowserType
from ..core.latam_form import LatamForm
from ..core.rules_engine import RulesEngine


@dataclass
class BrowserTab:
    """Represents a browser tab with its properties"""
    page: Page
    url: str
    title: str
    is_latam_form: bool
    last_accessed: float


class BrowserManager:
    """Manager for browser automation and tab management"""
    
    def __init__(self, rules_engine: RulesEngine):
        """
        Initialize BrowserManager with rules engine
        
        Args:
            rules_engine: RulesEngine instance for validation
        """
        self.rules_engine = rules_engine
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.active_tabs: List[BrowserTab] = []
        self.latam_form: Optional[LatamForm] = None
        self.logger = logging.getLogger(__name__)
        
        # Browser configuration
        self.browser_type = "chromium"
        self.headless = False
        self.viewport = {"width": 1280, "height": 720}
        
    async def initialize(self) -> bool:
        """
        Initialize Playwright and browser
        
        Returns:
            True if initialized successfully, False otherwise
        """
        try:
            # Start Playwright
            self.playwright = await async_playwright().start()
            
            # Launch browser
            browser_type = getattr(self.playwright, self.browser_type)
            self.browser = await browser_type.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-extensions",
                    "--disable-plugins"
                ]
            )
            
            # Create context
            self.context = await self.browser.new_context(
                viewport=self.viewport,
                java_script_enabled=True,
                ignore_https_errors=True
            )
            
            # Set user agent to avoid detection
            await self.context.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            self.logger.info("Browser initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing browser: {e}")
            return False
    
    async def find_latam_tabs(self) -> List[BrowserTab]:
        """
        Find all tabs that might contain Latam forms
        
        Returns:
            List of BrowserTab objects
        """
        try:
            if not self.context:
                return []
            
            # Get all pages in context
            pages = self.context.pages
            latam_tabs = []
            
            for page in pages:
                try:
                    url = page.url
                    title = await page.title() if page.url else "Untitled"
                    
                    # Check if this might be a Latam form
                    is_latam = self._is_latam_form_page(url, title)
                    
                    tab = BrowserTab(
                        page=page,
                        url=url,
                        title=title,
                        is_latam_form=is_latam,
                        last_accessed=time.time()
                    )
                    
                    latam_tabs.append(tab)
                    
                except Exception as e:
                    self.logger.warning(f"Error processing page: {e}")
                    continue
            
            self.active_tabs = latam_tabs
            return latam_tabs
            
        except Exception as e:
            self.logger.error(f"Error finding Latam tabs: {e}")
            return []
    
    def _is_latam_form_page(self, url: str, title: str) -> bool:
        """
        Check if a page is likely to be a Latam form
        
        Args:
            url: Page URL
            title: Page title
            
        Returns:
            True if likely a Latam form page
        """
        latam_indicators = [
            "latam", "estouro", "classe", "form", "pnr", "reserva",
            "autorização", "upgrade", "cepnr", "sabre"
        ]
        
        combined_text = f"{url} {title}".lower()
        
        # Count matching indicators
        matches = sum(1 for indicator in latam_indicators if indicator in combined_text)
        
        # Consider it a Latam form if we find at least 2 indicators
        return matches >= 2
    
    async def focus_latam_tab(self) -> Optional[LatamForm]:
        """
        Focus on the most appropriate Latam form tab
        
        Returns:
            LatamForm instance if successful, None otherwise
        """
        try:
            # Find Latam tabs
            latam_tabs = await self.find_latam_tabs()
            
            if not latam_tabs:
                self.logger.warning("No Latam form tabs found")
                return None
            
            # Find the best candidate (most recent or most relevant)
            best_tab = self._select_best_tab(latam_tabs)
            
            if best_tab:
                # Create LatamForm instance for this tab
                self.latam_form = LatamForm(self.rules_engine, self.browser_type)
                self.latam_form.page = best_tab.page
                self.latam_form.form_url = best_tab.url
                self.latam_form.is_form_loaded = await self.latam_form._check_form_loaded()
                
                self.logger.info(f"Focused on Latam tab: {best_tab.url}")
                return self.latam_form
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error focusing Latam tab: {e}")
            return None
    
    def _select_best_tab(self, tabs: List[BrowserTab]) -> Optional[BrowserTab]:
        """
        Select the best tab from a list of candidates
        
        Args:
            tabs: List of BrowserTab objects
            
        Returns:
            Best BrowserTab or None
        """
        if not tabs:
            return None
        
        # Sort by relevance (Latam form first, then by last accessed)
        tabs.sort(key=lambda tab: (not tab.is_latam_form, -tab.last_accessed))
        
        return tabs[0]
    
    async def create_new_tab(self, url: str = "") -> Optional[Page]:
        """
        Create a new browser tab
        
        Args:
            url: URL to navigate to (optional)
            
        Returns:
            New Page instance if successful, None otherwise
        """
        try:
            if not self.context:
                return None
            
            page = await self.context.new_page()
            
            if url:
                await page.goto(url, wait_until="domcontentloaded")
            
            # Update tab list
            await self.find_latam_tabs()
            
            self.logger.info(f"Created new tab: {url}")
            return page
            
        except Exception as e:
            self.logger.error(f"Error creating new tab: {e}")
            return None
    
    async def get_form_status(self) -> Dict[str, Any]:
        """
        Get current form status and browser information
        
        Returns:
            Dictionary with status information
        """
        try:
            status = {
                "browser_initialized": self.browser is not None,
                "context_created": self.context is not None,
                "active_tabs_count": len(self.active_tabs),
                "latam_form_active": self.latam_form is not None
            }
            
            if self.latam_form:
                form_status = await self.latam_form.get_form_status()
                status["form_details"] = form_status
            
            if self.active_tabs:
                status["tabs"] = [
                    {
                        "url": tab.url,
                        "title": tab.title,
                        "is_latam": tab.is_latam_form,
                        "last_accessed": tab.last_accessed
                    }
                    for tab in self.active_tabs
                ]
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting form status: {e}")
            return {"error": str(e)}
    
    async def wait_for_form_load(self, timeout: int = 30) -> bool:
        """
        Wait for Latam form to load
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if form loaded, False if timeout
        """
        try:
            if not self.latam_form:
                return False
            
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if await self.latam_form._check_form_loaded():
                    return True
                await asyncio.sleep(0.5)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error waiting for form load: {e}")
            return False
    
    async def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            
            self.browser = None
            self.context = None
            self.latam_form = None
            self.active_tabs = []
            
            self.logger.info("Browser cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    async def refresh_tabs(self):
        """Refresh the list of active tabs"""
        await self.find_latam_tabs()
    
    async def switch_to_tab(self, tab_index: int) -> bool:
        """
        Switch to a specific tab by index
        
        Args:
            tab_index: Index of tab to switch to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.context or tab_index >= len(self.active_tabs):
                return False
            
            tab = self.active_tabs[tab_index]
            # Bring tab to front (this is handled by the page object)
            
            # Update LatamForm if this is a Latam tab
            if tab.is_latam_form:
                if not self.latam_form:
                    self.latam_form = LatamForm(self.rules_engine, self.browser_type)
                
                self.latam_form.page = tab.page
                self.latam_form.form_url = tab.url
                self.latam_form.is_form_loaded = await self.latam_form._check_form_loaded()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error switching to tab {tab_index}: {e}")
            return False