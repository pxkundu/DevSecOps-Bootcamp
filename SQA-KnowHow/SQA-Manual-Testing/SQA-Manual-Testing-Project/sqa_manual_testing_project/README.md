# SQA Manual Testing Project
Manual testing for Janssen Patient Portal using Functional, Regression, and Risk-Based methodologies.

## Structure
- `docs/`: Plans, requirements, traceability.
- `test_artifacts/`: Test cases, data, logs, defects.
- `reports/`: Summaries and compliance.
- `environments/`: Test env setup.
- `templates/`: Reusable formats.
- `tools/`: Jira config.

## Methodologies
1. **Functional Testing**: Ensures login/record retrieval work (TC-001, TC-003).
2. **Regression Testing**: Validates stability post-update (TC-004).
3. **Risk-Based Testing**: Secures logout to prevent data access (TC-005).
