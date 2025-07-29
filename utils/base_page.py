"""
Base page class with common functionality
"""
import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.actions = ActionChains(driver)
    
    def navigate_to(self, url):
        """Navigate to a specific URL"""
        self.driver.get(url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self):
        """Wait for page to load completely"""
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    def find_element(self, locator, timeout=None):
        """Find element with explicit wait"""
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator, timeout=None):
        """Find multiple elements with explicit wait"""
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)
    
    def click_element(self, locator, timeout=None):
        """Click element with explicit wait"""
        element = self.wait_for_clickable(locator, timeout)
        element.click()
    
    def wait_for_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_visible(self, locator, timeout=None):
        """Wait for element to be visible"""
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator):
        """Scroll to element"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
    
    def hover_over_element(self, locator):
        """Hover over element"""
        element = self.find_element(locator)
        self.actions.move_to_element(element).perform()
    
    def get_text(self, locator):
        """Get text from element"""
        element = self.find_element(locator)
        return element.text
    
    def get_attribute(self, locator, attribute):
        """Get attribute value from element"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    def take_screenshot(self, name=None):
        """Take screenshot"""
        if not os.path.exists(Config.SCREENSHOT_DIR):
            os.makedirs(Config.SCREENSHOT_DIR)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
        filepath = os.path.join(Config.SCREENSHOT_DIR, filename)
        
        self.driver.save_screenshot(filepath)
        return filepath
    
    def execute_javascript(self, script, *args):
        """Execute JavaScript"""
        return self.driver.execute_script(script, *args)
    
    def get_page_title(self):
        """Get page title"""
        return self.driver.title
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
    
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.wait_for_page_load()