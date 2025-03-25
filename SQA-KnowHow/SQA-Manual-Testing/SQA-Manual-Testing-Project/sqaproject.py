import os
import shutil
from datetime import datetime

# Project root directory
PROJECT_DIR = "sqa_manual_testing_project"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d")

# Create directory structure
def create_folder_structure():
    folders = [
        f"{PROJECT_DIR}/docs/test_plan",
        f"{PROJECT_DIR}/docs/requirements",
        f"{PROJECT_DIR}/docs/traceability",
        f"{PROJECT_DIR}/test_artifacts/test_cases",
        f"{PROJECT_DIR}/test_artifacts/test_data",
        f"{PROJECT_DIR}/test_artifacts/execution_logs",
        f"{PROJECT_DIR}/test_artifacts/defect_reports",
        f"{PROJECT_DIR}/reports",
        f"{PROJECT_DIR}/environments",
        f"{PROJECT_DIR}/templates",
        f"{PROJECT_DIR}/tools",
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

# Write content to files
def generate_files():
    # Test Plan
    with open(f"{PROJECT_DIR}/docs/test_plan/test_plan.docx", "w") as f:
        f.write(
            "Test Plan: Janssen Patient Portal\n"
            "Objective: Ensure login, record retrieval, and logout meet IEC 62304 and GDPR.\n"
            "Scope: Functional, regression, and risk-based testing of core features.\n"
            "Timeline: March 25-31, 2025\n"
            "Resources: 2 testers, Chrome on Windows 10\n"
            "Risks: Login failure (High), Data breach (Critical)"
        )

    # Risk Assessment
    with open(f"{PROJECT_DIR}/docs/test_plan/risk_assessment.xlsx", "w") as f:
        f.write(
            "Risk ID,Description,Likelihood,Impact,Mitigation\n"
            "R1,Login failure,Medium,High,Functional and regression testing\n"
            "R2,Data exposure,Low,Critical,Risk-based testing with GDPR data"
        )

    # Software Requirements Specification (SRS)
    with open(f"{PROJECT_DIR}/docs/requirements/srs.docx", "w") as f:
        f.write(
            "Software Requirements Specification\n"
            "Req-001: User shall log in with valid credentials in <2s.\n"
            "Req-002: Invalid login shall show error.\n"
            "Req-003: Patient record retrieval shall display data in <3s."
        )

    # Traceability Matrix
    with open(f"{PROJECT_DIR}/docs/traceability/traceability_matrix.xlsx", "w") as f:
        f.write(
            "Req ID,Description,Test Case ID\n"
            "Req-001,Valid login,TC-001\n"
            "Req-002,Invalid login error,TC-002\n"
            "Req-003,Record retrieval,TC-003"
        )

    # Test Cases: Login (Functional Testing)
    with open(f"{PROJECT_DIR}/test_artifacts/test_cases/login_tests.xlsx", "w") as f:
        f.write(
            "Test ID,Title,Precondition,Steps,Expected Result,Status\n"
            "TC-001,Valid Login,User at login page,1. Enter 'user1', 'pass123' 2. Click Login,Dashboard loads in <2s,Pass\n"
            "TC-002,Invalid Login,User at login page,1. Enter 'wrong', 'wrong' 2. Click Login,Error: 'Invalid credentials',Pass"
        )

    # Test Cases: Record Retrieval (Regression Testing)
    with open(f"{PROJECT_DIR}/test_artifacts/test_cases/record_tests.xlsx", "w") as f:
        f.write(
            "Test ID,Title,Precondition,Steps,Expected Result,Status\n"
            "TC-003,Record Retrieval,Logged in,1. Enter patient ID 'P001' 2. Click Retrieve,Data displays in <3s,Pass\n"
            "TC-004,Post-Update Retrieval,Logged in post-update,1. Repeat TC-003,Data displays in <3s,Pass"
        )

    # Test Cases: Logout (Risk-Based Testing)
    with open(f"{PROJECT_DIR}/test_artifacts/test_cases/logout_tests.xlsx", "w") as f:
        f.write(
            "Test ID,Title,Precondition,Steps,Expected Result,Status\n"
            "TC-005,Secure Logout,Logged in,1. Click Logout,Session ends, no data accessible,Pass"
        )

    # Test Data
    with open(f"{PROJECT_DIR}/test_artifacts/test_data/patient_data.csv", "w") as f:
        f.write(
            "patient_id,name,email\n"
            "P001,John Doe,john.doe@test.com\n"
            "P002,Jane Smith,jane.smith@test.com"
        )

    # Execution Logs
    with open(f"{PROJECT_DIR}/test_artifacts/execution_logs/test_execution_log.xlsx", "w") as f:
        f.write(
            "Test ID,Date,Tester,Result,Comments\n"
            f"TC-001,{TIMESTAMP},You,Pass,Loaded in 1.8s\n"
            f"TC-002,{TIMESTAMP},You,Pass,Error as expected\n"
            f"TC-003,{TIMESTAMP},You,Pass,Data in 2.5s\n"
            f"TC-004,{TIMESTAMP},You,Pass,Post-update stable\n"
            f"TC-005,{TIMESTAMP},You,Pass,Session terminated"
        )

    # Defect Reports
    with open(f"{PROJECT_DIR}/test_artifacts/defect_reports/defect_log.xlsx", "w") as f:
        f.write(
            "Defect ID,Description,Severity,Priority,Steps to Reproduce,Status\n"
            "D-001,Login delay >2s on slow network,Medium,High,Enter valid creds, click Login,Resolved"
        )

    # Test Summary Report
    with open(f"{PROJECT_DIR}/reports/test_summary_report.docx", "w") as f:
        f.write(
            "Test Summary Report\n"
            "Tests Run: 5\n"
            "Passed: 5\n"
            "Failed: 0\n"
            "Defects: 1 (Resolved)\n"
            "Conclusion: Portal meets functional, regression, and risk-based goals."
        )

    # Compliance Report
    with open(f"{PROJECT_DIR}/reports/compliance_report.docx", "w") as f:
        f.write(
            "Compliance Report\n"
            "Standards: IEC 62304, ISO 13485, GDPR\n"
            "Result: All tests traceable, logs stored, data anonymized."
        )

    # Lessons Learned
    with open(f"{PROJECT_DIR}/reports/lessons_learned.docx", "w") as f:
        f.write(
            "Lessons Learned\n"
            "1. Add network stress tests for login.\n"
            "2. Expand regression suite post-updates."
        )

    # Environment Config
    with open(f"{PROJECT_DIR}/environments/env_config.docx", "w") as f:
        f.write(
            "Test Environment\n"
            "Browser: Chrome v120\n"
            "OS: Windows 10\n"
            "URL: patientportal.janssen.com"
        )

    # Test Case Template
    with open(f"{PROJECT_DIR}/templates/test_case_template.xlsx", "w") as f:
        f.write(
            "Test ID,Title,Precondition,Steps,Expected Result,Status\n"
        )

    # Defect Report Template
    with open(f"{PROJECT_DIR}/templates/defect_report_template.xlsx", "w") as f:
        f.write(
            "Defect ID,Description,Severity,Priority,Steps to Reproduce,Status\n"
        )

    # Jira Config
    with open(f"{PROJECT_DIR}/tools/jira_config.md", "w") as f:
        f.write(
            "# Jira Configuration\n"
            "Project: JPP-Test\n"
            "Fields: Severity, Priority, Steps to Reproduce"
        )

    # README
    with open(f"{PROJECT_DIR}/README.md", "w") as f:
        f.write(
            "# SQA Manual Testing Project\n"
            "Manual testing for Janssen Patient Portal using Functional, Regression, and Risk-Based methodologies.\n\n"
            "## Structure\n"
            "- `docs/`: Plans, requirements, traceability.\n"
            "- `test_artifacts/`: Test cases, data, logs, defects.\n"
            "- `reports/`: Summaries and compliance.\n"
            "- `environments/`: Test env setup.\n"
            "- `templates/`: Reusable formats.\n"
            "- `tools/`: Jira config.\n\n"
            "## Methodologies\n"
            "1. **Functional Testing**: Ensures login/record retrieval work (TC-001, TC-003).\n"
            "2. **Regression Testing**: Validates stability post-update (TC-004).\n"
            "3. **Risk-Based Testing**: Secures logout to prevent data access (TC-005).\n"
        )

# Main execution
if __name__ == "__main__":
    create_folder_structure()
    generate_files()
    print(f"Project generated at: {PROJECT_DIR}")