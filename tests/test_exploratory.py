"""
Additional exploratory tests for comprehensive coverage
"""
import pytest
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils.helpers import TestHelpers
from utils.test_data import TestData

class TestExploratoryScenarios:
    
    def test_random_link_exploration(self, home_page):
        """Randomly explore links on the page"""
        all_links = TestHelpers.extract_all_links(home_page.driver)
        internal_links = [link for link in all_links if not link['is_external']]
        
        if internal_links:
            # Randomly select up to 3 internal links to explore
            links_to_test = random.sample(internal_links, min(3, len(internal_links)))
            
            for link in links_to_test:
                try:
                    print(f"Exploring link: {link['text']} -> {link['url']}")
                    
                    # Navigate to link
                    home_page.navigate_to(link['url'])
                    time.sleep(2)
                    
                    # Basic checks on the new page
                    assert home_page.driver.title, "Page should have a title"
                    
                    # Check for common elements
                    common_elements = [
                        (By.TAG_NAME, "h1"),
                        (By.TAG_NAME, "nav"),
                        (By.TAG_NAME, "footer")
                    ]
                    
                    for locator in common_elements:
                        if home_page.is_element_present(locator, timeout=3):
                            print(f"  Found {locator[1]} element")
                    
                    # Take screenshot
                    home_page.take_screenshot(f"exploration_{link['text'].replace(' ', '_')}")
                    
                except Exception as e:
                    print(f"Error exploring link {link['url']}: {e}")
                    continue
    
    def test_form_interactions(self, home_page):
        """Test form interactions if forms are present"""
        forms = home_page.driver.find_elements(By.TAG_NAME, "form")
        
        if forms:
            print(f"Found {len(forms)} forms on the page")
            
            for i, form in enumerate(forms):
                try:
                    print(f"Testing form {i+1}")
                    
                    # Find input fields
                    inputs = form.find_elements(By.TAG_NAME, "input")
                    textareas = form.find_elements(By.TAG_NAME, "textarea")
                    selects = form.find_elements(By.TAG_NAME, "select")
                    
                    print(f"  Inputs: {len(inputs)}, Textareas: {len(textareas)}, Selects: {len(selects)}")
                    
                    # Test input fields
                    for input_field in inputs:
                        input_type = input_field.get_attribute('type')
                        
                        if input_type in ['text', 'email', 'tel', 'url']:
                            # Test with valid data
                            test_value = "test@example.com" if input_type == 'email' else "Test Value"
                            input_field.clear()
                            input_field.send_keys(test_value)
                            
                            # Verify value was entered
                            assert input_field.get_attribute('value') == test_value
                    
                    # Test textareas
                    for textarea in textareas:
                        textarea.clear()
                        textarea.send_keys("This is a test message for exploratory testing.")
                    
                    # Take screenshot of filled form
                    home_page.take_screenshot(f"form_{i+1}_filled")
                    
                except Exception as e:
                    print(f"Error testing form {i+1}: {e}")
        else:
            print("No forms found on the page")
    
    def test_keyboard_navigation(self, home_page):
        """Test keyboard navigation"""
        try:
            # Start from the body element
            body = home_page.driver.find_element(By.TAG_NAME, "body")
            body.click()
            
            # Test Tab navigation
            focusable_elements = []
            for _ in range(10):  # Try tabbing through first 10 elements
                try:
                    # Press Tab
                    home_page.driver.switch_to.active_element.send_keys(Keys.TAB)
                    time.sleep(0.5)
                    
                    # Get currently focused element
                    focused = home_page.driver.switch_to.active_element
                    tag_name = focused.tag_name
                    element_id = focused.get_attribute('id')
                    element_class = focused.get_attribute('class')
                    
                    focusable_elements.append({
                        'tag': tag_name,
                        'id': element_id,
                        'class': element_class
                    })
                    
                except Exception as e:
                    print(f"Error during keyboard navigation: {e}")
                    break
            
            print(f"Found {len(focusable_elements)} focusable elements")
            for elem in focusable_elements:
                print(f"  {elem['tag']} - ID: {elem['id']} - Class: {elem['class']}")
            
            # Test Enter key on focusable elements
            if focusable_elements:
                try:
                    home_page.driver.switch_to.active_element.send_keys(Keys.ENTER)
                    time.sleep(1)
                    print("Enter key interaction tested")
                except:
                    pass
                    
        except Exception as e:
            print(f"Keyboard navigation test failed: {e}")
    
    def test_browser_back_forward(self, home_page):
        """Test browser back and forward functionality"""
        original_url = home_page.get_current_url()
        
        # Find a link to navigate to
        links = home_page.driver.find_elements(By.TAG_NAME, "a")
        navigable_links = [link for link in links if link.get_attribute('href') 
                          and link.get_attribute('href').startswith('http')]
        
        if navigable_links:
            # Click first navigable link
            first_link = navigable_links[0]
            first_link.click()
            time.sleep(2)
            
            new_url = home_page.get_current_url()
            
            # Test back button
            home_page.driver.back()
            time.sleep(2)
            
            back_url = home_page.get_current_url()
            assert back_url == original_url, "Back button should return to original page"
            
            # Test forward button
            home_page.driver.forward()
            time.sleep(2)
            
            forward_url = home_page.get_current_url()
            assert forward_url == new_url, "Forward button should return to second page"
            
            print("Browser navigation (back/forward) working correctly")
    
    def test_page_zoom_functionality(self, home_page):
        """Test page zoom functionality"""
        original_size = home_page.driver.get_window_size()
        
        # Test zoom in
        home_page.driver.execute_script("document.body.style.zoom='150%'")
        time.sleep(2)
        home_page.take_screenshot("zoom_150_percent")
        
        # Test zoom out
        home_page.driver.execute_script("document.body.style.zoom='75%'")
        time.sleep(2)
        home_page.take_screenshot("zoom_75_percent")
        
        # Reset zoom
        home_page.driver.execute_script("document.body.style.zoom='100%'")
        time.sleep(1)
        
        print("Zoom functionality tested")
    
    def test_page_refresh_behavior(self, home_page):
        """Test page refresh behavior"""
        original_title = home_page.get_page_title()
        original_url = home_page.get_current_url()
        
        # Refresh the page
        home_page.refresh_page()
        
        # Verify page loaded correctly after refresh
        assert home_page.get_page_title() == original_title, "Title should remain same after refresh"
        assert home_page.get_current_url() == original_url, "URL should remain same after refresh"
        
        print("Page refresh behavior verified")
    
    def test_right_click_context_menu(self, home_page):
        """Test right-click context menu (where applicable)"""
        try:
            # Find an element to right-click on
            elements = home_page.driver.find_elements(By.TAG_NAME, "p")
            if not elements:
                elements = home_page.driver.find_elements(By.TAG_NAME, "div")
            
            if elements:
                element = elements[0]
                
                # Right-click on element
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(home_page.driver)
                actions.context_click(element).perform()
                time.sleep(1)
                
                # Take screenshot to capture context menu if visible
                home_page.take_screenshot("right_click_context_menu")
                
                # Click elsewhere to close context menu
                home_page.driver.find_element(By.TAG_NAME, "body").click()
                
                print("Right-click context menu tested")
        
        except Exception as e:
            print(f"Right-click test failed: {e}")
    
    def test_text_selection(self, home_page):
        """Test text selection functionality"""
        try:
            # Find text elements
            text_elements = home_page.driver.find_elements(By.TAG_NAME, "p")
            if not text_elements:
                text_elements = home_page.driver.find_elements(By.TAG_NAME, "h1")
            
            if text_elements:
                element = text_elements[0]
                text_content = element.text
                
                if text_content:
                    # Double-click to select text
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(home_page.driver)
                    actions.double_click(element).perform()
                    time.sleep(1)
                    
                    # Take screenshot of selected text
                    home_page.take_screenshot("text_selection")
                    
                    print(f"Text selection tested on: {text_content[:50]}...")
        
        except Exception as e:
            print(f"Text selection test failed: {e}")
    
    def test_scroll_behavior_edge_cases(self, home_page):
        """Test scroll behavior edge cases"""
        # Test rapid scrolling
        for _ in range(5):
            home_page.driver.execute_script("window.scrollBy(0, 200);")
            time.sleep(0.1)
        
        # Test scroll to specific positions
        positions = [0, 500, 1000, 9999999]  # Last one tests max scroll
        
        for pos in positions:
            home_page.driver.execute_script(f"window.scrollTo(0, {pos});")
            time.sleep(0.5)
            
            current_scroll = home_page.driver.execute_script("return window.pageYOffset;")
            print(f"Scrolled to position: {current_scroll}")
        
        # Test horizontal scroll if applicable
        home_page.driver.execute_script("window.scrollTo(100, 0);")
        time.sleep(0.5)
        
        horizontal_scroll = home_page.driver.execute_script("return window.pageXOffset;")
        print(f"Horizontal scroll position: {horizontal_scroll}")
        
        print("Scroll behavior edge cases tested")