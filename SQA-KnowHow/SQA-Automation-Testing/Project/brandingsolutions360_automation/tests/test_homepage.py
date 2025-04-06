from pages.homepage import HomePage
import os

SCREENSHOTS_DIR = "screenshots"

def test_homepage_header(driver):
    homepage = HomePage(driver)
    homepage.open("https://brandingsolutions360.com/")
    try:
        assert "Branding" in homepage.get_main_heading()
    except AssertionError:
        screenshot_name = "homepage_header_failed.png"
        screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
        driver.save_screenshot(screenshot_path)
        print(f"\nScreenshot saved to: {screenshot_path}")
        raise  # Re-raise the assertion error to mark the test as failed

def test_contact_button_click(driver):
    homepage = HomePage(driver)
    homepage.open("https://brandingsolutions360.com/")
    homepage.go_to_contact()
    try:
        assert "contact" in driver.current_url.lower()
    except AssertionError:
        screenshot_name = "contact_button_failed.png"
        screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
        driver.save_screenshot(screenshot_path)
        print(f"\nScreenshot saved to: {screenshot_path}")
        raise