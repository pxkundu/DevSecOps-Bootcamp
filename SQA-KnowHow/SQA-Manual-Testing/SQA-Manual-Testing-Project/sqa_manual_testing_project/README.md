# SQA Manual Testing Project
Manual testing for Janssen Patient Portal using Functional, Regression, and Risk-Based methodologies.

## Structure
- `docs/`: Plans, requirements, traceability.
- `test_artifacts/`: Test cases, data, logs, defects.
- `reports/`: Summaries and compliance.
- `environments/`: Test env setup.
- `templates/`: Reusable formats.
- `tools/`: Jira config.

---

### Selected Core SQA Manual Testing Methodologies
1. **Functional Testing**: Verifies that the software meets specified requirements (e.g., login works as per IEC 62304).
   - **Real-World Connection**: Ensures critical features like patient record retrieval function correctly, vital for patient care and compliance in pharma.
2. **Regression Testing**: Re-tests existing functionality after changes to ensure no new defects (e.g., post-update stability).
   - **Real-World Connection**: Critical for J&J’s frequent software updates to maintain ISO 13485 quality standards.
3. **Risk-Based Testing**: Prioritizes testing based on risk to patients or compliance (e.g., focusing on login security).
   - **Real-World Connection**: Aligns with ISO 14971, ensuring high-risk areas (e.g., data breaches) are rigorously tested.

---

### Minimum Understandable Content Explained
- **Test Plan**: Outlines scope with the three methodologies, reflecting real-world J&J planning.
- **Risk Assessment**: Prioritizes login and data risks, tied to ISO 14971.
- **SRS**: Simple requirements for traceability (IEC 62304).
- **Traceability Matrix**: Links tests to requirements, pharma audit-ready.
- **Test Cases**: 
  - **Functional**: TC-001/TC-002 (login), TC-003 (records)—ensures core features work.
  - **Regression**: TC-004—verifies stability post-update, a J&J must-have.
  - **Risk-Based**: TC-005—focuses on secure logout, critical for GDPR/ISO 13485.
- **Test Data**: GDPR-compliant, realistic patient data.
- **Execution Logs**: Completed runs with timestamps, mirroring GMP Annex 11 logs.
- **Defect Log**: One resolved defect, showing real-world triaging.
- **Reports**: Summary, compliance, and lessons learned—stakeholder-ready.
- **Templates**: Reusable formats for scalability.
- **Jira Config**: Practical tool setup for defect tracking.

---

### Real-World Connection and Relation
- **Functional Testing**: TC-001/TC-003 ensure patient access and data retrieval work, critical for J&J’s clinical operations (e.g., Calysta Pro EMR).
- **Regression Testing**: TC-004 mirrors J&J’s need to validate updates to Janssen Medical Cloud without breaking existing features, per ISO 13485.
- **Risk-Based Testing**: TC-005 addresses logout security, a high-risk area for patient data protection (GDPR, ISO 14971), common in pharma audits.
- **Pharma Context**: The structure (traceability, logs, compliance reports) reflects J&J’s regulatory demands, ensuring EMA/FDA readiness.

---

### Why This is Industry-Standard
- **Modularity**: Separate folders for artifacts, reports, and docs—scalable for large teams.
- **Compliance**: Traceability and logs meet IEC 62304/ISO 13485.
- **Best Practices**: Risk-based prioritization, standardized templates, and stakeholder reporting align with Fortune 100 QA processes.
- **Your Fit**: Leverages your J&J experience in SDLC, QA, and collaboration.

---
