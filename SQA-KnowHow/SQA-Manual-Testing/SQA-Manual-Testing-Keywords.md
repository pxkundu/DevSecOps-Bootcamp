## Manual Testing in Software Quality Assurance (SQA)

Let's cover everything you need to know, using industry-standard keywords, explaining each one, and tying them to real-world examples. Manual Testing is a hands-on process, so understanding its components will give you a solid grasp of how it fits into SQA. Here we go!

---

### What is Manual Testing in SQA?
Manual Testing is the process where a tester manually executes test cases on a software application without relying on automation tools or scripts. The tester acts as an end-user, interacting with the system to verify its functionality, usability, and overall quality against defined requirements. It’s about human observation, intuition, and adaptability—key pillars of ensuring software meets both technical and user expectations.

---

### Industry-Standard Keywords in Manual Testing
Below are the critical terms you’ll encounter in SQA Manual Testing, with explanations and real-world examples.

#### 1. **Test Case**
- **Definition**: A detailed set of steps, conditions, inputs, and expected outcomes designed to verify a specific feature or function of the software.
- **Real-World Example**: For an e-commerce app, a test case might be: “Enter ‘shoes’ in the search bar, press Enter, and verify that a list of shoe products appears within 3 seconds.”
- **Usage**: Testers write test cases in tools like Excel or TestRail and follow them to ensure consistency.

#### 2. **Test Plan**
- **Definition**: A high-level document outlining the scope, objectives, resources, schedule, and approach for testing the software.
- **Real-World Example**: A test plan for a banking app might specify testing login, transfers, and balance checks over two weeks with three testers.
- **Usage**: Guides the team on what to test, when, and how—think of it as the project’s testing roadmap.

#### 3. **Test Scenario**
- **Definition**: A broader description of what to test, focusing on a specific user journey or feature, often encompassing multiple test cases.
- **Real-World Example**: “Verify the checkout process” is a test scenario for an online store, covering payment, shipping, and confirmation steps.
- **Usage**: Helps testers brainstorm test cases and ensures all critical paths are covered.

#### 4. **Test Execution**
- **Definition**: The act of running test cases and recording the results (pass/fail) based on the software’s behavior.
- **Real-World Example**: A tester logs into a social media app with invalid credentials and confirms an error message appears as expected.
- **Usage**: This is the hands-on phase where testers interact with the app and document findings.

#### 5. **Defect (Bug)**
- **Definition**: A flaw or deviation from the expected behavior that causes the software to fail its requirements.
- **Real-World Example**: Clicking “Add to Cart” on a shopping site crashes the app—that’s a defect.
- **Usage**: Testers log defects in tools like Jira with details (steps to reproduce, screenshots) for developers to fix.

#### 6. **Bug Report**
- **Definition**: A detailed document describing a defect, including steps to reproduce, actual vs. expected results, and severity.
- **Real-World Example**: “Steps: Enter ‘-1’ items in quantity field. Actual: System accepts it. Expected: Error message for invalid input.”
- **Usage**: Ensures developers have clear info to resolve issues quickly.

#### 7. **Exploratory Testing**
- **Definition**: An unscripted testing approach where testers freely explore the software to find defects, relying on experience and creativity.
- **Real-World Example**: A tester randomly taps buttons in a game app and discovers a hidden crash when pausing mid-level.
- **Usage**: Ideal for finding edge cases or when formal test cases aren’t ready.

#### 8. **Ad-Hoc Testing**
- **Definition**: Informal, unplanned testing without predefined test cases, often to quickly spot obvious issues.
- **Real-World Example**: A tester tries a new feature in a chat app (e.g., sending emojis) and notices they don’t display correctly.
- **Usage**: Used in early builds or tight deadlines to catch glaring problems.

#### 9. **Regression Testing**
- **Definition**: Re-testing previously working features after a change (e.g., bug fix or update) to ensure nothing broke.
- **Real-World Example**: After fixing a login bug, the tester re-checks registration and password reset to confirm they still work.
- **Usage**: Ensures stability as the software evolves.

#### 10. **Smoke Testing**
- **Definition**: A quick, surface-level test to verify the basic functionality of the system works before deeper testing.
- **Real-World Example**: For a video app, testers check if it launches and plays a sample video without crashing.
- **Usage**: Acts as a “build acceptance” check after a new release.

#### 11. **Sanity Testing**
- **Definition**: A narrow, focused test to confirm a specific fix or feature works, without exhaustive checks.
- **Real-World Example**: After fixing a payment bug, testers verify only the payment flow works as expected.
- **Usage**: Quick validation post-fix to avoid full regression testing if unnecessary.

#### 12. **Usability Testing**
- **Definition**: Evaluating how intuitive and user-friendly the software is from an end-user perspective.
- **Real-World Example**: A tester notes that a “Submit” button is too small to tap easily on a mobile app.
- **Usage**: Ensures the software isn’t just functional but also practical for real people.

#### 13. **Functional Testing**
- **Definition**: Verifying that the software performs its intended functions according to requirements.
- **Real-World Example**: Testing a calculator app to ensure “2 + 2” equals “4.”
- **Usage**: Core of manual testing—checks the “what” of the software.

#### 14. **Non-Functional Testing**
- **Definition**: Assessing aspects like performance, reliability, or accessibility, often subjective in manual contexts.
- **Real-World Example**: A tester observes if a website feels sluggish on a slow network.
- **Usage**: Complements functional testing for a well-rounded quality check.

#### 15. **Test Coverage**
- **Definition**: The extent to which the software’s features, code, or requirements are tested.
- **Real-World Example**: Ensuring all menu options in a restaurant app (order, pay, track) are tested at least once.
- **Usage**: Measures how thorough the testing effort is.

#### 16. **Test Data**
- **Definition**: The inputs used during testing to simulate real-world usage.
- **Real-World Example**: Using fake emails (e.g., “test123@gmail.com”) to test a signup form.
- **Usage**: Testers prepare or generate data to cover valid, invalid, and edge cases.

#### 17. **Boundary Testing**
- **Definition**: Testing the limits or edge cases of input ranges to find defects at extremes.
- **Real-World Example**: Entering “999999” items in a cart to see if the system handles large numbers.
- **Usage**: Catches bugs at the fringes of acceptable behavior.

#### 18. **Positive Testing**
- **Definition**: Testing with valid inputs to confirm the software works as expected.
- **Real-World Example**: Entering a correct username and password to log in successfully.
- **Usage**: Verifies the happy path works.

#### 19. **Negative Testing**
- **Definition**: Testing with invalid inputs to ensure the software handles errors gracefully.
- **Real-World Example**: Entering “abc” in a phone number field and checking for an error message.
- **Usage**: Ensures robustness against bad data.

#### 20. **Test Environment**
- **Definition**: The setup (hardware, software, network) where testing occurs, mimicking production as closely as possible.
- **Real-World Example**: Testing a mobile app on an iPhone 13 with iOS 18 and Wi-Fi.
- **Usage**: Ensures results reflect real-world conditions.

#### 21. **Traceability Matrix**
- **Definition**: A document linking requirements to test cases to ensure everything’s covered.
- **Real-World Example**: A table showing “Requirement: User can log out” ties to “Test Case: Verify logout button works.”
- **Usage**: Tracks coverage and compliance with specs.

#### 22. **Severity**
- **Definition**: The impact of a defect on the system (e.g., critical, major, minor).
- **Real-World Example**: A crash on launch is “critical”; a misspelled label is “minor.”
- **Usage**: Prioritizes bug fixes for developers.

#### 23. **Priority**
- **Definition**: The urgency of fixing a defect, often based on business needs.
- **Real-World Example**: A payment failure is “high priority,” even if severity is moderate.
- **Usage**: Guides the order of fixes when time’s tight.

---

### The Manual Testing Process
Here’s how it flows in SQA:
1. **Requirement Analysis**: Testers study specs to understand what to test.
2. **Test Planning**: Define scope, resources, and timelines.
3. **Test Case Design**: Write detailed steps for each feature.
4. **Test Environment Setup**: Prepare devices, browsers, or servers.
5. **Test Execution**: Run the tests, observe, and log results.
6. **Defect Reporting**: Document bugs for devs to fix.
7. **Retesting**: Verify fixes and run regression tests.
8. **Reporting**: Summarize pass/fail rates and quality status.

---

### Real-World Application
Imagine testing a new email app:
- **Test Scenario**: Sending an email.
- **Test Case**: “Enter valid recipient, subject, body; click Send; verify email appears in Sent folder.”
- **Exploratory Testing**: Try attaching a 10GB file—what happens?
- **Defect**: “App crashes with large attachments.”
- **Bug Report**: “Steps: Attach 10GB file, click Send. Actual: Crash. Expected: Error message.”
- **Regression**: After the fix, re-test sending normal emails.

---

### Pros and Cons Recap
- **Pros**: Flexible, human-driven, catches subjective flaws.
- **Cons**: Slow, repetitive, prone to oversight.

---
