"""
Browser Automation Manager

Handles web browser automation using both Selenium and Playwright
for maximum compatibility and reliability.
"""

import asyncio
import time
import os
from pathlib import Path
from typing import Optional, Any, Dict, List, Union
from urllib.parse import urlparse

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import undetected_chromedriver as uc
from fake_useragent import UserAgent

try:
    from playwright.async_api import async_playwright, Browser as PlaywrightBrowser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not available, using Selenium only")


class BrowserManager:
    """
    Manages browser automation with support for multiple browser engines.
    """
    
    def __init__(
        self,
        headless: bool = True,
        browser_type: str = "chrome",
        use_undetected: bool = True,
        timeout: int = 30,
        screenshots_dir: str = "screenshots"
    ):
        """
        Initialize browser manager.
        
        Args:
            headless: Whether to run in headless mode
            browser_type: Type of browser (chrome, firefox, edge, playwright)
            use_undetected: Whether to use undetected Chrome driver
            timeout: Default timeout for operations
            screenshots_dir: Directory to save screenshots
        """
        self.headless = headless
        self.browser_type = browser_type
        self.use_undetected = use_undetected
        self.timeout = timeout
        self.screenshots_dir = Path(screenshots_dir)
        self.screenshots_dir.mkdir(exist_ok=True)
        
        # Browser instances
        self.selenium_driver = None
        self.playwright_browser = None
        self.playwright_page = None
        
        # User agent
        self.user_agent = UserAgent()
        
        logger.info(f"BrowserManager initialized with {browser_type}")
    
    async def start(self) -> None:
        """Start the browser instance."""
        if self.browser_type == "playwright" and PLAYWRIGHT_AVAILABLE:
            await self._start_playwright()
        else:
            await self._start_selenium()
    
    async def _start_selenium(self) -> None:
        """Start Selenium browser."""
        try:
            if self.browser_type == "chrome":
                if self.use_undetected:
                    options = uc.ChromeOptions()
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                    options.add_argument("--disable-blink-features=AutomationControlled")
                    options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    options.add_experimental_option('useAutomationExtension', False)
                    if self.headless:
                        options.add_argument("--headless")
                    
                    self.selenium_driver = uc.Chrome(
                        options=options,
                        driver_executable_path=ChromeDriverManager().install()
                    )
                else:
                    options = ChromeOptions()
                    options.add_argument(f"--user-agent={self.user_agent.chrome}")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                    if self.headless:
                        options.add_argument("--headless")
                    
                    self.selenium_driver = webdriver.Chrome(
                        service=webdriver.chrome.service.Service(
                            ChromeDriverManager().install()
                        ),
                        options=options
                    )
            
            elif self.browser_type == "firefox":
                options = FirefoxOptions()
                options.add_argument(f"--user-agent={self.user_agent.firefox}")
                if self.headless:
                    options.add_argument("--headless")
                
                self.selenium_driver = webdriver.Firefox(
                    service=webdriver.firefox.service.Service(
                        GeckoDriverManager().install()
                    ),
                    options=options
                )
            
            elif self.browser_type == "edge":
                options = EdgeOptions()
                options.add_argument(f"--user-agent={self.user_agent.edge}")
                if self.headless:
                    options.add_argument("--headless")
                
                self.selenium_driver = webdriver.Edge(
                    service=webdriver.edge.service.Service(
                        EdgeChromiumDriverManager().install()
                    ),
                    options=options
                )
            
            # Set window size and timeout
            self.selenium_driver.set_window_size(1920, 1080)
            self.selenium_driver.implicitly_wait(self.timeout)
            
            # Execute script to remove webdriver property
            if self.selenium_driver:
                self.selenium_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info(f"Selenium {self.browser_type} browser started")
            
        except Exception as e:
            logger.error(f"Failed to start Selenium browser: {str(e)}")
            raise
    
    async def _start_playwright(self) -> None:
        """Start Playwright browser."""
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright is not installed")
        
        try:
            self.playwright = await async_playwright().start()
            
            if self.browser_type == "playwright":
                browser_name = "chromium"
            else:
                browser_name = self.browser_type
            
            browser_class = getattr(self.playwright, browser_name)
            self.playwright_browser = await browser_class.launch(
                headless=self.headless
            )
            
            self.playwright_page = await self.playwright_browser.new_page()
            await self.playwright_page.set_viewport_size({"width": 1920, "height": 1080})
            
            # Set user agent
            await self.playwright_page.set_extra_http_headers({
                "User-Agent": self.user_agent.chrome
            })
            
            logger.info(f"Playwright {browser_name} browser started")
            
        except Exception as e:
            logger.error(f"Failed to start Playwright browser: {str(e)}")
            raise
    
    async def navigate(self, url: str) -> None:
        """Navigate to a URL."""
        try:
            if self.selenium_driver:
                self.selenium_driver.get(url)
                # Wait for page to load
                WebDriverWait(self.selenium_driver, self.timeout).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            elif self.playwright_page:
                await self.playwright_page.goto(url, wait_until="networkidle")
            
            logger.info(f"Navigated to {url}")
            
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {str(e)}")
            raise
    
    async def find_and_click_apply_link(self, link_texts: List[str] = None) -> bool:
        """
        Find and click an "Apply" link on the current page.
        
        Args:
            link_texts: List of possible link texts to look for
            
        Returns:
            True if link was found and clicked, False otherwise
        """
        if link_texts is None:
            link_texts = [
                "Apply", "Apply Now", "Apply Here", "Submit Application",
                "Start Application", "Begin Application", "Apply for Funding",
                "Submit", "Apply Today", "Get Started", "Apply Now",
                "Apply for Investment", "Submit Your Application"
            ]
        
        try:
            if self.selenium_driver:
                # Try different selectors for apply links
                selectors = [
                    "//a[contains(text(), '{}')]",
                    "//button[contains(text(), '{}')]",
                    "//*[contains(text(), '{}') and (self::a or self::button)]",
                    "//a[contains(@href, 'apply')]",
                    "//a[contains(@href, 'application')]",
                    "//a[contains(@class, 'apply')]",
                    "//button[contains(@class, 'apply')]"
                ]
                
                for link_text in link_texts:
                    for selector_template in selectors:
                        try:
                            if "{}" in selector_template:
                                selector = selector_template.format(link_text)
                            else:
                                selector = selector_template
                            
                            element = WebDriverWait(self.selenium_driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                            
                            # Scroll to element
                            self.selenium_driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            await asyncio.sleep(1)
                            
                            # Click the element
                            element.click()
                            logger.info(f"Clicked apply link: {link_text}")
                            return True
                            
                        except TimeoutException:
                            continue
                
                # If no specific link found, try to find any link with "apply" in href
                try:
                    apply_link = self.selenium_driver.find_element(By.XPATH, "//a[contains(@href, 'apply') or contains(@href, 'application')]")
                    apply_link.click()
                    logger.info("Clicked apply link found by href")
                    return True
                except NoSuchElementException:
                    pass
                
            elif self.playwright_page:
                # Playwright implementation
                for link_text in link_texts:
                    try:
                        # Try different selectors
                        selectors = [
                            f"text={link_text}",
                            f"a:has-text('{link_text}')",
                            f"button:has-text('{link_text}')",
                            "a[href*='apply']",
                            "a[href*='application']"
                        ]
                        
                        for selector in selectors:
                            try:
                                element = await self.playwright_page.wait_for_selector(selector, timeout=5000)
                                if element:
                                    await element.click()
                                    logger.info(f"Clicked apply link: {link_text}")
                                    return True
                            except:
                                continue
                    except:
                        continue
            
            logger.warning("No apply link found on the page")
            return False
            
        except Exception as e:
            logger.error(f"Error finding/clicking apply link: {str(e)}")
            return False
    
    async def wait_for_page_load(self, timeout: int = None) -> None:
        """Wait for page to fully load."""
        timeout = timeout or self.timeout
        
        try:
            if self.selenium_driver:
                WebDriverWait(self.selenium_driver, timeout).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
            elif self.playwright_page:
                await self.playwright_page.wait_for_load_state("networkidle", timeout=timeout * 1000)
            
            # Additional wait for dynamic content
            await asyncio.sleep(2)
            
        except Exception as e:
            logger.warning(f"Page load wait failed: {str(e)}")
    
    async def find_field(self, field_name: str) -> Optional[Any]:
        """
        Find a form field by various selectors.
        
        Args:
            field_name: Name or identifier of the field
            
        Returns:
            WebElement or Playwright element if found, None otherwise
        """
        selectors = [
            f'input[name="{field_name}"]',
            f'textarea[name="{field_name}"]',
            f'select[name="{field_name}"]',
            f'input[id="{field_name}"]',
            f'textarea[id="{field_name}"]',
            f'select[id="{field_name}"]',
            f'[data-field="{field_name}"]',
            f'[data-name="{field_name}"]',
            f'[placeholder*="{field_name}"]',
            f'label[for="{field_name}"] + input',
            f'label[for="{field_name}"] + textarea',
            f'label[for="{field_name}"] + select',
            f'input[placeholder*="{field_name}"]',
            f'textarea[placeholder*="{field_name}"]'
        ]
        
        for selector in selectors:
            try:
                if self.selenium_driver:
                    element = self.selenium_driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed() and element.is_enabled():
                        return element
                elif self.playwright_page:
                    element = await self.playwright_page.query_selector(selector)
                    if element:
                        is_visible = await element.is_visible()
                        is_enabled = await element.is_enabled()
                        if is_visible and is_enabled:
                            return element
                            
            except (NoSuchElementException, Exception):
                continue
        
        return None
    
    async def fill_field(self, element: Any, value: str) -> None:
        """
        Fill a form field with a value.
        
        Args:
            element: WebElement or Playwright element
            value: Value to fill
        """
        try:
            if self.selenium_driver:
                # Clear existing value
                element.clear()
                # Focus on element
                element.click()
                # Type value with human-like delays
                for char in value:
                    element.send_keys(char)
                    await asyncio.sleep(0.01)  # Small delay between characters
            elif self.playwright_page:
                # Clear and fill
                await element.fill("")
                await element.type(value, delay=10)  # 10ms delay between characters
            
            logger.debug(f"Filled field with value: {value[:50]}...")
            
        except Exception as e:
            logger.error(f"Failed to fill field: {str(e)}")
            raise
    
    async def upload_file(self, field_name: str, file_path: Union[str, Path]) -> bool:
        """
        Upload a file to a file input field.
        
        Args:
            field_name: Name of the file input field
            file_path: Path to the file to upload
            
        Returns:
            True if upload was successful, False otherwise
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return False
            
            # Find file input field
            file_selectors = [
                f'input[type="file"][name="{field_name}"]',
                f'input[type="file"][id="{field_name}"]',
                f'input[type="file"]',
                f'[data-field="{field_name}"] input[type="file"]'
            ]
            
            file_input = None
            for selector in file_selectors:
                try:
                    if self.selenium_driver:
                        file_input = self.selenium_driver.find_element(By.CSS_SELECTOR, selector)
                        if file_input.is_displayed():
                            break
                    elif self.playwright_page:
                        file_input = await self.playwright_page.query_selector(selector)
                        if file_input:
                            break
                except:
                    continue
            
            if not file_input:
                logger.error(f"File input field '{field_name}' not found")
                return False
            
            # Upload file
            if self.selenium_driver:
                file_input.send_keys(str(file_path.absolute()))
            elif self.playwright_page:
                await file_input.set_input_files(str(file_path.absolute()))
            
            logger.info(f"Uploaded file: {file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload file: {str(e)}")
            return False
    
    async def upload_multiple_files(self, field_name: str, file_paths: List[Union[str, Path]]) -> bool:
        """
        Upload multiple files to a file input field.
        
        Args:
            field_name: Name of the file input field
            file_paths: List of file paths to upload
            
        Returns:
            True if upload was successful, False otherwise
        """
        try:
            file_paths = [Path(fp) for fp in file_paths]
            
            # Check if all files exist
            for file_path in file_paths:
                if not file_path.exists():
                    logger.error(f"File not found: {file_path}")
                    return False
            
            # Find file input field
            file_selectors = [
                f'input[type="file"][name="{field_name}"]',
                f'input[type="file"][id="{field_name}"]',
                f'input[type="file"]',
                f'[data-field="{field_name}"] input[type="file"]'
            ]
            
            file_input = None
            for selector in file_selectors:
                try:
                    if self.selenium_driver:
                        file_input = self.selenium_driver.find_element(By.CSS_SELECTOR, selector)
                        if file_input.is_displayed():
                            break
                    elif self.playwright_page:
                        file_input = await self.playwright_page.query_selector(selector)
                        if file_input:
                            break
                except:
                    continue
            
            if not file_input:
                logger.error(f"File input field '{field_name}' not found")
                return False
            
            # Upload files
            if self.selenium_driver:
                # For Selenium, we need to send all file paths as a single string
                file_paths_str = "\n".join(str(fp.absolute()) for fp in file_paths)
                file_input.send_keys(file_paths_str)
            elif self.playwright_page:
                # For Playwright, we can pass multiple files
                await file_input.set_input_files([str(fp.absolute()) for fp in file_paths])
            
            logger.info(f"Uploaded {len(file_paths)} files")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload multiple files: {str(e)}")
            return False
    
    async def select_option(self, element: Any, option_value: str) -> None:
        """
        Select an option from a dropdown.
        
        Args:
            element: Select element
            option_value: Value to select
        """
        try:
            if self.selenium_driver:
                from selenium.webdriver.support.ui import Select
                select = Select(element)
                select.select_by_value(option_value)
            elif self.playwright_page:
                await element.select_option(value=option_value)
            
            logger.debug(f"Selected option: {option_value}")
            
        except Exception as e:
            logger.error(f"Failed to select option: {str(e)}")
            raise
    
    async def click_button(self, button_text: str = None, selector: str = None) -> None:
        """
        Click a button.
        
        Args:
            button_text: Text of the button to click
            selector: CSS selector for the button
        """
        try:
            if selector:
                button_selector = selector
            elif button_text:
                button_selector = f'button:contains("{button_text}"), input[value="{button_text}"]'
            else:
                raise ValueError("Either button_text or selector must be provided")
            
            if self.selenium_driver:
                button = self.selenium_driver.find_element(By.CSS_SELECTOR, button_selector)
                button.click()
            elif self.playwright_page:
                await self.playwright_page.click(button_selector)
            
            logger.debug(f"Clicked button: {button_text or selector}")
            
        except Exception as e:
            logger.error(f"Failed to click button: {str(e)}")
            raise
    
    async def wait_for_element(self, selector: str, timeout: int = None) -> Any:
        """
        Wait for an element to appear.
        
        Args:
            selector: CSS selector for the element
            timeout: Timeout in seconds
            
        Returns:
            Element when found
        """
        timeout = timeout or self.timeout
        
        try:
            if self.selenium_driver:
                element = WebDriverWait(self.selenium_driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                return element
            elif self.playwright_page:
                element = await self.playwright_page.wait_for_selector(selector, timeout=timeout * 1000)
                return element
                
        except TimeoutException:
            logger.warning(f"Element {selector} not found within {timeout} seconds")
            return None
    
    async def take_screenshot(self, filename: str = None) -> str:
        """
        Take a screenshot of the current page.
        
        Args:
            filename: Optional filename for the screenshot
            
        Returns:
            Path to the screenshot file
        """
        if not filename:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_path = self.screenshots_dir / filename
        
        try:
            if self.selenium_driver:
                self.selenium_driver.save_screenshot(str(screenshot_path))
            elif self.playwright_page:
                await self.playwright_page.screenshot(path=str(screenshot_path))
            
            logger.info(f"Screenshot saved to {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return ""
    
    async def get_page_source(self) -> str:
        """Get the current page source."""
        try:
            if self.selenium_driver:
                return self.selenium_driver.page_source
            elif self.playwright_page:
                return await self.playwright_page.content()
        except Exception as e:
            logger.error(f"Failed to get page source: {str(e)}")
            return ""
    
    async def close(self) -> None:
        """Close the browser."""
        try:
            if self.selenium_driver:
                self.selenium_driver.quit()
                self.selenium_driver = None
            elif self.playwright_browser:
                await self.playwright_browser.close()
                await self.playwright.stop()
                self.playwright_browser = None
                self.playwright_page = None
            
            logger.info("Browser closed")
            
        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")
    
    def __enter__(self):
        """Context manager entry."""
        asyncio.create_task(self.start())
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        asyncio.create_task(self.close()) 