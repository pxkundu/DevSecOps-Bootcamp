**Software, tools, and technical expertise** used in **SQA Manual Testing**, with a focus on their practical application across industries, including general software development and regulated sectors like European pharmaceuticals (e.g., Novartis, AstraZeneca). 

Manual testing relies on human effort, but it’s supported by a range of tools to streamline processes, ensure accuracy, and meet quality standards. 

I’ll break this down into three sections—software/tools, technical expertise, and how they intertwine—using industry-standard terms and real-world context.

---

### Software and Tools for SQA Manual Testing
These tools assist testers in planning, executing, documenting, and reporting manual tests. While manual testing doesn’t involve automation scripts, technology enhances efficiency and compliance.

#### 1. **Test Management Tools**
- **Purpose**: Organize test cases, track execution, and generate reports.
- **Examples**:
  - **TestRail**: A popular tool for creating test plans, logging results, and linking to requirements.
    - *Use Case*: AstraZeneca testers use TestRail to manage test cases for a clinical trial system, ensuring EMA traceability.
  - **HP ALM (Application Lifecycle Management)**: Comprehensive suite for test planning and defect tracking.
    - *Use Case*: Novartis uses ALM to align manual tests with GxP requirements for a drug safety app.
  - **Jira with Zephyr**: Combines bug tracking with test management.
    - *Use Case*: A startup manually tests a health app, logging defects and test results in Jira.
- **Features**: Test case creation, execution logs, dashboards, and integration with bug trackers.

#### 2. **Bug Tracking Tools**
- **Purpose**: Log, prioritize, and monitor defects found during testing.
- **Examples**:
  - **Jira**: Industry standard for defect management.
    - *Use Case*: Roche logs a UI glitch in a medical device controller, assigning it “critical severity” for devs to fix.
  - **Bugzilla**: Open-source option for smaller teams.
    - *Use Case*: A biotech firm tracks manual test bugs in Bugzilla for a lab data system.
  - **MantisBT**: Lightweight bug tracker.
    - *Use Case*: Used by a pharma contractor for quick defect reporting on a manufacturing tool.
- **Features**: Defect ID, steps to reproduce, severity/priority fields, and status updates.

#### 3. **Document Management Tools**
- **Purpose**: Store test plans, reports, and compliance docs securely.
- **Examples**:
  - **Microsoft SharePoint**: Centralized storage with version control.
    - *Use Case*: Sanofi stores GMP-compliant test execution logs for EMA audits.
  - **Confluence**: Collaborative documentation platform.
    - *Use Case*: AstraZeneca documents test scenarios and lessons learned for a drug inventory system.
  - **Google Workspace**: Budget-friendly option for smaller teams.
    - *Use Case*: A medtech startup shares test summary reports via Google Docs.
- **Features**: Access control, audit trails, and searchable archives.

#### 4. **Spreadsheet Software**
- **Purpose**: Lightweight test case creation and tracking for smaller projects.
- **Examples**:
  - **Microsoft Excel**: Classic tool for manual test case templates.
    - *Use Case*: A Roche tester logs usability test results for a patient app in Excel before formal reporting.
  - **Google Sheets**: Collaborative alternative.
    - *Use Case*: A distributed team at Novartis tracks ad-hoc test findings in real-time.
- **Features**: Custom tables, filters, and basic reporting.

#### 5. **Screen Capture and Annotation Tools**
- **Purpose**: Document visual defects or UI issues during testing.
- **Examples**:
  - **Snagit**: Captures screenshots/videos with markup.
    - *Use Case*: A tester at Sanofi annotates a misaligned button in a drug labeling app for the bug report.
  - **Greenshot**: Free, lightweight screenshot tool.
    - *Use Case*: Used to highlight a display error in a clinical dashboard.
  - **Lightshot**: Quick and simple capture tool.
    - *Use Case*: Captures a crash in a trial data entry form for defect logging.
- **Features**: Annotations, cropping, and easy sharing.

#### 6. **Test Environment Tools**
- **Purpose**: Simulate real-world conditions for testing.
- **Examples**:
  - **Virtual Machines (VMware, VirtualBox)**: Run software on different OS versions.
    - *Use Case*: Novartis tests a pharmacovigilance app on Windows 10 and 11 VMs.
  - **BrowserStack Live**: Manual testing across browsers/devices.
    - *Use Case*: AstraZeneca checks a patient portal’s usability on Safari, Chrome, and Edge.
  - **Physical Devices**: Real hardware for medical device software.
    - *Use Case*: Roche tests a ventilator UI on the actual machine in a lab.
- **Features**: Multi-platform support, device emulation, and network simulation.

#### 7. **Collaboration Tools**
- **Purpose**: Facilitate communication between testers, devs, and stakeholders.
- **Examples**:
  - **Slack/Teams**: Real-time updates on test progress.
    - *Use Case*: Sanofi testers ping devs on Teams about a critical defect during smoke testing.
  - **Trello**: Task tracking for testing phases.
    - *Use Case*: A small pharma team manages exploratory testing tasks on Trello boards.
- **Features**: Chat, file sharing, and task assignment.

---

### Technical Expertise Required for SQA Manual Testing
Manual testing isn’t just clicking buttons—it demands a mix of skills to execute effectively, especially in regulated environments like pharma.

#### 1. **Domain Knowledge**
- **What**: Understanding the industry and software’s purpose.
- **Expertise**: Knowledge of pharma processes (e.g., clinical trials, GMP) or medical device workflows.
- **Use Case**: A Novartis tester knows ICH Q9 risk principles to prioritize testing a drug safety module over a reporting feature.
- **Level**: Intermediate to advanced, depending on complexity.

#### 2. **Test Case Design**
- **What**: Crafting detailed, repeatable test scenarios.
- **Expertise**: Writing clear steps, covering positive/negative cases, and ensuring traceability.
- **Use Case**: A Roche tester designs boundary tests for a dosing app (e.g., max dose input) to meet ISO 14971 safety standards.
- **Level**: Basic to intermediate; improves with experience.

#### 3. **Defect Reporting**
- **What**: Documenting bugs with precision.
- **Expertise**: Describing issues concisely, assessing severity/priority, and using tools like Jira.
- **Use Case**: An AstraZeneca tester logs a data sync failure in a trial app, attaching logs and rating it “major severity.”
- **Level**: Basic; refined through practice.

#### 4. **Exploratory Testing Skills**
- **What**: Thinking creatively to find unscripted issues.
- **Expertise**: Intuition, curiosity, and ability to mimic end-user behavior.
- **Use Case**: A Sanofi tester explores a manufacturing UI and catches a hidden crash by entering invalid batch data.
- **Level**: Intermediate; grows with domain familiarity.

#### 5. **Attention to Detail**
- **What**: Spotting subtle flaws or inconsistencies.
- **Expertise**: Observing UI, functionality, and performance nuances.
- **Use Case**: A Roche tester notices a 1-second lag in a ventilator alarm—missed by others but critical for patient safety.
- **Level**: Innate but honed over time.

#### 6. **Regulatory Compliance Knowledge**
- **What**: Understanding standards like GMP, EMA, or FDA rules.
- **Expertise**: Applying GxP guidelines to testing and reporting.
- **Use Case**: A Novartis tester ensures a pharmacovigilance system’s manual tests meet EudraVigilance data integrity rules.
- **Level**: Advanced; critical in pharma.

#### 7. **Basic Tool Proficiency**
- **What**: Using testing and office software effectively.
- **Expertise**: Navigating TestRail, Jira, Excel, or SharePoint; capturing evidence with Snagit.
- **Use Case**: An AstraZeneca tester logs a usability issue in TestRail and attaches a Snagit screenshot.
- **Level**: Basic; easily trainable.

#### 8. **Communication Skills**
- **What**: Conveying findings to technical and non-technical teams.
- **Expertise**: Writing clear reports and collaborating via Slack/Teams.
- **Use Case**: A Sanofi tester explains a defect’s GMP impact to devs in a concise Teams message.
- **Level**: Basic to intermediate; key for stakeholder buy-in.

#### 9. **Test Environment Setup**
- **What**: Configuring systems for realistic testing.
- **Expertise**: Managing VMs, browsers, or physical devices; understanding network conditions.
- **Use Case**: A Roche tester sets up a VM with Windows 10 to test a lab system’s compatibility.
- **Level**: Intermediate; requires some IT knowledge.

---

### How Tools and Expertise Interconnect
- **Test Management + Test Case Design**: TestRail helps a Novartis tester write and organize GMP-compliant test cases for a drug batch system.
- **Bug Tracking + Defect Reporting**: Jira enables an AstraZeneca tester to log a trial app bug with detailed steps, ensuring devs can replicate it.
- **Screen Capture + Attention to Detail**: Snagit lets a Roche tester document a subtle UI flaw in a medical device, flagged due to sharp observation.
- **Environment Tools + Domain Knowledge**: BrowserStack helps a Sanofi tester verify a patient portal across devices, leveraging pharma UI standards.
- **Collaboration + Communication**: Teams allows a Novartis tester to quickly escalate a critical defect to devs, ensuring timely fixes.

---

### Industry-Specific Notes (European Pharma)
- **Pharma Tools**: TestRail and HP ALM are favorites for their audit-ready reporting (GMP Annex 11 compliance). Jira dominates defect tracking due to CAPA integration.
- **Expertise**: Testers often need GxP training and ICH Q9 familiarity—beyond typical QA skills—to handle regulatory complexity.
- **Physical Devices**: Common in medical device testing (e.g., Roche’s diagnostics), requiring hands-on hardware skills.

---

### Example Scenario
A tester at AstraZeneca manually tests a clinical trial dashboard:
- **Tools**: TestRail (test cases), Jira (defects), Snagit (screenshots), SharePoint (docs), BrowserStack (cross-browser).
- **Expertise**: Designs test cases for patient data entry, spots a privacy flaw (domain knowledge), logs it in Jira with evidence, and communicates via Teams.
- **Outcome**: A compliance report is generated, meeting EMA standards, with full traceability.

---
