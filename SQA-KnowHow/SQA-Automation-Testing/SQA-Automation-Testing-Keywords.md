### SQA Automation Testing Keywords and Use Cases

#### 1. **Test Automation**
- **Definition**: The process of using software tools to execute predefined test cases automatically, validate outcomes, and report results.
- **Industry Use Case**: At J&J, automate regression testing for Janssen Medical Cloud’s patient portal using Selenium to ensure login functionality remains stable across updates, reducing manual effort from 10 hours to 30 minutes per cycle.

#### 2. **Test Script**
- **Definition**: A coded sequence of instructions that automates a test case, written in languages like JavaScript, Python, or Java.
- **Industry Use Case**: A Cypress script for Calysta Pro EMR automates patient record retrieval (`cy.get('#record-id').type('123'); cy.get('#fetch').click();`), ensuring IEC 62304-compliant data accuracy with each sprint.

#### 3. **Test Case**
- **Definition**: A specific scenario or condition to be tested, with inputs, execution steps, and expected results, automated via scripts.
- **Industry Use Case**: For Janssen With Me, an automated test case checks “Enter valid clinician credentials, expect dashboard in <2 seconds,” executed nightly via Jenkins to meet performance SLAs.

#### 4. **Test Automation Framework**
- **Definition**: A structured set of guidelines, tools, and libraries to organize and execute automated tests efficiently.
- **Industry Use Case**: Novartis uses a data-driven framework with Selenium and TestNG to test a pharmacovigilance system, pulling adverse event data from a CSV to verify EudraVigilance compliance across 1,000 scenarios.

#### 5. **Regression Testing**
- **Definition**: Automated re-testing of previously validated functionality to ensure new changes don’t introduce defects.
- **Industry Use Case**: After a J&J update to Calysta Pro EMR, a Selenium suite re-runs 500 UI and API tests in Jenkins, confirming no regressions in patient data sync per ISO 13485.

#### 6. **Functional Testing**
- **Definition**: Automating verification that software features work as per requirements.
- **Industry Use Case**: AstraZeneca automates functional testing of a trial enrollment app with Cypress, ensuring “Submit patient consent” triggers a database update, traceable to GCP standards.

#### 7. **Non-Functional Testing**
- **Definition**: Automating tests for performance, security, or usability aspects beyond core functionality.
- **Industry Use Case**: J&J uses JMeter to automate load testing on Janssen Medical Cloud, simulating 1,000 clinicians to ensure <3-second response times under IEC 81001-5-1 cybersecurity guidelines.

#### 8. **Continuous Integration/Continuous Deployment (CI/CD)**
- **Definition**: Automating test execution as part of a pipeline triggered by code commits or deployments.
- **Industry Use Case**: Your work at SJ Innovation integrated Cypress tests into GitHub Actions for Janssen With Me, running UI checks on every pull request, cutting regression time by 40%.

#### 9. **Test Data Management**
- **Definition**: Preparing, generating, or maintaining data for automated tests (e.g., synthetic, anonymized).
- **Industry Use Case**: Sanofi automates patient record tests in a trial system with Python scripts pulling GDPR-compliant fake data from a database, ensuring ISO 14971 risk controls are met.

#### 10. **Assertions**
- **Definition**: Code statements that verify expected test outcomes (e.g., “element exists,” “value equals X”).
- **Industry Use Case**: A Postman script for Calysta Pro asserts API response `{ "status": "success" }` after saving a record, logged for GMP Annex 11 audits.

#### 11. **Parallel Testing**
- **Definition**: Running multiple automated tests simultaneously to reduce execution time.
- **Industry Use Case**: Roche uses Selenium Grid to test a diagnostics dashboard across Chrome, Firefox, and Edge in parallel, ensuring ISO 13485 compliance in under an hour vs. 3 hours sequentially.

#### 12. **Smoke Testing**
- **Definition**: A quick, automated check of basic functionality to confirm a build is stable.
- **Industry Use Case**: J&J automates smoke tests with Cypress for Janssen Medical Cloud, verifying login and dashboard load post-deploy, acting as a gatekeeper for deeper testing.

#### 13. **Sanity Testing**
- **Definition**: Focused automation to verify specific fixes or features work without full regression.
- **Industry Use Case**: After fixing a Calysta Pro bug, a Selenium script checks only the updated prescription module, ensuring IEC 62304 compliance in 10 minutes.

#### 14. **Exploratory Testing (Hybrid)**:
- **Definition**: Combining manual exploration with automation to script discovered scenarios.
- **Industry Use Case**: You manually explore Janssen With Me’s UI, find a lag, then automate it with Cypress (`cy.wait(5000).should('not.exist')`), enhancing test coverage.

#### 15. **Performance Testing**
- **Definition**: Automating tests to measure speed, scalability, and stability under load.
- **Industry Use Case**: Novartis uses JMeter to automate stress tests on a drug inventory system, ensuring it handles 500 simultaneous users per GMP performance requirements.

#### 16. **Security Testing**
- **Definition**: Automating checks for vulnerabilities (e.g., SQL injection, data leaks).
- **Industry Use Case**: J&J automates API security tests with Postman for Calysta Pro, asserting no unencrypted patient data escapes, meeting GDPR and IEC 81001-5-1 standards.

#### 17. **Test Coverage**
- **Definition**: The percentage of application features or code exercised by automated tests.
- **Industry Use Case**: AstraZeneca targets 90% test coverage for a trial app’s critical paths (e.g., data entry) using Selenium, tracked in TestRail for ISO 13485 validation.

#### 18. **Defect Tracking**
- **Definition**: Automating defect logging and monitoring post-test execution.
- **Industry Use Case**: Your J&J work used Jira to auto-log Cypress failures (e.g., “Dashboard failed to load”) with screenshots, speeding up triaging for devs.

#### 19. **Risk-Based Testing**
- **Definition**: Automating tests prioritized by risk to users or compliance.
- **Industry Use Case**: Roche automates high-risk ventilator UI tests (e.g., alarm triggers) with Selenium, aligning with ISO 14971 risk management, over lower-risk settings.

#### 20. **Traceability**
- **Definition**: Linking automated tests to requirements for auditability.
- **Industry Use Case**: J&J maps Calysta Pro’s automated Cypress tests to IEC 62304 requirements in TestRail, proving compliance during an EMA audit.

#### 21. **Flaky Tests**
- **Definition**: Automated tests that unpredictably pass or fail due to timing or environment issues.
- **Industry Use Case**: Sanofi debugs flaky Selenium tests for a trial system (e.g., UI load delays), adding retries (`driver.wait()`) to ensure GMP-consistent results.

#### 22. **Test Environment**
- **Definition**: The automated setup (e.g., VMs, containers) mimicking production for testing.
- **Industry Use Case**: Novartis runs Selenium tests in Docker containers simulating clinic servers, ensuring Calysta Pro’s cloud sync meets ISO 13485 in a controlled environment.

#### 23. **Headless Testing**
- **Definition**: Running automated browser tests without a visible UI for speed.
- **Industry Use Case**: J&J uses headless Chrome with Selenium to test Janssen Medical Cloud’s backend interactions, cutting CI/CD runtime by 50%.

#### 24. **API Testing**
- **Definition**: Automating verification of application programming interfaces.
- **Industry Use Case**: Your Postman scripts at SJ Innovation tested Calysta Pro’s API endpoints (e.g., `POST /patient`), ensuring data integrity for GMP compliance.

#### 25. **Validation**
- **Definition**: Proving automated tests meet their intended purpose for regulatory use.
- **Industry Use Case**: Roche validates a Cypress suite for a diagnostics tool with OQ (Operational Qualification), documenting results for IEC 62304 sign-off.

---

### Industry Context: Pharma and Your Background
- **Regulatory Tie-In**: Keywords like **Traceability**, **Validation**, and **Risk-Based Testing** are critical for J&J’s medical software (e.g., Janssen With Me), ensuring EMA/FDA compliance.
- **Your Skills**: Your experience with **CI/CD** (Jenkins, GitHub Actions), **API Testing** (Postman), and **Web Technologies** (React.js) directly supports tools like Cypress and Selenium, while **Defect Tracking** (Jira) and **Regression Testing** match your J&J QA work.
- **Pharma Use Cases**: Automation here focuses on patient safety (e.g., **Performance Testing** for real-time systems), data security (e.g., **Security Testing** for GDPR), and audit readiness (e.g., **Traceability** for ISO 13485).

---

### Example Workflow at J&J
- **Scenario**: Automating Calysta Pro EMR’s patient record feature.
- **Keywords in Action**:
  - **Test Automation**: Cypress scripts run UI tests.
  - **Test Case**: “Save record, expect success message.”
  - **CI/CD**: Jenkins triggers on commits.
  - **Assertions**: `cy.get('#success').should('be.visible')`.
  - **Traceability**: Linked to IEC 62304 in TestRail.
  - **Defect Tracking**: Failures logged in Jira.
  - **Result**: 95% pass rate, validated for clinical use.

---

### How to Apply This
- **Learn**: Experiment with a **Data-Driven Framework** using Cypress and a CSV—mimics J&J’s scale.
- **Practice**: Automate a **Regression Testing** suite for a React.js app you’ve built, integrating with GitHub Actions.
- **Pharma Focus**: Add **Traceability** by documenting a test-to-requirement link in a spreadsheet.

---
