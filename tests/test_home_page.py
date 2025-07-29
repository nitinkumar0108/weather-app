"""
Home page exploratory tests
"""
import pytest
import time
from utils.helpers import TestHelpers
from utils.test_data import TestData

class TestHomePage:
    
    def test_page_loads_successfully(self, home_page):
        """Test that the home page loads successfully"""
        assert "kalp" in home_page.get_page_title().lower()
        assert "kalp.network" in home_page.get_current_url()
    
    def test_page_elements_present(self, home_page):
        """Test that key page elements are present"""
        elements = home_page.verify_page_elements()
        
        # At least navigation should be present
        assert elements['navigation'], "Navigation menu should be present"
        
        # Take screenshot for visual verification
        home_page.take_screenshot("page_elements_verification")
    
    def test_navigation_functionality(self, home_page):
        """Test navigation menu functionality"""
        nav_links = home_page.get_navigation_links()
        
        if nav_links:
            print(f"Found {len(nav_links)} navigation links")
            
            # Test each navigation link
            for i, link in enumerate(nav_links[:5]):  # Test first 5 links
                try:
                    link_text = link.text
                    href = link.get_attribute('href')
                    
                    if href and href.startswith('http'):
                        print(f"Testing link: {link_text} -> {href}")
                        
                        # Click link and verify page loads
                        original_url = home_page.get_current_url()
                        link.click()
                        time.sleep(2)
                        
                        new_url = home_page.get_current_url()
                        assert new_url != original_url or "#" in href, f"Link {link_text} should navigate somewhere"
                        
                        # Go back to home page for next test
                        home_page.driver.back()
                        time.sleep(2)
                        
                except Exception as e:
                    print(f"Error testing link {i}: {e}")
                    continue
    
    def test_responsive_design(self, home_page):
        """Test responsive design at different viewport sizes"""
        for size in TestData.VIEWPORT_SIZES:
            print(f"Testing viewport size: {size[0]}x{size[1]}")
            
            elements_info = TestHelpers.check_responsive_elements(home_page.driver, size)
            
            # Verify elements are visible
            visible_elements = [elem for elem in elements_info if elem['visible']]
            assert len(visible_elements) > 0, f"No elements visible at {size[0]}x{size[1]}"
            
            # Take screenshot for each viewport
            home_page.take_screenshot(f"responsive_{size[0]}x{size[1]}")
    
    def test_page_performance(self, home_page):
        """Test page load performance"""
        load_time = TestHelpers.measure_page_load_time(
            home_page.driver, 
            home_page.get_current_url()
        )
        
        print(f"Page load time: {load_time:.2f} seconds")
        
        # Performance assertion
        assert load_time < TestData.PERFORMANCE_THRESHOLDS['page_load_time'], \
            f"Page load time {load_time:.2f}s exceeds threshold"
    
    def test_broken_links(self, home_page):
        """Test for broken links on the page"""
        broken_links = TestHelpers.check_broken_links(
            home_page.driver, 
            home_page.get_current_url()
        )
        
        if broken_links:
            print("Broken links found:")
            for link in broken_links:
                print(f"  - {link}")
        
        # This is exploratory, so we log but don't fail
        assert len(broken_links) < 10, "Too many broken links found"
    
    def test_images_loading(self, home_page):
        """Test that images load properly"""
        broken_images = TestHelpers.check_images_loaded(home_page.driver)
        
        if broken_images:
            print("Broken images found:")
            for img in broken_images:
                print(f"  - {img}")
        
        # Log broken images but don't fail the test
        print(f"Found {len(broken_images)} broken images")
    
    def test_console_errors(self, home_page):
        """Check for JavaScript console errors"""
        errors = TestHelpers.get_console_errors(home_page.driver)
        
        if errors:
            print("Console errors found:")
            for error in errors:
                print(f"  - {error['message']}")
        
        # Log errors but don't fail unless critical
        assert len(errors) < 5, "Too many console errors"
    
    def test_seo_elements(self, home_page):
        """Test basic SEO elements"""
        seo_info = TestHelpers.check_seo_elements(home_page.driver)
        
        print("SEO Analysis:")
        print(f"  Title: {seo_info['title']} (Length: {seo_info['title_length']})")
        print(f"  Meta Description: {seo_info.get('meta_description', 'Not found')}")
        
        if seo_info.get('meta_description'):
            print(f"  Meta Description Length: {seo_info['meta_description_length']}")
        
        print("  Headings structure:")
        for heading_level, headings in seo_info['headings'].items():
            if headings:
                print(f"    {heading_level}: {len(headings)} found")
        
        if seo_info['images_without_alt']:
            print(f"  Images without alt text: {len(seo_info['images_without_alt'])}")
        
        # Basic SEO assertions
        assert seo_info['title'], "Page should have a title"
        assert len(seo_info['title']) > 10, "Title should be descriptive"
    
    def test_social_media_links(self, home_page):
        """Test social media links if present"""
        social_links = home_page.get_social_links()
        
        if social_links:
            print(f"Found {len(social_links)} social media links")
            
            for link in social_links:
                href = link.get_attribute('href')
                print(f"  Social link: {href}")
                
                # Verify links are valid URLs
                assert href.startswith(('http://', 'https://')), "Social links should be valid URLs"
        else:
            print("No social media links found")
    
    def test_cta_buttons_functionality(self, home_page):
        """Test Call-to-Action buttons"""
        cta_buttons = home_page.get_cta_buttons()
        
        if cta_buttons:
            print(f"Found {len(cta_buttons)} CTA buttons")
            
            for i, button in enumerate(cta_buttons[:3]):  # Test first 3 buttons
                try:
                    button_text = button.text
                    print(f"Testing CTA button: {button_text}")
                    
                    # Scroll to button and hover
                    home_page.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(1)
                    
                    # Check if button is clickable
                    assert button.is_enabled(), f"CTA button '{button_text}' should be enabled"
                    
                except Exception as e:
                    print(f"Error testing CTA button {i}: {e}")
        else:
            print("No CTA buttons found")
    
    def test_page_scroll_functionality(self, home_page):
        """Test page scrolling functionality"""
        # Get initial scroll position
        initial_scroll = home_page.driver.execute_script("return window.pageYOffset;")
        
        # Scroll to bottom
        home_page.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Get final scroll position
        final_scroll = home_page.driver.execute_script("return window.pageYOffset;")
        
        assert final_scroll > initial_scroll, "Page should be scrollable"
        
        # Scroll back to top
        home_page.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        top_scroll = home_page.driver.execute_script("return window.pageYOffset;")
        assert top_scroll == 0, "Should be able to scroll back to top"
    
    def test_page_accessibility_basics(self, home_page):
        """Test basic accessibility features"""
        # Check for alt attributes on images
        images = home_page.driver.find_elements("tag name", "img")
        images_without_alt = []
        
        for img in images:
            alt = img.get_attribute('alt')
            if not alt:
                images_without_alt.append(img.get_attribute('src'))
        
        print(f"Images without alt text: {len(images_without_alt)}")
        
        # Check for form labels
        inputs = home_page.driver.find_elements("tag name", "input")
        inputs_without_labels = []
        
        for input_elem in inputs:
            input_id = input_elem.get_attribute('id')
            input_name = input_elem.get_attribute('name')
            
            # Check if there's a label for this input
            try:
                if input_id:
                    home_page.driver.find_element("css selector", f"label[for='{input_id}']")
                elif input_name:
                    # Check if input is wrapped in label
                    parent = input_elem.find_element("xpath", "..")
                    if parent.tag_name.lower() != 'label':
                        inputs_without_labels.append(input_name or 'unnamed')
            except:
                inputs_without_labels.append(input_name or 'unnamed')
        
        print(f"Form inputs without labels: {len(inputs_without_labels)}")
        
        # These are warnings, not failures for exploratory testing
        if images_without_alt:
            print("Consider adding alt text to images for better accessibility")
        
        if inputs_without_labels:
            print("Consider adding labels to form inputs for better accessibility")