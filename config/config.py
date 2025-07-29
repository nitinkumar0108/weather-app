"""
Configuration settings for the test framework
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

class Config:
    # Base URL
    BASE_URL = "https://kalp.network/"
    
    # Timeouts
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30
    
    # Browser settings
    BROWSER = os.getenv('BROWSER', 'chrome').lower()
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    
    # Screenshot settings
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_DIR = "screenshots"
    
    # Report settings
    REPORT_DIR = "reports"
    
    @staticmethod
    def get_driver():
        """Initialize and return WebDriver instance"""
        if Config.BROWSER == 'chrome':
            options = ChromeOptions()
            if Config.HEADLESS:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
        elif Config.BROWSER == 'firefox':
            options = FirefoxOptions()
            if Config.HEADLESS:
                options.add_argument('--headless')
            
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {Config.BROWSER}")
        
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        driver.maximize_window()
        
        return driver