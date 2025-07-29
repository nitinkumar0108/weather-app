"""
Home page object model for Kalp Network
"""
from selenium.webdriver.common.by import By
from utils.base_page import BasePage

class HomePage(BasePage):
    # Locators
    LOGO = (By.CSS_SELECTOR, "img[alt*='logo'], .logo")
    NAVIGATION_MENU = (By.CSS_SELECTOR, "nav, .navbar, .navigation")
    HERO_SECTION = (By.CSS_SELECTOR, ".hero, .banner, .main-banner")
    CTA_BUTTONS = (By.CSS_SELECTOR, "a[href*='contact'], button[class*='cta'], .btn-primary")
    FOOTER = (By.CSS_SELECTOR, "footer")
    SOCIAL_LINKS = (By.CSS_SELECTOR, "a[href*='twitter'], a[href*='linkedin'], a[href*='facebook']")
    
    # Navigation links
    NAV_LINKS = (By.CSS_SELECTOR, "nav a, .navbar a, .navigation a")
    
    # Content sections
    ABOUT_SECTION = (By.CSS_SELECTOR, "[id*='about'], .about, [class*='about']")
    SERVICES_SECTION = (By.CSS_SELECTOR, "[id*='service'], .service, [class*='service']")
    CONTACT_SECTION = (By.CSS_SELECTOR, "[id*='contact'], .contact, [class*='contact']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def load(self):
        """Load the home page"""
        from config.config import Config
        self.navigate_to(Config.BASE_URL)
    
    def is_logo_displayed(self):
        """Check if logo is displayed"""
        return self.is_element_visible(self.LOGO)
    
    def get_navigation_links(self):
        """Get all navigation links"""
        try:
            return self.find_elements(self.NAV_LINKS)
        except:
            return []
    
    def click_navigation_link(self, link_text):
        """Click navigation link by text"""
        links = self.get_navigation_links()
        for link in links:
            if link_text.lower() in link.text.lower():
                link.click()
                return True
        return False
    
    def get_hero_text(self):
        """Get hero section text"""
        try:
            return self.get_text(self.HERO_SECTION)
        except:
            return ""
    
    def get_cta_buttons(self):
        """Get all CTA buttons"""
        try:
            return self.find_elements(self.CTA_BUTTONS)
        except:
            return []
    
    def click_first_cta_button(self):
        """Click the first CTA button"""
        buttons = self.get_cta_buttons()
        if buttons:
            buttons[0].click()
            return True
        return False
    
    def scroll_to_footer(self):
        """Scroll to footer"""
        if self.is_element_present(self.FOOTER):
            self.scroll_to_element(self.FOOTER)
            return True
        return False
    
    def get_social_links(self):
        """Get social media links"""
        try:
            return self.find_elements(self.SOCIAL_LINKS)
        except:
            return []
    
    def verify_page_elements(self):
        """Verify key page elements are present"""
        elements_status = {
            'logo': self.is_element_present(self.LOGO),
            'navigation': self.is_element_present(self.NAVIGATION_MENU),
            'hero_section': self.is_element_present(self.HERO_SECTION),
            'footer': self.is_element_present(self.FOOTER)
        }
        return elements_status