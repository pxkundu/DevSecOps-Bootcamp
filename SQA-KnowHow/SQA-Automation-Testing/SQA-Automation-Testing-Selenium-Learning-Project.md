Let’s create a simple learning project for **SQA Automation Testing** using **Selenium with Python**, following the **Page Object Model (POM)** method. 

POM is an industry-standard design pattern that enhances test maintainability and readability by separating test logic from page-specific details—perfect for your background with Janssen & Janssen and your goal to master automation for a European pharma SQA role. 

This project will simulate testing a basic web application (we’ll use a public demo site), aligning with your skills in Python, web technologies, and QA.

---

### Project Overview
- **Goal**: Automate testing of a login page on a demo site (e.g., `https://the-internet.herokuapp.com/login`).
- **Tool**: Selenium WebDriver with Python.
- **Pattern**: Page Object Model (POM) to organize code.
- **Features Tested**: Valid login, invalid login.
- **Outcome**: A reusable, modular test suite with clear separation of concerns.

---

### Prerequisites
1. **Python**: Installed (3.7+ recommended).
2. **Selenium**: Install via `pip install selenium`.
3. **WebDriver**: Download ChromeDriver (matches your Chrome version) from [here](https://chromedriver.chromium.org/downloads) and add it to your system PATH.
4. **IDE**: Use PyCharm, VS Code, or any editor you prefer.

---

### Project Structure
```
selenium_pom_project/
├── pages/                  # Page objects (POM classes)
│   ├── base_page.py       # Base class for common methods
│   └── login_page.py      # Login page-specific elements and actions
├── tests/                 # Test scripts
│   └── test_login.py      # Test cases
├── requirements.txt       # Dependencies
└── README.md              # Project info
```

---

### Step-by-Step Implementation

#### 1. Setup Environment
- Create a new directory: `selenium_pom_project`.
- Initialize a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # Mac/Linux
  venv\Scripts\activate     # Windows
  ```
- Install Selenium:
  ```bash
  pip install selenium
  ```
- Create `requirements.txt`:
  ```
  selenium==4.10.0
  ```
- Install from it: `pip install -r requirements.txt`.

---

#### 2. Create Base Page (BasePage Class)
- File: `pages/base_page.py`
- Purpose: A parent class with common methods (e.g., finding elements), inherited by all page objects.
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def find_element(self, locator):
        """Wait for and return an element."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        """Click an element."""
        self.find_element(locator).click()

    def enter_text(self, locator, text):
        """Enter text into an element."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
```

---

#### 3. Create Login Page (LoginPage Class)
- File: `pages/login_page.py`
- Purpose: Encapsulates the login page’s elements and actions (e.g., entering credentials, submitting).
```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators (using By class for Selenium)
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "flash")
    ERROR_MESSAGE = (By.CLASS_NAME, "flash")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Navigate to the login page."""
        self.driver.get("https://the-internet.herokuapp.com/login")

    def login(self, username, password):
        """Perform login action."""
        self.enter_text(self.USERNAME_FIELD, username)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    def get_success_message(self):
        """Return success message text if present."""
        return self.find_element(self.SUCCESS_MESSAGE).text

    def get_error_message(self):
        """Return error message text if present."""
        return self.find_element(self.ERROR_MESSAGE).text
```

---

#### 4. Create Test Cases
- File: `tests/test_login.py`
- Purpose: Defines test scenarios using the LoginPage class, with assertions for pass/fail.
```python
import unittest
from selenium import webdriver
from pages.login_page import LoginPage

class TestLogin(unittest.TestCase):
    def setUp(self):
        """Setup WebDriver before each test."""
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.login_page.open()

    def tearDown(self):
        """Cleanup after each test."""
        self.driver.quit()

    def test_valid_login(self):
        """Test login with valid credentials."""
        self.login_page.login("tomsmith", "SuperSecretPassword!")
        success_msg = self.login_page.get_success_message()
        self.assertIn("You logged into a secure area!", success_msg)

    def test_invalid_login(self):
        """Test login with invalid credentials."""
        self.login_page.login("wronguser", "wrongpass")
        error_msg = self.login_page.get_error_message()
        self.assertIn("Your username is invalid!", error_msg)

if __name__ == "__main__":
    unittest.main()
```

---

#### 5. Add README
- File: `README.md`
```markdown
# Selenium POM Learning Project
A simple automation project using Selenium with Python and Page Object Model (POM) to test a login page.

## Setup
1. Install Python 3.7+.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies: `pip install -r requirements.txt`.
4. Download ChromeDriver and add to PATH.

## Running Tests
- Run: `python tests/test_login.py`
- Tests: Valid login, invalid login on `https://the-internet.herokuapp.com/login`.

## Structure
- `pages/`: POM classes (BasePage, LoginPage).
- `tests/`: Test scripts.
```

---

### How It Works (POM in Action)
- **Separation**: `LoginPage` handles page-specific logic (locators, actions), while `test_login.py` focuses on test scenarios—clean and maintainable.
- **Reusability**: The `login()` method can be reused across tests (e.g., valid, invalid, edge cases).
- **Scalability**: Add more pages (e.g., DashboardPage) or tests without cluttering code.
- **Pharma Tie-In**: Imagine this as a J&J medical portal—locators could target patient login fields, with assertions for GDPR compliance (e.g., masked data).

---

### Running the Project
1. Ensure ChromeDriver is in your PATH.
2. Activate the virtual environment: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows).
3. Run the tests:
   ```bash
   python tests/test_login.py
   ```
4. Output:
   - `test_valid_login`: Passes if “secure area” message appears.
   - `test_invalid_login`: Passes if “invalid” error appears.

---

### Why POM?
- **Maintainability**: Update locators in `LoginPage` if the UI changes, not in every test.
- **Readability**: Tests read like stories (e.g., `login_page.login()`), not low-level Selenium commands.
- **Your Fit**: Aligns with your SDLC and frontend experience—structuring code is second nature from React.js projects.

---

### Extending the Project (Next Steps)
1. **Add Data-Driven Testing**:
   - Use a CSV with usernames/passwords, loop through in `test_login.py`.
   - Example: `pytest` with `parametrize` for multiple credentials.
2. **CI/CD Integration**:
   - Add a GitHub Actions workflow to run tests on push, like your J&J Jenkins setup.
3. **Pharma Context**:
   - Mock a medical login (e.g., clinician credentials), assert ISO 13485-compliant error messages.
4. **More Tests**:
   - Test logout, password reset, or timeout scenarios.

---

### Example Output
```plaintext
....
----------------------------------------------------------------------
Ran 2 tests in 5.123s

OK
```

---

### Your Learning Takeaways
- **Selenium Basics**: WebDriver setup, element interaction, waits.
- **POM Mastery**: Modular design, reusable page objects.
- **Python Skills**: Classes, inheritance, unittest—leverages your C/Python background.
- **Pharma Relevance**: Structured automation ready for J&J’s regulatory needs (e.g., traceability in TestRail).

---
