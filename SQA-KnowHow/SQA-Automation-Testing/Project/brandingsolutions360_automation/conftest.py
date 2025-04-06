import pytest
from utils.driver_factory import get_driver
import os
import allure

SCREENSHOTS_DIR = "screenshots"

def pytest_addoption(parser):
    parser.addoption(
        "--screenshot_on_fail",
        action="store_true",
        default=False,
        help="Capture screenshot on test failure",
    )

@pytest.fixture(scope="function")
def driver(request):
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    if rep.when == "call" and rep.failed and item.config.getoption("--screenshot_on_fail"):
        try:
            driver = item.funcargs["driver"]  # Access the driver instance
            screenshot_name = f"{item.name}.png"
            screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
            driver.save_screenshot(screenshot_path)
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(f"Failed to capture screenshot or attach to Allure: {e}")