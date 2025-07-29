"""
Helper utilities for testing
"""
import time
import requests
from urllib.parse import urljoin, urlparse
from selenium.webdriver.common.by import By

class TestHelpers:
    
    @staticmethod
    def measure_page_load_time(driver, url):
        """Measure page load time"""
        start_time = time.time()
        driver.get(url)
        # Wait for page to be completely loaded
        driver.execute_script("return document.readyState") == "complete"
        end_time = time.time()
        return end_time - start_time
    
    @staticmethod
    def check_broken_links(driver, base_url):
        """Check for broken links on the page"""
        broken_links = []
        links = driver.find_elements(By.TAG_NAME, "a")
        
        for link in links:
            href = link.get_attribute("href")
            if href and href.startswith(('http://', 'https://')):
                try:
                    response = requests.head(href, timeout=10, allow_redirects=True)
                    if response.status_code >= 400:
                        broken_links.append({
                            'url': href,
                            'status_code': response.status_code,
                            'text': link.text
                        })
                except requests.RequestException as e:
                    broken_links.append({
                        'url': href,
                        'error': str(e),
                        'text': link.text
                    })
        
        return broken_links
    
    @staticmethod
    def check_images_loaded(driver):
        """Check if all images are loaded properly"""
        broken_images = []
        images = driver.find_elements(By.TAG_NAME, "img")
        
        for img in images:
            # Check if image is loaded using JavaScript
            is_loaded = driver.execute_script(
                "return arguments[0].complete && arguments[0].naturalHeight !== 0",
                img
            )
            
            if not is_loaded:
                broken_images.append({
                    'src': img.get_attribute('src'),
                    'alt': img.get_attribute('alt')
                })
        
        return broken_images
    
    @staticmethod
    def get_console_errors(driver):
        """Get JavaScript console errors"""
        logs = driver.get_log('browser')
        errors = [log for log in logs if log['level'] == 'SEVERE']
        return errors
    
    @staticmethod
    def check_responsive_elements(driver, viewport_size):
        """Check if elements are properly displayed at given viewport size"""
        driver.set_window_size(viewport_size[0], viewport_size[1])
        time.sleep(2)  # Wait for resize
        
        # Check if elements are visible and not overlapping
        elements_info = []
        important_elements = driver.find_elements(By.CSS_SELECTOR, 
            "nav, .navbar, .hero, .banner, .content, .footer, .btn, .cta")
        
        for element in important_elements:
            if element.is_displayed():
                size = element.size
                location = element.location
                elements_info.append({
                    'tag': element.tag_name,
                    'class': element.get_attribute('class'),
                    'size': size,
                    'location': location,
                    'visible': element.is_displayed()
                })
        
        return elements_info
    
    @staticmethod
    def extract_all_links(driver):
        """Extract all links from the page"""
        links = []
        link_elements = driver.find_elements(By.TAG_NAME, "a")
        
        for link in link_elements:
            href = link.get_attribute("href")
            text = link.text.strip()
            if href:
                links.append({
                    'url': href,
                    'text': text,
                    'is_external': not href.startswith(driver.current_url.split('/')[0:3])
                })
        
        return links
    
    @staticmethod
    def check_seo_elements(driver):
        """Check basic SEO elements"""
        seo_info = {}
        
        # Title
        seo_info['title'] = driver.title
        seo_info['title_length'] = len(driver.title)
        
        # Meta description
        try:
            meta_desc = driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
            seo_info['meta_description'] = meta_desc.get_attribute('content')
            seo_info['meta_description_length'] = len(seo_info['meta_description'])
        except:
            seo_info['meta_description'] = None
        
        # Headings
        headings = {}
        for i in range(1, 7):
            h_elements = driver.find_elements(By.TAG_NAME, f"h{i}")
            headings[f'h{i}'] = [h.text for h in h_elements]
        seo_info['headings'] = headings
        
        # Images without alt text
        images_without_alt = []
        images = driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            alt = img.get_attribute('alt')
            if not alt or alt.strip() == '':
                images_without_alt.append(img.get_attribute('src'))
        seo_info['images_without_alt'] = images_without_alt
        
        return seo_info