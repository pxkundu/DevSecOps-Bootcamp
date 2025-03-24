**SQA Manual Testing Reporting Criteria and Best Practices** as followed by European pharmaceutical companies, such as AstraZeneca, Novartis, Roche, or Sanofi. These companies operate under stringent regulatory frameworks like the European Medicines Agency (EMA) guidelines, Good Manufacturing Practices (GMP), and International Council for Harmonisation (ICH) standards. 

Manual testing remains a critical component of Software Quality Assurance (SQA) in this sector, especially for validating complex, safety-critical systems (e.g., clinical trial management, pharmacovigilance, or drug manufacturing software). 

I’ll break this down into reporting criteria, best practices, and industry-specific details, using relevant keywords and real-world context.

---

### Reporting Criteria in SQA Manual Testing
Reporting in manual testing is about documenting the process, results, and compliance to ensure transparency, traceability, and regulatory adherence. Here are the key criteria European pharma companies emphasize:

#### 1. **Test Summary Report**
- **Definition**: A high-level overview of testing activities, including scope, objectives, pass/fail rates, and key findings.
- **Criteria**: Must summarize executed test cases, defects found, and overall quality status.
- **Use Case**: At Roche, a test summary report for a drug safety system might detail 95% test case pass rate, with 5 critical defects resolved before release.
- **Industry Twist**: Must align with ICH Q9 (Quality Risk Management) to highlight risk mitigation outcomes.

#### 2. **Defect Report**
- **Definition**: Detailed documentation of identified bugs, including steps to reproduce, severity, and priority.
- **Criteria**: Includes defect ID, description, environment, actual vs. expected results, and screenshots/logs.
- **Use Case**: Novartis logs a defect in a clinical trial app where patient data isn’t masked (HIPAA/EMA violation), rated as “critical severity” and “high priority.”
- **Industry Twist**: Linked to Corrective and Preventive Action (CAPA) processes for regulatory audits.

#### 3. **Test Execution Log**
- **Definition**: A record of each test case run, with timestamps, tester names, and outcomes.
- **Criteria**: Captures pass/fail status, deviations, and comments per test step.
- **Use Case**: AstraZeneca testers log manual execution of a batch release system test, noting a 2-second delay in GMP compliance checks.
- **Industry Twist**: Must be tamper-proof and auditable per GMP Annex 11 (Computerised Systems).

#### 4. **Traceability Matrix**
- **Definition**: A document mapping test cases to requirements to ensure full coverage.
- **Criteria**: Links each test to an EMA/GMP requirement (e.g., data integrity, user access control).
- **Use Case**: Sanofi uses a traceability matrix to prove all pharmacovigilance reporting features meet EudraVigilance standards.
- **Industry Twist**: Mandatory for EMA submissions and validation sign-off.

#### 5. **Risk Assessment Report**
- **Definition**: An analysis of potential risks uncovered during testing and their impact on patient safety or compliance.
- **Criteria**: Identifies risk level (low, medium, high) and mitigation steps.
- **Use Case**: Roche reports a medium-risk UI glitch in a medical device controller, mitigated by a design tweak.
- **Industry Twist**: Follows ISO 14971 (Medical Device Risk Management) and ICH Q9 principles.

#### 6. **Compliance Report**
- **Definition**: Evidence that testing adheres to regulatory standards.
- **Criteria**: Confirms alignment with EMA, GMP, and GxP (Good Practice) rules.
- **Use Case**: Novartis submits a compliance report showing manual tests on a drug labeling system meet Ph. Eur. (European Pharmacopoeia) standards.
- **Industry Twist**: Includes signatures from Quality Assurance (QA) leads for legal accountability.

#### 7. **Exit Criteria Evaluation**
- **Definition**: Metrics determining when testing is complete (e.g., 95% pass rate, no critical defects).
- **Criteria**: Predefined thresholds must be met, with justification for exceptions.
- **Use Case**: AstraZeneca stops testing a trial data portal once 98% of test cases pass and all high-severity bugs are fixed.
- **Industry Twist**: Tied to Validation Summary Reports (VSR) for regulatory sign-off.

---

### Best Practices in SQA Manual Testing Reporting
European pharma companies follow disciplined best practices to ensure reporting is robust, actionable, and compliant. Here’s how they do it:

#### 1. **Standardized Templates**
- **Practice**: Use consistent formats for reports (e.g., defect logs, test summaries) across projects.
- **Why**: Ensures uniformity and simplifies audits by EMA inspectors.
- **Example**: Sanofi might use an EMA-approved template for defect reports, including fields like “GxP Impact” and “Resolution Date.”
- **Keyword**: **Documentation Control**—keeps records organized and retrievable.

#### 2. **Detailed Defect Classification**
- **Practice**: Categorize defects by severity (critical, major, minor) and priority (high, medium, low).
- **Why**: Prioritizes fixes based on patient safety and compliance risks.
- **Example**: Roche classifies a data entry error in a drug dosing app as “critical severity, high priority” due to potential overdose risk.
- **Keyword**: **Severity/Priority Assessment**—drives urgency and resource allocation.

#### 3. **Real-Time Reporting**
- **Practice**: Log results as tests are executed, not post-facto.
- **Why**: Reduces errors and ensures data integrity for GMP Annex 11 audits.
- **Example**: AstraZeneca testers update a cloud-based test execution log during usability testing of a patient monitoring app.
- **Keyword**: **Data Integrity**—a cornerstone of pharma SQA.

#### 4. **Traceability and Audit Readiness**
- **Practice**: Link every report to requirements and maintain version control.
- **Why**: Enables EMA or ISO 13485 auditors to trace compliance from spec to test outcome.
- **Example**: Novartis keeps a traceability matrix showing how a batch tracking system meets GMP requirements, ready for inspection.
- **Keyword**: **Audit Trail**—proves process adherence.

#### 5. **Risk-Based Reporting**
- **Practice**: Focus reporting on high-risk areas (e.g., drug safety, data security).
- **Why**: Aligns with ICH Q9 and ensures critical issues aren’t buried in noise.
- **Example**: Roche prioritizes reporting on a ventilator software’s alarm system over cosmetic UI flaws.
- **Keyword**: **Risk-Based Testing**—optimizes effort and safety.

#### 6. **Stakeholder Communication**
- **Practice**: Share concise, actionable insights with developers, QA leads, and regulators.
- **Why**: Speeds up defect resolution and approval processes.
- **Example**: Sanofi emails a defect summary to devs within 24 hours of a failed test on a manufacturing control system.
- **Keyword**: **Collaboration**—bridges testing and development teams.

#### 7. **Post-Test Review**
- **Practice**: Conduct a review of reports to identify trends and improve processes.
- **Why**: Drives continuous improvement per ISO 9001 principles.
- **Example**: AstraZeneca analyzes regression test failures to refine test cases for a drug trial platform.
- **Keyword**: **Lessons Learned**—enhances future testing.

#### 8. **Regulatory Alignment**
- **Practice**: Embed EMA, GMP, and ICH references in all reports.
- **Why**: Proves compliance during marketing authorization applications.
- **Example**: Novartis includes “ICH Q10 Compliance” notes in a test summary for a quality management system.
- **Keyword**: **Validation**—ensures software is fit for purpose.

---

### Industry-Specific Nuances in European Pharma
- **Regulatory Oversight**: The EMA enforces strict reporting standards (e.g., EudraLex Volume 4 for GMP). Reports must withstand audits and support marketing authorizations.
- **GxP Focus**: Good Clinical Practice (GCP), Good Laboratory Practice (GLP), and GMP dictate testing and reporting rigor. For instance, GCP drives manual testing of clinical trial software at Roche.
- **Patient Safety**: Defects impacting drug dosing, trial data, or device operation (e.g., Sanofi’s insulin pens) get escalated reporting priority.
- **Cross-Border Harmonization**: Companies like AstraZeneca (UK/Sweden) align with both EMA and national regulators (e.g., MHRA), requiring multilingual or standardized reports.

---

### Example in Action
Imagine Novartis testing a pharmacovigilance system:
- **Test Execution Log**: Tester logs “Adverse event report submitted at 10:03 AM, pass” during manual checks.
- **Defect Report**: “Event timestamp missing—Severity: Major, Priority: High, GxP Impact: Yes.”
- **Traceability Matrix**: Links test to EMA EudraVigilance requirement 3.1.2.
- **Test Summary**: “99% pass rate, 1 major defect resolved, validated per ICH Q9.”
- **Practice**: Real-time logging in a GMP-compliant tool, reviewed by QA for CAPA.

---

### Tools and Standards
- **Tools**: TestRail or Jira for test management, SharePoint for document control—all validated per GMP Annex 11.
- **Standards**: EMA Guidelines, ICH Q9/Q10, ISO 13485 (devices), Ph. Eur. for quality specs.

---

This covers the full scope of SQA manual testing reporting criteria and best practices in European pharma companies. It’s a blend of precision, compliance, and practical execution tailored to life-critical software.