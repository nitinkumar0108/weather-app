# Kalp Network Exploratory Testing Framework

A comprehensive Selenium-based testing framework for exploratory testing of the Kalp Network website (https://kalp.network/).

## Features

- **Page Object Model**: Clean, maintainable test structure
- **Comprehensive Testing**: Covers functionality, performance, accessibility, and SEO
- **Cross-browser Support**: Chrome and Firefox support
- **Responsive Testing**: Tests across multiple viewport sizes
- **Visual Documentation**: Automatic screenshots on failures and key test points
- **Detailed Reporting**: HTML reports with test results and screenshots
- **Exploratory Scenarios**: Random link exploration, form testing, keyboard navigation

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment** (Optional):
   Create a `.env` file to customize settings:
   ```
   BROWSER=chrome
   HEADLESS=false
   ```

## Running Tests

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test Categories
```bash
# Home page tests only
python -m pytest tests/test_home_page.py -v

# Exploratory tests only
python -m pytest tests/test_exploratory.py -v

# Run with specific browser
BROWSER=firefox python run_tests.py

# Run in headless mode
HEADLESS=true python run_tests.py
```

## Test Categories

### 1. Home Page Tests (`test_home_page.py`)
- **Page Loading**: Verifies successful page load and basic elements
- **Navigation**: Tests navigation menu functionality
- **Responsive Design**: Tests across different viewport sizes
- **Performance**: Measures and validates page load times
- **Link Validation**: Checks for broken links
- **Image Loading**: Verifies all images load properly
- **Console Errors**: Monitors JavaScript errors
- **SEO Elements**: Validates title, meta description, headings
- **Social Media Links**: Tests social media link presence and validity
- **CTA Buttons**: Tests call-to-action button functionality
- **Accessibility**: Basic accessibility checks

### 2. Exploratory Tests (`test_exploratory.py`)
- **Random Link Exploration**: Randomly navigates through internal links
- **Form Interactions**: Tests form fields and validation
- **Keyboard Navigation**: Tests tab navigation and keyboard accessibility
- **Browser Navigation**: Tests back/forward functionality
- **Zoom Functionality**: Tests page behavior at different zoom levels
- **Page Refresh**: Validates page state after refresh
- **Context Menu**: Tests right-click functionality
- **Text Selection**: Tests text selection capabilities
- **Scroll Behavior**: Tests various scrolling scenarios

## Framework Structure

```
├── config/
│   └── config.py              # Configuration settings
├── pages/
│   └── home_page.py           # Page object models
├── utils/
│   ├── base_page.py           # Base page class
│   ├── helpers.py             # Test helper utilities
│   └── test_data.py           # Test data constants
├── tests/
│   ├── conftest.py            # Pytest configuration
│   ├── test_home_page.py      # Home page tests
│   └── test_exploratory.py    # Exploratory test scenarios
├── screenshots/               # Test screenshots
├── reports/                   # HTML test reports
├── requirements.txt           # Python dependencies
├── run_tests.py              # Test runner script
└── README.md                 # This file
```

## Key Features

### Automatic Screenshots
- Screenshots taken on test failures
- Visual verification screenshots during tests
- Responsive design screenshots at different viewport sizes

### Performance Monitoring
- Page load time measurement
- Performance threshold validation
- Console error monitoring

### Accessibility Testing
- Alt text validation for images
- Form label checking
- Keyboard navigation testing

### SEO Validation
- Title and meta description analysis
- Heading structure validation
- Image alt text compliance

## Configuration Options

### Browser Settings
- **BROWSER**: `chrome` (default) or `firefox`
- **HEADLESS**: `true` or `false` (default)

### Timeouts
- **IMPLICIT_WAIT**: 10 seconds (default)
- **EXPLICIT_WAIT**: 20 seconds (default)
- **PAGE_LOAD_TIMEOUT**: 30 seconds (default)

### Performance Thresholds
- **Page Load Time**: 5 seconds (default)
- **Element Load Time**: 3 seconds (default)

## Reports and Artifacts

### HTML Reports
- Detailed test execution reports
- Test results with pass/fail status
- Execution time and error details
- Located in `reports/` directory

### Screenshots
- Failure screenshots with timestamps
- Visual verification screenshots
- Responsive design screenshots
- Located in `screenshots/` directory

## Extending the Framework

### Adding New Page Objects
1. Create new page class in `pages/` directory
2. Extend `BasePage` class
3. Define page-specific locators and methods

### Adding New Tests
1. Create test file in `tests/` directory
2. Import required page objects and utilities
3. Use pytest fixtures for setup

### Custom Test Data
- Modify `utils/test_data.py` for test-specific data
- Add new test scenarios in respective test files

## Best Practices

1. **Page Object Model**: Keep page-specific logic in page objects
2. **Explicit Waits**: Use explicit waits for better reliability
3. **Error Handling**: Implement proper exception handling
4. **Screenshots**: Take screenshots for visual verification
5. **Logging**: Use print statements for test execution tracking

## Troubleshooting

### Common Issues
1. **WebDriver Issues**: Ensure ChromeDriver/GeckoDriver is properly installed
2. **Timeout Errors**: Increase timeout values in config if needed
3. **Element Not Found**: Check if page structure has changed
4. **Permission Errors**: Ensure write permissions for screenshots and reports directories

### Debug Mode
Run tests with verbose output:
```bash
python -m pytest tests/ -v -s --tb=long
```

This framework provides comprehensive exploratory testing capabilities for the Kalp Network website, ensuring functionality, performance, and user experience quality across different scenarios and environments.