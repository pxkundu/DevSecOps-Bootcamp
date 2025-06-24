# awdx

**awdx** (AWS DevOps X) is a next-generation, human-friendly CLI tool for AWS DevSecOps. It helps you manage, automate, and secure your AWS environment with simple, interactive commands and smart suggestions.

---

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Status](#status)

---

## Features
- **Profile Management:** Create, switch, and validate AWS profiles interactively.
- **Security Audits:** Scan for misconfigurations, exposed secrets, and risky permissions.
- **Cost Insights:** Get clear summaries of your AWS spending.
- **Resource Checks:** Instantly check S3 buckets, security groups, IAM users, and more for best practices.
- **Automation:** Run common DevSecOps tasks with a single, smart command.
- **Suggestions:** Receive actionable best-practice tips after every action.
- **Human-Friendly CLI:** Simple, memorable commands and interactive prompts.
- **Future:** AI/NLP-powered natural language commands.

---

## Requirements
- Python 3.8+
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [typer](https://typer.tiangolo.com/)

---

## Installation

### From Source
```bash
pip install .
```

### From PyPI (after publishing)
```bash
pip install awdx
```

---

## Usage

Show help and available commands:
```bash
awdx --help
```

Profile management commands:

- List all AWS profiles:
  ```bash
  awdx profile list
  ```
- Show the current AWS profile:
  ```bash
  awdx profile current
  ```
- Switch to a different AWS profile:
  ```bash
  awdx profile switch <profile>
  ```
- Add a new AWS profile interactively:
  ```bash
  awdx profile add
  ```
- Edit an existing AWS profile:
  ```bash
  awdx profile edit <profile>
  ```
- Delete an AWS profile:
  ```bash
  awdx profile delete <profile>
  ```
- Validate credentials and permissions for a profile:
  ```bash
  awdx profile validate <profile>
  ```
- Show profile details and security posture:
  ```bash
  awdx profile info <profile>
  ```
- Suggest best practices for a profile:
  ```bash
  awdx profile suggest <profile>
  ```
- Import profiles from a file (YAML/JSON):
  ```bash
  awdx profile import <file>
  ```
- Export profiles to a file (YAML/JSON):
  ```bash
  awdx profile export <file>
  ```

Example interactive session:
```
$ awdx profile list
👤 Found 3 profiles:
🎯 👤 default (current)
👤 devops
👤 prod

$ awdx profile info devops
ℹ️ Profile: devops
  🔑 AWS Access Key ID: ASIA4TWKQEDUPVYSYMJV
  🌍 Region: N/A
🔒 Security posture:
    ✅ MFA: Check if enabled in AWS Console
    ✅ Key rotation: Rotate keys every 90 days
    🚫 Avoid using root credentials
💡 Tip: Check for MFA and key rotation status for better security.

$ awdx profile suggest devops
💡 Suggestions for profile: devops
✅ Enable MFA for all IAM users.
✅ Rotate access keys every 90 days.
✅ Remove unused or old access keys.
🚫 Avoid using root credentials for automation.
✅ Use least privilege IAM policies.
💡 Tip: Enable MFA, rotate keys regularly, and avoid using root credentials.
```

---

## Project Status

Early development. See `docs/` for design and installation details. 