25 important interview questions inspired by **Week 1, Day 3: Networking Deep Dive** topics, tailored to reflect the kinds of questions Fortune 100 companies (e.g., Amazon, Google, Microsoft, etc.) might ask for AWS DevOps and Cloud Engineer roles. These questions span theoretical knowledge, practical application, and troubleshooting scenarios related to VPC, subnets, Security Groups, routing, and DDoS mitigation—key concepts from Day 3. 

These are designed to test depth, problem-solving, and real-world experience at an intermediate level.

---

### VPC and Networking Basics
1. **What is a VPC, and why would you use one in AWS?**
   - Tests understanding of **Virtual Private Cloud** and **Isolation**.

2. **Explain the difference between a public subnet and a private subnet.**
   - Focuses on **Subnet**, **Internet Gateway**, and **NAT Gateway**.

3. **How does a CIDR block work, and what does /16 vs. /24 mean in a VPC?**
   - Assesses knowledge of **CIDR Block** and IP address allocation.

4. **What’s the purpose of an Internet Gateway in a VPC? Can a VPC function without it?**
   - Evaluates grasp of **Internet Gateway** and network connectivity.

5. **Describe how Route Tables control traffic in a VPC. Give an example.**
   - Targets **Route Table** and **Default Route** concepts.

---

### Subnets and Availability
6. **How would you design a VPC with high availability across multiple Availability Zones?**
   - Tests **High Availability**, **Availability Zone**, and subnet strategy.

7. **What’s the role of a NAT Gateway, and when would you use it instead of an Internet Gateway?**
   - Focuses on **NAT Gateway** and private subnet outbound access.

8. **Can an EC2 instance in a private subnet access the internet? If so, how?**
   - Assesses **Private Subnet**, **NAT Gateway**, and routing knowledge.

9. **You’re tasked with setting up a VPC with 3 tiers (web, app, DB). How would you assign subnets?**
   - Practical use case for **Subnet** segmentation and **Security**.

10. **What happens if two subnets in a VPC have overlapping CIDR ranges?**
    - Tests understanding of **CIDR Block** conflicts and troubleshooting.

---

### Security Groups and Traffic Control
11. **What’s the difference between a Security Group and a Network ACL (NACL)?**
    - Compares **Security Group** with another AWS security tool.

12. **How do Security Groups handle inbound and outbound traffic by default?**
    - Focuses on **Inbound Rule**, **Outbound Rule**, and stateful behavior.

13. **Design a Security Group for a web server that’s publicly accessible but secure.**
    - Practical application of **Security Group** and **DDoS Mitigation**.

14. **Can you apply multiple Security Groups to an EC2 instance? How do they interact?**
    - Tests advanced **Security Group** usage and rule precedence.

15. **What’s a common mistake when configuring Security Groups that blocks legitimate traffic?**
    - Probes troubleshooting skills and **Inbound Rule** misconfigs.

---

### Troubleshooting and Real-World Scenarios
16. **An EC2 instance in a public subnet can’t be reached via SSH. What would you check first?**
    - Assesses **Security Group**, **Route Table**, and **Public IP** knowledge.

17. **Your web application in a VPC suddenly stops responding. How do you diagnose the issue?**
    - Broad test of **Troubleshooting**, **Route Table**, and **Security** skills.

18. **A private subnet EC2 needs to pull updates from the internet but fails. What’s wrong?**
    - Targets **NAT Gateway** setup and outbound routing.

19. **You notice high latency between two EC2 instances in a VPC. What might be causing it?**
    - Evaluates **Latency**, **AZ**, and network design awareness.

20. **How would you verify that a Route Table is correctly directing traffic to an Internet Gateway?**
    - Practical check of **Route Table** and **Default Route**.

---

### DDoS Mitigation and Security
21. **How can Security Groups help mitigate a DDoS attack on an EC2 instance?**
    - Focuses on **DDoS Mitigation** and **Security Group** rules.

22. **What AWS service would you pair with a VPC to protect against DDoS attacks at scale?**
    - Tests knowledge beyond Day 3 (e.g., AWS Shield) but ties to **Security**.

23. **A public-facing app is under a brute-force SSH attack. How do you lock it down quickly?**
    - Practical **Security Group** fix and **Inbound Rule** adjustment.

24. **Explain how you’d configure a VPC to isolate sensitive data from public access.**
    - Use case for **Private Subnet**, **NAT Gateway**, and **Security**.

25. **Your team reports a subnet is ‘down’ after a network change. How do you investigate and recover?**
    - Simulates Day 3’s chaos twist (**DDoS** or misconfig) and **Troubleshooting**.

---

### Why These Questions Fit Fortune 100 Interviews
- **Depth**: They go beyond basics (e.g., “What’s a VPC?”) to test understanding (e.g., “How does CIDR impact design?”).
- **Practicality**: Many are scenario-based, reflecting real-world challenges Fortune 100 companies face (e.g., HA, DDoS).
- **AWS Focus**: Questions align with AWS-specific features (e.g., NAT Gateway, Security Groups), common in Amazon, Microsoft, or Google roles.
- **Problem-Solving**: Troubleshooting and mitigation questions mimic on-call or design tasks in large-scale environments.

---

### Preparation Tips for Day 3 Topics
- **Theory**: Review Day 3’s **Key Concepts** (e.g., **CIDR**, **NAT Gateway**) and AWS docs.
- **Practice**: Build a VPC with public/private subnets, tweak Security Groups, and simulate failures.
- **Answers**: Check answers file.

