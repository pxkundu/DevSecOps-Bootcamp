# Profilyze: AWS Profile Manager CLI - Design Document

## Vision
Profilyze aims to be the smartest, most intuitive, and lightweight AWS profile manager for DevOps engineers. Inspired by the UX and efficiency of tools like `kubectl`, `aws`, `kubectx`, `npm`, and `docker`, Profilyze will make creating, switching, validating, and managing AWS CLI profiles seamless and secure.

---

## Core Features
- **List Profiles:** Show all configured AWS profiles with active/last-used indicators.
- **Switch Profile:** Set the default profile for the current shell/session.
- **Add Profile:** Interactive creation of new profiles (access key, secret, region, MFA, role assumption).
- **Edit Profile:** Update credentials, region, or other settings for an existing profile.
- **Delete Profile:** Remove a profile safely.
- **Validate Profile:** Test credentials and permissions for a profile.
- **Profile Info:** Show details, last used, and security posture (MFA, key age, etc.).
- **Best Practice Suggestions:** Automated recommendations (e.g., enable MFA, rotate keys, avoid root, etc.).
- **Import/Export:** Backup and restore profiles (YAML/JSON).
- **Quick Context:** Show current profile and region in prompt (optional shell integration).

---

## User Experience Principles
- **Fast:** Sub-second response for all commands.
- **Intuitive:** Simple, memorable commands and flags.
- **Interactive:** Guided prompts for profile creation and editing.
- **Safe:** Warnings and confirmations for destructive actions.
- **Scriptable:** All commands support non-interactive mode for automation.
- **Extensible:** Easy to add new commands or plugins.

---

## CLI Structure (Commands & Subcommands)
```
awdx profile list                # List all profiles
awdx profile current             # Show current AWS profile and region
awdx profile switch <PROFILE>    # Switch to a profile
awdx profile add                 # Add a new profile (interactive)
awdx profile edit <PROFILE>      # Edit an existing profile
awdx profile delete <PROFILE>    # Delete a profile
awdx profile validate <PROFILE>  # Validate credentials and permissions
awdx profile info <PROFILE>      # Show profile details and security posture
awdx profile suggest <PROFILE>   # Suggest best practices for a profile
awdx profile import <FILE>       # Import profiles from file
awdx profile export <FILE>       # Export profiles to file
awdx profile help                # Show help for profile commands
```

---

## Extensibility
- **Plugin System:** Allow custom commands/plugins (e.g., `profilyze plugin install <name>`)
- **Shell Integration:** Optional prompt customization to show current profile/region
- **Configurable Output:** Support for table, JSON, YAML outputs

---

## Technical Stack
- **Language:** Python 3.8+
- **CLI Framework:** [Typer](https://typer.tiangolo.com/) (or Click, for fast, modern CLI UX)
- **AWS SDK:** boto3
- **Config Handling:** Read/write to `~/.aws/credentials` and `~/.aws/config`
- **Prompting:** [questionary](https://github.com/tmbo/questionary) or [InquirerPy](https://github.com/kazhala/InquirerPy) for interactive prompts
- **Packaging:** pip-installable, single-file binary via PyInstaller or similar
- **Testing:** pytest
- **Linting/Formatting:** black, flake8

---

## Security Considerations
- Never log or display secrets/access keys
- Securely handle temporary credentials and MFA
- Warn on risky actions (e.g., using root credentials)
- Optionally support credential encryption at rest

---

## Example Usage
```
$ profilyze list
* default      (last used: 2h ago)
  devops       (last used: 1d ago)
  prod         (last used: 3d ago)

$ profilyze use devops
Switched to profile: devops

$ profilyze add
[Prompted for access key, secret, region, MFA, etc.]
Profile 'test' added and validated!

$ profilyze suggest devops
[Best practice suggestions: enable MFA, rotate keys, ...]
```

---

## Future Enhancements
- Profile sync across machines (cloud backup)
- Integration with SSO/Identity providers
- Profile usage analytics
- GUI frontend

---

*Profilyze will empower DevOps engineers to manage AWS profiles with confidence, speed, and security.* 