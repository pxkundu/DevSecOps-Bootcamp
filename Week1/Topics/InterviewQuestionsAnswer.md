Concise answers to the 25 interview questions based on **Week 1, Day 3: Networking Deep Dive** topics. These responses are crafted to reflect the knowledge level of an intermediate AWS DevOps or Cloud Engineer, align with Fortune 100 expectations, and incorporate Day 3’s key concepts (e.g., VPC, subnets, Security Groups, routing, DDoS mitigation). 

These are designed to be clear, professional, and demonstrate both theoretical understanding and practical application.

---

### VPC and Networking Basics

1. **What is a VPC, and why would you use one in AWS?**
   - **Answer**: A Virtual Private Cloud (VPC) is a logically isolated network in AWS where I can launch resources like EC2 instances or RDS databases. It’s defined by a CIDR block, such as 10.0.0.0/16, giving me control over IP addressing and routing. I’d use a VPC to isolate workloads—like separating dev and prod environments—ensure security by restricting access, and customize networking with subnets and gateways. For example, it’s critical for compliance in industries like finance where data isolation is mandatory.

2. **Explain the difference between a public subnet and a private subnet.**
   - **Answer**: A public subnet has a route to an Internet Gateway (IGW) in its Route Table, allowing direct internet access—ideal for web servers. For instance, its route might be 0.0.0.0/0 → IGW. A private subnet lacks this route, isolating it from the internet, and typically uses a NAT Gateway for outbound traffic only—like for a database. The key difference is inbound accessibility: public subnets get public IPs; private ones don’t.

3. **How does a CIDR block work, and what does /16 vs. /24 mean in a VPC?**
   - **Answer**: A CIDR block defines an IP range using Classless Inter-Domain Routing notation. The number after the slash (e.g., /16) indicates how many bits are fixed, leaving the rest for hosts. For 10.0.0.0/16, 16 bits are the network (10.0), giving 65,536 IPs (2^16). For 10.0.1.0/24, 24 bits are fixed (10.0.1), leaving 256 IPs (2^8). In a VPC, /16 provides a large pool for multiple subnets, while /24 is a smaller subnet for specific resources like EC2s.

4. **What’s the purpose of an Internet Gateway in a VPC? Can a VPC function without it?**
   - **Answer**: An Internet Gateway (IGW) connects a VPC to the public internet, enabling resources in public subnets to receive inbound traffic and send outbound traffic. It’s attached to the VPC and referenced in a Route Table (e.g., 0.0.0.0/0 → IGW). A VPC can function without it—for example, a fully private VPC for internal apps—but resources won’t have direct internet access unless a NAT Gateway or VPN is used for outbound-only traffic.

5. **Describe how Route Tables control traffic in a VPC. Give an example.**
   - **Answer**: Route Tables define traffic rules in a VPC by mapping destinations to targets. Each subnet associates with a Route Table, and rules like 10.0.0.0/16 → local keep traffic internal, while 0.0.0.0/0 → IGW sends unmatched traffic to the internet. Example: A public subnet’s Route Table has 0.0.0.0/0 → IGW, so an EC2 can serve HTTP; a private subnet’s 0.0.0.0/0 → NAT Gateway allows updates but blocks inbound connections.

---

### Subnets and Availability

6. **How would you design a VPC with high availability across multiple Availability Zones?**
   - **Answer**: I’d create a VPC (e.g., 10.0.0.0/16) and deploy subnets in at least two Availability Zones—like 10.0.1.0/24 in us-east-1a and 10.0.2.0/24 in us-east-1b. Public subnets get an IGW route for web servers, and private subnets use NAT Gateways (one per AZ) for redundancy. I’d place EC2 instances or an Application Load Balancer across AZs and enable Multi-AZ RDS. This ensures failover if one AZ goes down, maintaining high availability.

7. **What’s the role of a NAT Gateway, and when would you use it instead of an Internet Gateway?**
   - **Answer**: A NAT Gateway allows instances in a private subnet to access the internet outbound (e.g., for software updates) while blocking inbound connections, enhancing security. It sits in a public subnet, uses an Elastic IP, and is referenced in the private subnet’s Route Table (0.0.0.0/0 → NAT). I’d use it instead of an IGW when I need isolation—like for a database—since an IGW enables two-way traffic, exposing resources to the public.

8. **Can an EC2 instance in a private subnet access the internet? If so, how?**
   - **Answer**: Yes, it can access the internet outbound via a NAT Gateway. I’d place the NAT Gateway in a public subnet with an IGW route, then configure the private subnet’s Route Table to send 0.0.0.0/0 to the NAT Gateway. The EC2 instance doesn’t need a public IP, as the NAT handles outbound translation. For example, this lets a private EC2 pull Yum updates securely without being directly accessible.

9. **You’re tasked with setting up a VPC with 3 tiers (web, app, DB). How would you assign subnets?**
   - **Answer**: I’d use a VPC (10.0.0.0/16) with three subnet types: public (10.0.1.0/24) for web servers with an IGW route, private (10.0.2.0/24) for app servers with a NAT Gateway route, and private (10.0.3.0/24) for the DB with no internet route. I’d spread each across two AZs (e.g., 10.0.4.0/24 in us-east-1b) for HA. Security Groups would limit traffic: web allows HTTP, app allows app-specific ports, DB only allows app tier access.

10. **What happens if two subnets in a VPC have overlapping CIDR ranges?**
    - **Answer**: Overlapping CIDR ranges (e.g., 10.0.1.0/24 and 10.0.1.0/24) cause routing conflicts, as AWS can’t determine which subnet owns an IP. Creation fails with an error like “CIDR block overlaps with existing subnet.” Traffic could misroute or drop, breaking connectivity. I’d fix it by adjusting one CIDR (e.g., 10.0.2.0/24) to ensure unique ranges within the VPC’s 10.0.0.0/16.

---

### Security Groups and Traffic Control

11. **What’s the difference between a Security Group and a Network ACL (NACL)?**
    - **Answer**: A Security Group is a stateful firewall at the instance level, controlling inbound and outbound traffic with rules (e.g., allow HTTP). It auto-allows return traffic. A Network ACL is stateless, applies at the subnet level, and requires explicit inbound/outbound rules (e.g., allow port 80 in and out). Security Groups are for resource-specific security; NACLs add subnet-wide control—like blocking all SSH at the network layer.

12. **How do Security Groups handle inbound and outbound traffic by default?**
    - **Answer**: By default, a Security Group denies all inbound traffic (no rules) and allows all outbound traffic (0.0.0.0/0, all ports). It’s stateful, so if I allow inbound HTTP (port 80), return traffic is permitted automatically without an outbound rule. I’d add inbound rules like SSH (port 22, my IP) to enable access, while outbound stays open unless restricted for security.

13. **Design a Security Group for a web server that’s publicly accessible but secure.**
    - **Answer**: I’d create a Security Group with: Inbound: HTTP (port 80, 0.0.0.0/0) for public access, HTTPS (port 443, 0.0.0.0/0) for secure traffic, SSH (port 22, my IP or a VPN range like 192.168.1.0/24) for admin access. Outbound: Default all (0.0.0.0/0) for updates, or restrict to specific ports (e.g., 443 for HTTPS APIs). This balances accessibility with security by limiting SSH exposure.

14. **Can you apply multiple Security Groups to an EC2 instance? How do they interact?**
    - **Answer**: Yes, I can apply multiple Security Groups to an EC2 instance. AWS evaluates them with an implicit “OR”—if any group allows traffic, it’s permitted. For example, one group might allow SSH (port 22, my IP), another HTTP (port 80, 0.0.0.0/0). There’s no precedence; all rules combine. Deny rules aren’t supported—only NACLs can explicitly deny—so I’d ensure no unintended overlaps (e.g., overly broad SSH).

15. **What’s a common mistake when configuring Security Groups that blocks legitimate traffic?**
    - **Answer**: A common mistake is forgetting to add an inbound rule for the needed port—like allowing HTTP (port 80) but not SSH (port 22) for admin access, or restricting the source IP too tightly (e.g., my IP changes). Another is misconfiguring outbound rules if customized—like blocking all outbound, preventing updates. I’d double-check rules and test connectivity immediately after applying them.

---

### Troubleshooting and Real-World Scenarios

16. **An EC2 instance in a public subnet can’t be reached via SSH. What would you check first?**
    - **Answer**: I’d first check the Security Group—ensure it has an inbound rule for SSH (port 22, my IP). Next, verify the subnet’s Route Table has 0.0.0.0/0 → IGW and the instance has a public IP. I’d also confirm the key pair matches (e.g., “bootcamp-key.pem”) and the instance is running. Most likely, it’s a missing SSH rule or network misconfig.

17. **Your web application in a VPC suddenly stops responding. How do you diagnose the issue?**
    - **Answer**: I’d start by checking the EC2 instance status (running?) and Security Group (HTTP port 80 allowed?). Then, verify the Route Table—ensure 0.0.0.0/0 → IGW for the public subnet. I’d use CloudWatch Logs for app errors and VPC Flow Logs for dropped packets. If it’s multi-AZ, I’d check AZ health. Likely culprits: Security Group change or IGW detachment.

18. **A private subnet EC2 needs to pull updates from the internet but fails. What’s wrong?**
    - **Answer**: The private subnet probably lacks a NAT Gateway or has a misconfigured Route Table. I’d check if 0.0.0.0/0 points to a NAT Gateway in a public subnet with an IGW. If the NAT’s missing or its Elastic IP is detached, outbound fails. I’d add a NAT, update the Route Table, and test with `yum update`.

19. **You notice high latency between two EC2 instances in a VPC. What might be causing it?**
    - **Answer**: High latency could stem from instances being in different AZs (e.g., us-east-1a vs. 1b), adding cross-AZ latency (~1-2 ms). Other causes: overloaded subnet bandwidth, misconfigured routing (e.g., traffic exiting via NAT), or Security Group rules slowing processing. I’d check placement, ping times, and Flow Logs to pinpoint it.

20. **How would you verify that a Route Table is correctly directing traffic to an Internet Gateway?**
    - **Answer**: I’d go to VPC > Route Tables, select the table, and check the Routes tab for 0.0.0.0/0 → <IGW-ID>. Then, ensure the public subnet is associated with this table (Subnets tab). I’d test by launching an EC2 in that subnet, assigning a public IP, and pinging google.com. If it fails, the IGW might be detached.

---

### DDoS Mitigation and Security

21. **How can Security Groups help mitigate a DDoS attack on an EC2 instance?**
    - **Answer**: Security Groups can limit inbound traffic to trusted sources—like restricting HTTP (port 80) to a specific IP range instead of 0.0.0.0/0, or SSH to a VPN. They can’t block all DDoS traffic (e.g., volumetric attacks), but tightening rules reduces attack surface. I’d pair them with AWS Shield for broader protection.

22. **What AWS service would you pair with a VPC to protect against DDoS attacks at scale?**
    - **Answer**: I’d use AWS Shield, a managed DDoS protection service. Standard Shield auto-mitigates Layer 3/4 attacks (e.g., SYN floods) for free, while Shield Advanced adds Layer 7 protection (e.g., HTTP floods) and cost protection. It integrates with VPC resources like ALBs, complementing Security Groups for comprehensive defense.

23. **A public-facing app is under a brute-force SSH attack. How do you lock it down quickly?**
    - **Answer**: I’d modify the Security Group to restrict SSH (port 22) to my IP or a trusted range (e.g., 192.168.1.0/24) instead of 0.0.0.0/0. I’d apply the change immediately, test SSH from my IP, and monitor CloudTrail for attack patterns. Long-term, I’d use a bastion host or VPN for SSH access.

24. **Explain how you’d configure a VPC to isolate sensitive data from public access.**
    - **Answer**: I’d create a VPC with private subnets (e.g., 10.0.2.0/24) for sensitive data—like an RDS instance—without an IGW route. The Route Table would use a NAT Gateway for outbound updates only. Security Groups would allow only specific app-tier IPs (e.g., port 3306 from 10.0.1.0/24). Public subnets would handle web traffic, fully isolated from the private tier.

25. **Your team reports a subnet is ‘down’ after a network change. How do you investigate and recover?**
    - **Answer**: I’d check the Route Table—ensure 0.0.0.0/0 points to the IGW (public) or NAT (private). Next, verify Security Groups (e.g., HTTP/SSH rules intact) and subnet associations. I’d use VPC Flow Logs to spot dropped traffic and test an EC2’s connectivity. To recover, I’d restore the IGW route or fix Security Group rules, then validate with a ping or HTTP request.

---

These answers showcase a mix of theory (e.g., **CIDR**, **High Availability**), practical steps (e.g., configuring **NAT Gateway**), and troubleshooting (e.g., diagnosing latency), aligning with Day 3’s focus and Fortune 100 rigor. 