# 🔒 Security Basics

## 🎯 Overview

Essential security concepts, threats, and best practices you need to understand for DevSecOps work. This covers foundational security knowledge required for building secure applications and infrastructure.

## 📚 Key Concepts

### **What is Information Security?**

**Information Security** is the practice of protecting information and information systems from unauthorized access, use, disclosure, disruption, modification, or destruction.

**Core Principles (CIA Triad):**
- **Confidentiality**: Information is accessible only to authorized users
- **Integrity**: Information is accurate and complete
- **Availability**: Information is accessible when needed

### **Why Security Matters in DevOps**
- **Data breaches** can cost millions in damages
- **Compliance requirements** for many industries
- **Customer trust** depends on security
- **Regulatory penalties** for security failures
- **Business continuity** requires secure systems

## 🛡️ Security Threats

### **Common Attack Vectors**

#### **Malware**
- **Viruses**: Self-replicating malicious code
- **Worms**: Network-spreading malware
- **Trojans**: Disguised malicious software
- **Ransomware**: Encrypts data for ransom

#### **Social Engineering**
- **Phishing**: Fraudulent emails/messages
- **Pretexting**: False scenarios to gain information
- **Baiting**: Physical media with malware
- **Quid pro quo**: Service for information exchange

#### **Network Attacks**
- **DDoS**: Distributed Denial of Service
- **Man-in-the-Middle**: Intercepting communications
- **Packet sniffing**: Capturing network traffic
- **Port scanning**: Discovering open services

#### **Application Attacks**
- **SQL Injection**: Database query manipulation
- **Cross-Site Scripting (XSS)**: Client-side code injection
- **Cross-Site Request Forgery (CSRF)**: Unauthorized actions
- **Buffer Overflow**: Memory corruption attacks

### **OWASP Top 10**

#### **2021 OWASP Top 10**
1. **Broken Access Control**: Unauthorized access to resources
2. **Cryptographic Failures**: Weak encryption implementation
3. **Injection**: Code injection attacks
4. **Insecure Design**: Flaws in architecture/design
5. **Security Misconfiguration**: Poor security settings
6. **Vulnerable Components**: Outdated/unsafe dependencies
7. **Authentication Failures**: Weak authentication systems
8. **Software and Data Integrity**: Untrusted data/code
9. **Security Logging Failures**: Insufficient monitoring
10. **Server-Side Request Forgery**: Forced server requests

## 🔐 Authentication & Authorization

### **Authentication (Who are you?)**

#### **Authentication Factors**
- **Something you know**: Passwords, PINs
- **Something you have**: Tokens, smart cards
- **Something you are**: Biometrics (fingerprint, face)

#### **Multi-Factor Authentication (MFA)**
- **Two-factor authentication (2FA)**: Two factors required
- **Time-based One-Time Password (TOTP)**: Google Authenticator
- **SMS/Email codes**: Secondary verification
- **Hardware tokens**: Physical security devices

### **Authorization (What can you do?)**

#### **Access Control Models**
- **Discretionary Access Control (DAC)**: Owner decides access
- **Mandatory Access Control (MAC)**: System enforces access
- **Role-Based Access Control (RBAC)**: Access based on roles
- **Attribute-Based Access Control (ABAC)**: Access based on attributes

#### **Principle of Least Privilege**
- **Minimum necessary permissions** for tasks
- **Regular permission reviews** and updates
- **Just-in-time access** for temporary needs
- **Separation of duties** for critical functions

## 🔒 Cryptography

### **Encryption Types**

#### **Symmetric Encryption**
- **Same key** for encryption and decryption
- **Fast and efficient** for large data
- **Key management** challenges
- **Examples**: AES, DES, 3DES

#### **Asymmetric Encryption**
- **Public/private key pairs**
- **Secure key exchange**
- **Digital signatures**
- **Examples**: RSA, ECC, DSA

### **Hash Functions**
- **One-way functions**: Cannot be reversed
- **Deterministic**: Same input = same output
- **Collision resistance**: Hard to find same hash
- **Examples**: SHA-256, MD5, bcrypt

### **Digital Signatures**
- **Verify authenticity** of messages
- **Non-repudiation**: Cannot deny sending
- **Integrity checking**: Detect tampering
- **Certificate-based**: PKI infrastructure

## 🌐 Network Security

### **Network Security Controls**

#### **Firewalls**
- **Packet filtering**: Allow/deny based on rules
- **Stateful inspection**: Track connection state
- **Application-level**: Deep packet inspection
- **Next-generation**: Advanced threat protection

#### **Intrusion Detection/Prevention**
- **IDS**: Monitor and alert on threats
- **IPS**: Monitor and block threats
- **Signature-based**: Known attack patterns
- **Behavior-based**: Anomaly detection

#### **Virtual Private Networks (VPN)**
- **Site-to-site**: Connect office networks
- **Client-to-site**: Remote worker access
- **SSL/TLS**: Secure web traffic
- **IPsec**: Network layer security

### **Network Segmentation**
- **DMZ**: Demilitarized zone for public services
- **VLANs**: Virtual LAN separation
- **Micro-segmentation**: Fine-grained network control
- **Zero Trust**: Never trust, always verify

## ☁️ Cloud Security

### **Cloud Security Challenges**
- **Shared responsibility model**
- **Data sovereignty** and compliance
- **Identity management** across services
- **API security** and access control

### **Cloud Security Best Practices**

#### **Identity and Access Management**
- **Strong authentication** with MFA
- **Role-based permissions** (RBAC)
- **Regular access reviews**
- **Principle of least privilege**

#### **Data Protection**
- **Encryption at rest** and in transit
- **Key management** services
- **Data classification** and labeling
- **Backup and recovery** procedures

#### **Network Security**
- **Virtual Private Clouds (VPC)**
- **Security groups** and NACLs
- **Web Application Firewalls (WAF)**
- **DDoS protection** services

## 🔍 Security Monitoring

### **Security Information and Event Management (SIEM)**
- **Log collection** and aggregation
- **Real-time analysis** and correlation
- **Alert generation** and response
- **Compliance reporting** and auditing

### **Threat Detection**
- **Signature-based**: Known threat patterns
- **Behavior-based**: Anomaly detection
- **Machine learning**: AI-powered detection
- **Threat intelligence**: External threat feeds

### **Incident Response**
- **Preparation**: Plans and procedures
- **Identification**: Detect security incidents
- **Containment**: Limit incident scope
- **Eradication**: Remove threat
- **Recovery**: Restore normal operations
- **Lessons learned**: Improve processes

## 🧪 Security Testing

### **Types of Security Testing**

#### **Static Application Security Testing (SAST)**
- **Code analysis** for vulnerabilities
- **Early detection** in development
- **Automated scanning** in CI/CD
- **False positive** management

#### **Dynamic Application Security Testing (DAST)**
- **Runtime testing** of applications
- **Black-box testing** approach
- **Real-world attack simulation**
- **Production-like environment** testing

#### **Penetration Testing**
- **Authorized security assessment**
- **Manual testing** by security experts
- **Comprehensive vulnerability** discovery
- **Remediation recommendations**

### **Vulnerability Assessment**
- **Automated scanning** tools
- **Regular assessments** and updates
- **Risk prioritization** and scoring
- **Remediation tracking** and verification

## 📋 Security Frameworks

### **NIST Cybersecurity Framework**
- **Identify**: Understand security risks
- **Protect**: Implement safeguards
- **Detect**: Identify security events
- **Respond**: Take action on incidents
- **Recover**: Maintain resilience

### **ISO 27001**
- **Information Security Management System**
- **Risk-based approach** to security
- **Continuous improvement** cycle
- **International standard** for security

### **OWASP SAMM**
- **Software Assurance Maturity Model**
- **Security practices** across SDLC
- **Maturity levels** and roadmaps
- **Measurement and improvement**

## 📋 Self-Check Questions

### **Security Concepts**
1. **Q**: What are the three principles of the CIA triad?
   **A**: Confidentiality, Integrity, Availability

2. **Q**: What is the difference between authentication and authorization?
   **A**: Authentication verifies identity, authorization determines access

3. **Q**: What is the principle of least privilege?
   **A**: Grant minimum necessary permissions for tasks

### **Threats and Attacks**
4. **Q**: What is a DDoS attack?
   **A**: Distributed Denial of Service - overwhelming system with traffic

5. **Q**: What is SQL injection?
   **A**: Inserting malicious SQL code into database queries

6. **Q**: What is phishing?
   **A**: Fraudulent attempts to steal sensitive information

### **Security Controls**
7. **Q**: What is MFA?
   **A**: Multi-Factor Authentication - using multiple verification methods

8. **Q**: What is a firewall?
   **A**: Network security device that controls traffic based on rules

## 🎯 Practice Exercises

### **Beginner Level**
1. **Set up password policies** and MFA
2. **Configure basic firewall rules**
3. **Implement HTTPS** for web applications
4. **Create security awareness** training

### **Intermediate Level**
1. **Set up vulnerability scanning** in CI/CD
2. **Implement secrets management**
3. **Configure network segmentation**
4. **Create incident response** procedures

### **Advanced Level**
1. **Design secure architecture** patterns
2. **Implement zero trust** security model
3. **Set up comprehensive monitoring** and alerting
4. **Conduct penetration testing** exercises

## 🔗 Additional Resources

### **Security Standards**
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [ISO 27001](https://www.iso.org/isoiec-27001-information-security.html)

### **Learning Platforms**
- [Cybrary](https://www.cybrary.it/) - Free cybersecurity courses
- [SANS](https://www.sans.org/) - Security training and certifications
- [TryHackMe](https://tryhackme.com/) - Hands-on security labs

### **Security Tools**
- [Nmap](https://nmap.org/) - Network discovery and security auditing
- [Wireshark](https://www.wireshark.org/) - Network protocol analyzer
- [Metasploit](https://www.metasploit.com/) - Penetration testing framework
- [Burp Suite](https://portswigger.net/burp) - Web application security testing

## 🔗 Related Prerequisites

- [Networking Fundamentals](../03-Networking-Fundamentals/README.md) - Network security concepts
- [DevOps Fundamentals](../05-DevOps-Fundamentals/README.md) - DevSecOps practices
- [Tools & Technologies](../09-Tools-Technologies/README.md) - Security tools

---

**Ready for the next step?** Move on to [Data & AI/ML Concepts](../07-Data-AI-ML-Concepts/README.md) to learn data fundamentals!
