# BrandingSolutions360 Selenium Automation Framework

Automation test suite using Selenium + Python (POM based).

---

### 💡 What is POM (Page Object Model)?

POM is a **design pattern** that:
- Creates a **class for each web page** in your app.
- Separates **locators**, **actions**, and **tests** cleanly.
- Promotes **code reusability**, **maintainability**, and **scalability**.

---

### 📁 Project Structure Overview

```bash
brandingsolutions360_automation/
├── README.md                # Project documentation
├── requirements.txt         # Required Python packages
├── .env                     # Placeholder for environment variables
├── conftest.py              # Global pytest fixture for driver setup, screenshot on failure
├── pytest.ini               # Pytest configurations
├── tests/
│   └── test_homepage.py     # Test cases for homepage
├── pages/
│   ├── base_page.py         # Base page methods (click, get_text, open)
│   └── homepage.py          # Page class for homepage with actions
├── locators/
│   └── homepage_locators.py # Web element locators for homepage
├── utils/
│   ├── driver_factory.py    # Chrome WebDriver setup
│   └── screenshot_utils.py  # Utility function for saving screenshots
└── screenshots/             # Screenshots captured on test failure
```

---

### 🧑‍💻 Instructions to Run This Project Locally

Follow these detailed steps to set up and run the automation tests on your local machine.

#### ✅ 1. Clone or Generate Project Structure

If you haven't already, ensure you have the project files. If you used the provided `bash` script, the `brandingsolutions360_automation` directory and its contents should have been created. If you cloned from a repository, navigate to the project's root directory in your terminal:

```bash
cd brandingsolutions360_automation
```

#### ✅ 2. Create and Activate a Python Virtual Environment

It's highly recommended to use a virtual environment to isolate the project's dependencies.

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows CMD
```

Your terminal prompt should now be prefixed with `(venv)`, indicating that the virtual environment is active.

#### ✅ 3. Install Dependencies

Install the required Python packages listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install `selenium`, `pytest`, and `python-dotenv`.

#### ✅ 4. Set Up ChromeDriver

Selenium requires a browser driver to interact with the browser. This project is configured for Google Chrome.

- **Download ChromeDriver:** Go to https://chromedriver.chromium.org/downloads and download the ChromeDriver that matches the version of your Google Chrome browser. You can check your Chrome version by opening Chrome, clicking on the three dots (menu), going to "Help," and then "About Google Chrome."

- **Ensure ChromeDriver is in your system path:** The easiest way for Selenium to find ChromeDriver is if it's in a directory that's included in your system's PATH environment variable. Common locations include:
    - `/usr/local/bin`
    - `/usr/bin`
    - `C:\Windows`
    - `C:\Windows\System32`

    You can either move the downloaded `chromedriver` executable to one of these directories or add the directory where you saved it to your PATH.

    **Verification:** Open a new terminal window and run:
    ```bash
    which chromedriver     # macOS/Linux
    where chromedriver     # Windows CMD
    ```
    This command should output the path to the `chromedriver` executable if it's correctly configured in your PATH.

#### ✅ 5. Run the Tests and Generate Reports

You can run the tests using `pytest`. Here's how to generate different types of reports and save outputs:

##### 5.1. Basic Test Execution

To run all tests in the `tests/` directory:

```bash
pytest
```

Pytest will execute the test functions in `tests/test_homepage.py` and display the results in the terminal. The `--capture=tee-sys --tb=short` options in `pytest.ini` control how output and tracebacks are displayed.

##### 5.2. Saving Screenshots on Test Failure

The `conftest.py` file is already set up to capture screenshots when a test fails and the `--screenshot_on_fail` flag is used.

```bash
pytest --screenshot_on_fail tests/
```

This command will run the tests, and if any test fails, a screenshot will be saved in the `screenshots/` directory with the name of the failed test.

##### 5.3. Generating HTML Reports with `pytest-html`

To generate a self-contained HTML report of your test execution:

1.  **Install `pytest-html`:**
    ```bash
    pip install pytest-html
    ```

2.  **Run tests with the `--html` option:**
    ```bash
    pytest --html=report.html --self-contained-html tests/
    ```

    This command will create an HTML file named `report.html` in your project's root directory, which you can open in your web browser to view the test results.

##### 5.4. Generating Allure Reports with `allure-pytest`

Allure is a powerful reporting framework that provides detailed and interactive test reports.

1.  **Install `allure-pytest`:**
    ```bash
    pip install allure-pytest
    ```

2.  **Install the Allure command-line tool:** Follow the instructions in the previous response to install the `allure` command-line tool for your operating system (using Homebrew, SDKMAN!, Snap, or manual download).

3.  **Run tests with the `--alluredir` option:**
    ```bash
    pytest --alluredir=allure-results tests/
    ```

    This command will generate the raw Allure report data in the `allure-results` directory.

4.  **Generate and open the Allure report:**
    ```bash
    allure serve allure-results
    ```

    This command will start an Allure server and automatically open the generated report in your default web browser. You can also generate a static HTML report:

    ```bash
    allure generate allure-results -o allure-report --clean
    ```

    This will create an `allure-report` directory containing the static HTML report. Open `allure-report/index.html` in your browser to view it.

    **Integrating Screenshots with Allure:** Ensure your `conftest.py` includes the necessary code to attach screenshots to the Allure report on test failure (as provided in the previous detailed response).

#### ✅ 6. (Optional) Save a Screenshot on Failure (Detailed Implementation)

Here's the detailed implementation of the `pytest` hook in `conftest.py` to save screenshots on failure:

1.  **Ensure `screenshots/` directory exists:** The `bash` script should have created this. If not, create it manually:
    ```bash
    mkdir screenshots
    ```

2.  **Verify `conftest.py` content:** Your `conftest.py` should look like this (including Allure integration for comprehensive reporting):

    ```python
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
    ```

3.  **Run tests with the screenshot option:**
    ```bash
    pytest --screenshot_on_fail --alluredir=allure-results tests/
    allure serve allure-results
    ```

    Now, if a test fails, a screenshot will be saved in the `screenshots/` directory and attached to the corresponding failed test case in the Allure report.

---

### 🧪 Example Test Flow

The file `tests/test_homepage.py` contains example test cases:
- **`test_homepage_header(driver)`:** Opens the homepage (`https://brandingsolutions360.com/`) and asserts that the main heading (H1 tag) contains the text "Branding".
- **`test_contact_button_click(driver)`:** Opens the homepage, clicks the "Contact" button, and asserts that the current URL contains the word "contact" (case-insensitive).

---

### 🧰 Additional Tips

- **Running in Headless Mode:** To run Chrome without a visible UI (useful for CI environments), modify the `get_driver` function in `utils/driver_factory.py`:

  ```python
  from selenium import webdriver
  from selenium.webdriver.chrome.options import Options

  def get_driver():
      options = Options()
      options.add_argument("--start-maximized")
      options.add_argument("--headless")  # Enable headless mode
      driver = webdriver.Chrome(options=options)
      return driver
  ```

- **Environment Variables:** You can use the `.env` file (with the `python-dotenv` package) to manage environment-specific configurations like URLs or browser settings. Load them in your `conftest.py` or test files.

- **Logging:** For more detailed debugging information, consider integrating Python's built-in `logging` module into your framework.

---
