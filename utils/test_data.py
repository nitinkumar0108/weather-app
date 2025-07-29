"""
Test data for various test scenarios
"""

class TestData:
    # URLs to test
    EXTERNAL_LINKS = [
        "https://google.com",
        "https://github.com",
        "https://linkedin.com"
    ]
    
    # Form test data
    CONTACT_FORM_DATA = {
        "valid": {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test Inquiry",
            "message": "This is a test message for exploratory testing."
        },
        "invalid": {
            "name": "",
            "email": "invalid-email",
            "subject": "",
            "message": ""
        }
    }
    
    # Search terms
    SEARCH_TERMS = [
        "blockchain",
        "kalp",
        "network",
        "technology",
        "services"
    ]
    
    # Browser viewport sizes for responsive testing
    VIEWPORT_SIZES = [
        (1920, 1080),  # Desktop
        (1366, 768),   # Laptop
        (768, 1024),   # Tablet
        (375, 667),    # Mobile
    ]
    
    # Performance thresholds
    PERFORMANCE_THRESHOLDS = {
        "page_load_time": 5.0,  # seconds
        "element_load_time": 3.0,  # seconds
    }