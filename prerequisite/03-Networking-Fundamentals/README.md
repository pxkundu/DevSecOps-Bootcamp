# 🌐 Networking Fundamentals

## 🎯 Overview

Essential networking concepts, protocols, and terminology you need to understand for DevOps, cloud computing, and infrastructure management. This covers the foundational knowledge required for working with networks in cloud environments.

## 📚 Key Concepts

### **What is Computer Networking?**

**Computer Networking** is the practice of connecting computers and devices to share resources and communicate with each other. In DevOps and cloud computing, understanding networking is crucial for designing, deploying, and troubleshooting applications.

**Why Learn Networking?**
- **Cloud platforms**: AWS VPC, Azure VNet, GCP VPC
- **Container orchestration**: Kubernetes networking
- **Load balancing**: Application distribution
- **Security**: Network security and firewalls
- **Troubleshooting**: Diagnose connectivity issues

## 🌍 Network Types

### **Local Area Network (LAN)**
- **Definition**: Network within a limited geographic area
- **Examples**: Office network, home network
- **Characteristics**: High speed, low latency, private

### **Wide Area Network (WAN)**
- **Definition**: Network spanning large geographic areas
- **Examples**: Internet, corporate networks across cities
- **Characteristics**: Lower speed, higher latency, public/private

### **Virtual Private Network (VPN)**
- **Definition**: Secure connection over public network
- **Purpose**: Remote access, secure communication
- **Types**: Site-to-site, client-to-site

## 🔌 Network Protocols

### **TCP/IP Model**

#### **Application Layer**
- **HTTP/HTTPS**: Web traffic
- **FTP**: File transfer
- **SSH**: Secure shell
- **DNS**: Domain name resolution
- **SMTP**: Email

#### **Transport Layer**
- **TCP**: Reliable, ordered delivery
- **UDP**: Fast, unreliable delivery

#### **Internet Layer**
- **IP**: Internet Protocol
- **ICMP**: Network control messages (ping)
- **ARP**: Address resolution

#### **Network Access Layer**
- **Ethernet**: Local network communication
- **WiFi**: Wireless communication

### **Key Protocols Explained**

#### **HTTP/HTTPS**
- **HTTP**: Hypertext Transfer Protocol (port 80)
- **HTTPS**: HTTP over SSL/TLS (port 443)
- **Purpose**: Web communication
- **Methods**: GET, POST, PUT, DELETE

#### **SSH**
- **Port**: 22
- **Purpose**: Secure remote access
- **Features**: Encryption, authentication
- **Use cases**: Server administration, file transfer

#### **DNS**
- **Purpose**: Convert domain names to IP addresses
- **Process**: Recursive resolution
- **Records**: A, AAAA, CNAME, MX, TXT

## 📡 IP Addressing

### **IPv4 Addressing**
- **Format**: 4 octets (e.g., 192.168.1.1)
- **Range**: 0.0.0.0 to 255.255.255.255
- **Classes**: A, B, C, D, E

#### **Private IP Ranges**
- **Class A**: 10.0.0.0/8
- **Class B**: 172.16.0.0/12
- **Class C**: 192.168.0.0/16

### **IPv6 Addressing**
- **Format**: 8 groups of 16-bit hex (e.g., 2001:db8::1)
- **Benefits**: Larger address space, better security
- **Adoption**: Growing but IPv4 still dominant

### **Subnetting**
- **Purpose**: Divide networks into smaller segments
- **CIDR**: Classless Inter-Domain Routing
- **Examples**: /24 (256 addresses), /16 (65,536 addresses)

## 🔧 Network Devices

### **Routers**
- **Function**: Connect different networks
- **Layer**: Network layer (Layer 3)
- **Purpose**: Route traffic between networks

### **Switches**
- **Function**: Connect devices within a network
- **Layer**: Data link layer (Layer 2)
- **Types**: Unmanaged, managed, PoE

### **Firewalls**
- **Function**: Control network traffic
- **Types**: Network, application, next-generation
- **Features**: Packet filtering, stateful inspection

### **Load Balancers**
- **Function**: Distribute traffic across servers
- **Types**: Application, network, global
- **Algorithms**: Round-robin, least connections, IP hash

## 🛡️ Network Security

### **Security Concepts**

#### **Defense in Depth**
- **Multiple layers** of security controls
- **Network, host, application** level protection
- **Redundancy** in security measures

#### **Zero Trust**
- **Never trust, always verify**
- **Continuous authentication**
- **Least privilege access**

### **Security Technologies**

#### **Firewalls**
- **Network firewalls**: Filter traffic by IP/port
- **Application firewalls**: Filter by application behavior
- **Next-gen firewalls**: Deep packet inspection

#### **VPNs**
- **Site-to-site**: Connect office networks
- **Client-to-site**: Remote worker access
- **SSL/TLS**: Secure web traffic

#### **Intrusion Detection/Prevention**
- **IDS**: Monitor and alert on threats
- **IPS**: Monitor and block threats
- **SIEM**: Security information and event management

## ☁️ Cloud Networking

### **Virtual Private Cloud (VPC)**
- **Definition**: Private network in the cloud
- **Components**: Subnets, route tables, security groups
- **Benefits**: Isolation, customization, security

### **Subnets**
- **Public subnets**: Internet-accessible
- **Private subnets**: Internal only
- **Purpose**: Security and resource organization

### **Security Groups**
- **Virtual firewalls** for cloud resources
- **Stateful**: Track connection state
- **Rules**: Allow/deny traffic by port and source

### **Network ACLs**
- **Stateless**: Don't track connections
- **Subnet level**: Apply to entire subnet
- **Rules**: Allow/deny traffic by IP and port

## 🔍 Network Troubleshooting

### **Common Commands**

#### **Connectivity Testing**
```bash
ping          # Test connectivity to host
traceroute    # Show network path to host
nslookup      # DNS resolution testing
dig           # Detailed DNS queries
```

#### **Network Information**
```bash
ipconfig      # Windows network configuration
ifconfig      # Linux network configuration
netstat       # Network connections and statistics
ss            # Socket statistics
```

#### **Port Testing**
```bash
telnet        # Test port connectivity
nc            # Netcat for port scanning
nmap          # Network discovery and port scanning
```

### **Troubleshooting Process**
1. **Identify the problem**: What's not working?
2. **Gather information**: Check logs, run diagnostics
3. **Isolate the issue**: Determine scope and location
4. **Test solutions**: Try fixes systematically
5. **Verify resolution**: Confirm the fix works
6. **Document**: Record the solution

## 📊 Network Monitoring

### **Key Metrics**
- **Bandwidth**: Data transfer rate
- **Latency**: Response time
- **Packet loss**: Dropped packets
- **Jitter**: Variation in latency
- **Throughput**: Actual data transfer

### **Monitoring Tools**
- **SNMP**: Simple Network Management Protocol
- **NetFlow**: Network traffic analysis
- **Packet capture**: Wireshark, tcpdump
- **Cloud monitoring**: AWS CloudWatch, Azure Monitor

## 📋 Self-Check Questions

### **Basic Concepts**
1. **Q**: What is the difference between LAN and WAN?
   **A**: LAN is local area network, WAN is wide area network

2. **Q**: What port does HTTP use?
   **A**: Port 80

3. **Q**: What is a subnet?
   **A**: A division of a network into smaller segments

### **IP Addressing**
4. **Q**: What is a private IP address range?
   **A**: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16

5. **Q**: What does /24 mean in CIDR notation?
   **A**: 24 bits for network, 8 bits for hosts (256 addresses)

### **Security**
6. **Q**: What is a firewall?
   **A**: Device that controls network traffic based on rules

7. **Q**: What is the purpose of a VPN?
   **A**: Secure connection over public network

## 🎯 Practice Exercises

### **Beginner Level**
1. **Test connectivity**: Use `ping` and `traceroute`
2. **Check network configuration**: Use `ipconfig`/`ifconfig`
3. **Test DNS resolution**: Use `nslookup` and `dig`
4. **Check open ports**: Use `netstat` and `ss`

### **Intermediate Level**
1. **Configure network settings**: Set up static IP
2. **Troubleshoot connectivity**: Diagnose network issues
3. **Use packet capture**: Basic Wireshark analysis
4. **Configure firewall rules**: Basic firewall setup

### **Advanced Level**
1. **Design network architecture**: Plan subnet layout
2. **Implement security measures**: Configure firewalls and VPNs
3. **Monitor network performance**: Set up monitoring tools
4. **Troubleshoot complex issues**: Multi-layer problem solving

## 🔗 Additional Resources

### **Learning Platforms**
- [Cisco Networking Academy](https://www.netacad.com/) - Free networking courses
- [CompTIA Network+](https://www.comptia.org/certifications/network) - Networking certification
- [Packet Pushers](https://packetpushers.net/) - Networking podcast and blog

### **Practice Tools**
- [GNS3](https://www.gns3.com/) - Network simulation
- [Wireshark](https://www.wireshark.org/) - Packet analysis
- [Nmap](https://nmap.org/) - Network discovery

### **Online Labs**
- [Cisco Packet Tracer](https://www.netacad.com/courses/packet-tracer) - Network simulation
- [TryHackMe](https://tryhackme.com/) - Cybersecurity labs
- [HackTheBox](https://www.hackthebox.com/) - Penetration testing practice

## 🔗 Related Prerequisites

- [Cloud Computing Basics](../01-Cloud-Computing-Basics/README.md) - VPC and cloud networking
- [Security Basics](../06-Security-Basics/README.md) - Network security concepts
- [DevOps Fundamentals](../05-DevOps-Fundamentals/README.md) - Network automation

---

**Ready for the next step?** Move on to [Programming & Scripting](../04-Programming-Scripting/README.md) to learn coding fundamentals!
