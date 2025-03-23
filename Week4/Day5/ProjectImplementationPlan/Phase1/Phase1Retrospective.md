## Retrospective on Phase 1 Deliverables

### Context
- **Objective**: Deliver a Terraform-based infrastructure blueprint for multi-region EKS clusters, VPCs, RDS, S3, and ECR, reusing Day 2’s CRM setup.
- **Deliverables**: Terraform files in `CRMSupplyChainCapstone/infrastructure/` (`main.tf`, `variables.tf`, `outputs.tf`, `backend.tf`, `terraform.tfvars`, and `modules/{vpc,eks,rds}`).

### Time Estimate for Phase 1
- **Design & Coding**: ~1-2 days (writing modules, configuring main.tf, iterating).
- **Validation**: ~4-6 hours (running terraform init, plan, apply, fixing errors).
- **Total**: ~2-3 days for 2 engineers, assuming AWS setup and basic testing.

---

### What Went Well
1. **Clear Blueprint**:
   - The deliverables successfully defined a multi-region architecture (`us-east-1`, `eu-west-1`) with EKS, VPCs, RDS, and ECR, providing a solid foundation for the project.
   - The use of `for_each` in `main.tf` for VPC and EKS modules streamlined multi-region provisioning, reflecting modern Terraform practices.
2. **Cost Optimization**:
   - Choices like t3.medium nodes (2 per region), single-AZ RDS, and a single NAT Gateway per VPC kept the estimated AWS spend low (~$60-70/month), aligning with budget goals.
3. **Reuse of Day 2**:
   - Leveraging Day 2’s S3/DynamoDB backend and extending existing module patterns (e.g., `modules/vpc`) saved time and ensured consistency with prior work.
4. **DevSecOps Alignment**:
   - Security features (IAM least privilege, RDS encryption, restricted security groups) and modularity (separate VPC, EKS, RDS modules) matched Fortune 100 standards (e.g., Amazon, Walmart).

---

### What Could Be Improved
1. **Version Specification**:
   - **Reflection**: Explicit versioning (e.g., `>= 1.9.0`, `>= 5.40.0`) would enforce consistency.
2. **Secrets Management**:
   - RDS includes a hardcoded password (`"securepassword"`) in `modules/rds/main.tf`. In a real-world scenario, this should use AWS Secrets Manager or a Terraform variable with a sensitive flag.
   - **Reflection**: Missed an opportunity to model secure credential handling.
3. **ECR Lifecycle Policy**:
   - The script defines ECR repos but omits lifecycle policies (e.g., keep last 5 images), requiring manual AWS configuration post-deployment.
   - **Reflection**: Including `lifecycle_policy` resources would enhance automation and cost control.
4. **Documentation in Deliverables**:
   - While `docs/README.md` exists as a placeholder, the Terraform files lack inline comments or a separate `infrastructure/README.md` to explain design choices (e.g., why single-AZ RDS).
   - **Reflection**: Better documentation would improve maintainability, a key DevOps principle.
5. **Testing Simulation**:
   - No dry-run or validation step (e.g., `terraform plan`) was scripted to verify the deliverables before applying, which could catch syntax errors early.
   - **Reflection**: Adding a validation step would align with CI/CD rigor.

---

### Action Items
1. **Version Pinning (Optional)**:
   - If sticking with the original code, document in `docs/README.md` that users should run with Terraform 1.9.x and AWS provider 5.x (latest as of March 2025) for consistency.
   - Alternatively, adopt the updated script with pins if version certainty becomes critical later.
2. **Secure Secrets**:
   - Update `modules/rds/main.tf` to use a variable for the RDS password (e.g., `var.db_password`) and note in `README.md` to integrate with Secrets Manager in production.
3. **ECR Lifecycle**:
   - Add `aws_ecr_lifecycle_policy` resources to `main.tf` for each repo, or document the manual step in `docs/architecture.md`.
4. **Enhance Documentation**:
   - Add inline comments to Terraform files (e.g., `# Single-AZ RDS for cost optimization`) and create `infrastructure/README.md` with a quick setup guide.
5. **Validation Step**:
   - Extend the script with a `terraform init && terraform validate` command to ensure deliverables are syntactically correct before proceeding.

---

### Key Takeaways
1. **Balance of Simplicity and Standards**:
   - The original code struck a good balance between simplicity (no version pins, minimal config) and enterprise-grade design (modular, multi-region), making it ideal for a learning capstone while still professional.
2. **Reuse is Powerful**:
   - Leveraging Day 2’s setup reinforced the value of modular IaC, a practice that saved time and mirrored real-world efficiency (e.g., Amazon’s reusable infra patterns).
3. **Cost vs. Resilience Trade-offs**:
   - Opting for single-AZ RDS and limited nodes highlighted the need to weigh cost against availability—a real Fortune 100 decision point (e.g., Walmart optimizing logistics spend).
4. **DevSecOps Gaps**:
   - Hardcoded secrets and missing lifecycle policies showed that security and automation require proactive design, not afterthoughts—lessons to apply in Phases 2-5.
5. **Documentation Matters**:
   - Lack of inline guidance underscored how critical documentation is for team handoff, a DHL-like best practice we should prioritize moving forward.

---

### Reflection on Going Forward
- **Next Steps**: Phase 2 (Backend) will build on this infra, so ensuring `terraform apply` works smoothly is key. We’ll address secrets and ECR policies there if needed, keeping the blueprint intact.
- **Confidence**: The deliverables are a strong starting point, aligning with the project’s goals (cost-efficient, multi-region, DevSecOps-ready) and setting us up for success.

This retrospective validates Phase 1’s strengths while identifying actionable refinements, ensuring we proceed with clarity and purpose. 