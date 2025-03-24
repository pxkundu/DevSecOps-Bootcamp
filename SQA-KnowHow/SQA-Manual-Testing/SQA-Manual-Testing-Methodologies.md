**Manual Testing Methodologies** used in Fortune 100 medical and pharmaceutical companies, such as Johnson & Johnson (J&J), Pfizer, Merck, or Eli Lilly, with a focus on how these methodologies ensure the quality of software critical to healthcare—think drug development systems, clinical trial management software, or medical device interfaces. 

These companies operate in a highly regulated environment (e.g., FDA, HIPAA, GxP), so their manual testing practices are rigorous, compliance-driven, and tailored to patient safety and data integrity. 

I’ll break this down using industry-standard keywords, explain their meanings, and provide use cases specific to this sector.

---

### Context: Manual Testing in Medical/Pharma Companies
In companies like J&J, manual testing is vital for software that can’t fully rely on automation due to complexity, regulatory scrutiny, or human judgment needs—like validating user interfaces for clinicians or ensuring a drug tracking system meets Good Manufacturing Practices (GMP). While automation is growing, manual testing remains a cornerstone for exploratory, usability, and ad-hoc checks, especially in early development or for systems with frequent regulatory updates.

---

### Manual Testing Methodologies
Here are the key methodologies and keywords, tailored to Fortune 100 medical/pharma contexts:

#### 1. **Test Case Development**
- **Definition**: Writing detailed, step-by-step instructions to verify software functionality against requirements.
- **Use Case**: At J&J, testers might develop test cases for a clinical trial management system (e.g., “Enter patient ID, verify HIPAA-compliant data masking works”). These are aligned with FDA 21 CFR Part 11 for electronic records.
- **Industry Twist**: Test cases often include traceability to regulatory requirements, ensuring every feature (e.g., adverse event reporting) is validated.

#### 2. **Test Plan**
- **Definition**: A comprehensive document outlining testing scope, objectives, resources, and timelines.
- **Use Case**: For a Pfizer drug inventory system, the test plan might detail testing barcode scanning across 10 sites over 3 months, ensuring compliance with GMP.
- **Industry Twist**: Includes risk assessments (e.g., patient safety impact if software fails) and validation protocols for audits.

#### 3. **Test Scenario**
- **Definition**: High-level descriptions of functionalities or workflows to test.
- **Use Case**: Merck might define a scenario like “End-to-end patient enrollment in a Phase III trial,” covering registration, consent, and data logging.
- **Industry Twist**: Scenarios often map to clinical workflows or drug lifecycle stages, ensuring real-world applicability.

#### 4. **Test Execution**
- **Definition**: Manually running test cases and recording outcomes.
- **Use Case**: At Eli Lilly, testers execute tests on a diabetes management app, manually checking if glucose readings sync correctly with a cloud database.
- **Industry Twist**: Execution logs are meticulously documented for regulatory submission (e.g., FDA 510(k) clearance for medical devices).

#### 5. **Defect Tracking**
- **Definition**: Identifying, logging, and monitoring software bugs.
- **Use Case**: J&J testers find a defect in a surgical robot UI where a button mislabels a critical function—they log it in Jira with steps, screenshots, and patient risk level.
- **Industry Twist**: Defects are classified by severity (e.g., critical if it impacts drug dosing) and tied to CAPA (Corrective and Preventive Action) processes.

#### 6. **Bug Report**
- **Definition**: A detailed record of a defect, including reproduction steps and impact.
- **Use Case**: A tester at Novartis reports: “Steps: Enter expired drug batch number. Actual: Accepted. Expected: Rejection with GMP error.” This triggers a fix and revalidation.
- **Industry Twist**: Reports include regulatory references (e.g., “Violates ICH Q9 Quality Risk Management”).

#### 7. **Exploratory Testing**
- **Definition**: Unscripted testing to uncover unexpected issues using tester expertise.
- **Use Case**: At J&J’s MedTech division, a tester explores a new ventilator UI and finds a hidden lag in oxygen level display—missed by scripted tests.
- **Industry Twist**: Critical for medical devices where human factors (e.g., clinician response time) matter.

#### 8. **Ad-Hoc Testing**
- **Definition**: Informal, unplanned testing to spot obvious flaws quickly.
- **Use Case**: Pfizer testers ad-hoc test a vaccine tracking app post-update and catch a misaligned temperature alert before formal testing.
- **Industry Twist**: Used during agile sprints or pre-audit checks to flag urgent issues.

#### 9. **Regression Testing**
- **Definition**: Re-testing to ensure new changes don’t break existing functionality.
- **Use Case**: After fixing a bug in Merck’s Keytruda dosing calculator, testers re-run all prior tests to confirm no side effects.
- **Industry Twist**: Mandatory after every change due to validation requirements (e.g., GxP compliance).

#### 10. **Smoke Testing**
- **Definition**: Quick checks to confirm basic functionality works.
- **Use Case**: Eli Lilly testers smoke test a new build of a drug labeling system to ensure it launches and prints labels before full testing.
- **Industry Twist**: Often a gatekeeper for accepting builds in regulated environments.

#### 11. **Sanity Testing**
- **Definition**: Focused testing to verify specific fixes or features.
- **Use Case**: Post-fix, J&J testers check only the updated adverse event reporting module in a pharmacovigilance system.
- **Industry Twist**: Speeds up validation cycles while maintaining compliance.

#### 12. **Usability Testing**
- **Definition**: Assessing software ease-of-use and intuitiveness.
- **Use Case**: At J&J, testers (or clinicians) evaluate a patient portal to ensure nurses can quickly log vitals—critical for FDA Human Factors Engineering guidelines.
- **Industry Twist**: Heavily emphasized for medical devices and patient-facing apps.

#### 13. **Functional Testing**
- **Definition**: Verifying software meets specified requirements.
- **Use Case**: Pfizer tests a supply chain system to confirm it flags expired drugs per FDA rules.
- **Industry Twist**: Tied to functional specifications in Design History Files (DHF) for devices.

#### 14. **Non-Functional Testing**
- **Definition**: Checking performance, reliability, or security aspects.
- **Use Case**: Merck testers manually assess if a trial database feels responsive under simulated peak load (e.g., 100 users).
- **Industry Twist**: Often manual for subjective metrics like “feel” before automation takes over.

#### 15. **Test Coverage**
- **Definition**: Measuring how much of the software is tested.
- **Use Case**: J&J ensures 100% coverage of critical features (e.g., drug interaction checks) in a prescribing app.
- **Industry Twist**: Linked to Risk-Based Testing—prioritizing high-risk areas per ISO 14971.

#### 16. **Test Data**
- **Definition**: Realistic inputs for testing.
- **Use Case**: Eli Lilly uses anonymized patient data (per HIPAA) to test a clinical trial dashboard.
- **Industry Twist**: Must comply with data privacy laws and mimic real clinical scenarios.

#### 17. **Boundary Testing**
- **Definition**: Testing at the edges of input ranges.
- **Use Case**: Novartis tests a drug pump interface by entering max dosage (e.g., 999 mg) to ensure it rejects unsafe values.
- **Industry Twist**: Critical for safety-critical systems like infusion pumps.

#### 18. **Positive Testing**
- **Definition**: Valid inputs to confirm expected behavior.
- **Use Case**: J&J testers enter a correct patient ID in a telemetry system and verify data displays.
- **Industry Twist**: Ensures baseline compliance with specs.

#### 19. **Negative Testing**
- **Definition**: Invalid inputs to check error handling.
- **Use Case**: Pfizer testers enter a negative temperature in a vaccine storage app and confirm an alert triggers.
- **Industry Twist**: Ensures fail-safes for patient safety.

#### 20. **Test Environment**
- **Definition**: Controlled setup mimicking production.
- **Use Case**: Merck sets up a test lab with real MRI machines to validate imaging software.
- **Industry Twist**: Must replicate clinical settings and pass IQ/OQ/PQ (Installation/Operational/Performance Qualification).

#### 21. **Traceability Matrix**
- **Definition**: Mapping requirements to test cases.
- **Use Case**: J&J links “Secure login” requirement to test cases for a drug trial app, proving compliance to auditors.
- **Industry Twist**: Essential for FDA submissions and GxP audits.

#### 22. **Severity**
- **Definition**: Impact level of a defect.
- **Use Case**: A crash in J&J’s insulin pump software is “critical” due to life-threatening potential.
- **Industry Twist**: Drives prioritization in regulated fixes.

#### 23. **Priority**
- **Definition**: Urgency of fixing a defect.
- **Use Case**: A UI glitch in Pfizer’s vaccine tracker is “high priority” pre-launch, even if severity is low.
- **Industry Twist**: Balances business needs with regulatory timelines.

#### 24. **Risk-Based Testing**
- **Definition**: Prioritizing tests based on risk to patients or business.
- **Use Case**: J&J focuses testing on a chemotherapy dosing module over a reporting feature due to higher risk.
- **Industry Twist**: Aligns with ISO 14971 and FDA risk management standards.

#### 25. **Validation**
- **Definition**: Proving software meets its intended use.
- **Use Case**: Eli Lilly validates a drug dispensing system meets GMP before production use.
- **Industry Twist**: A formal process with documented evidence for regulators.

---

### How These Are Applied in Fortune 100 Medical/Pharma
- **Regulatory Compliance**: Every methodology (e.g., test execution, defect tracking) feeds into compliance frameworks like FDA 21 CFR Part 11, ISO 13485, or ICH guidelines. For J&J, this might mean validating software for its Innovative Medicine or MedTech divisions (e.g., surgical robots).
- **Cross-Functional Teams**: Testers collaborate with clinicians, regulatory experts, and engineers. At Pfizer, usability testing might involve nurses to ensure a vaccine tracker is practical in chaotic hospitals.
- **Documentation Overload**: Bug reports, test plans, and traceability matrices are gold for audits. Merck might maintain a 500-page validation package for a single drug trial system.
- **Real-World Focus**: Exploratory and usability testing shine here—J&J might test a patient app with real doctors to catch workflow hiccups automation can’t predict.

---

### Example Workflow at J&J
Imagine J&J testing a new drug adverse event reporting system:
1. **Test Plan**: Defines scope—HIPAA compliance, 50 users, 2-month timeline.
2. **Test Scenarios**: “Report an event,” “Export data for FDA.”
3. **Test Cases**: “Enter event with valid drug code, verify submission.”
4. **Exploratory Testing**: Try uploading a corrupted file—does it crash?
5. **Defect Tracking**: Log a UI freeze as “major severity, high priority.”
6. **Regression Testing**: Post-fix, re-test all reporting features.
7. **Traceability Matrix**: Link tests to FDA requirements.
8. **Validation**: Sign off that it’s ready for clinical use.

---

### Why Manual Testing Persists
- **Regulatory Nuances**: Automation struggles with subjective checks (e.g., “Is this warning clear?”) that regulators demand.
- **Human Factors**: Usability for doctors or patients requires human eyes—critical for J&J’s MedTech products like ventilators.
- **Early Stages**: New systems (e.g., Pfizer’s trial software) need manual exploration before automation is viable.

---

