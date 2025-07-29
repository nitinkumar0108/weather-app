"""
Pytest configuration and fixtures
"""
import pytest
import os
from datetime import datetime
from config.config import Config
from pages.home_page import HomePage

@pytest.fixture(scope="session")
def setup_directories():
    """Setup test directories"""
    directories = [Config.SCREENSHOT_DIR, Config.REPORT_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

@pytest.fixture(scope="function")
def driver(setup_directories):
    """WebDriver fixture"""
    driver = Config.get_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def home_page(driver):
    """Home page fixture"""
    page = HomePage(driver)
    page.load()
    return page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        if hasattr(item, "funcargs") and "driver" in item.funcargs:
            driver = item.funcargs["driver"]
            if Config.SCREENSHOT_ON_FAILURE:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"FAILED_{item.name}_{timestamp}"
                screenshot_path = os.path.join(Config.SCREENSHOT_DIR, f"{screenshot_name}.png")
                driver.save_screenshot(screenshot_path)
                print(f"\nScreenshot saved: {screenshot_path}")

def pytest_configure(config):
    """Configure pytest"""
    if not os.path.exists(Config.REPORT_DIR):
        os.makedirs(Config.REPORT_DIR)

def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Kalp Network - Exploratory Test Report"