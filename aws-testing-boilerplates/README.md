# AWS Testing Boilerplates

A collection of testing-specific AWS DevOps templates for automated testing and security troubleshooting.

## Structure
- **cloudformation/**: S3 security scanning.
- **codebuild/**: Integration testing for ECS services.
- **lambda/**: Compliance scanning with AWS Config.
- **stepfunctions/**: Chaos engineering tests.
- **cloudwatch/**: Security incident monitoring.

## Usage
1. Clone the repo
2. Customize templates (e.g., update ARNs, regions, service names).
3. Deploy using AWS CLI or AWS Console.

## Prerequisites
- AWS CLI
- AWS account with CloudTrail, Config, and SNS enabled
- ECS cluster or Lambda functions for testing

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License
MIT License. See [LICENSE](LICENSE).

---

*Prepared by {Partha Sarathi Kundu} on April 19, 2025, for the AWS Boilerplate writing project.*