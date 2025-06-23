# Profilyze (Profile Management for awdx)

Profilyze is the profile management module of the **awdx** CLI tool. It provides a simple, interactive, and emoji-powered experience for managing AWS CLI profiles as part of your DevSecOps workflow.

## Usage
All Profilyze commands are available as subcommands under:
```
awdx profile <command>
```

## Available Commands

### 🟢 List Profiles
```
awdx profile list
```
Lists all AWS profiles found in your `~/.aws/credentials` and `~/.aws/config` files. The current profile is highlighted with a ⭐.

### ⭐ Show Current Profile
```
awdx profile current
```
Displays the currently active AWS profile (from the `AWS_PROFILE` environment variable or default).

### 🔄 Switch Profile
```
awdx profile switch <profile>
```
Prints the export command to switch your AWS profile for the current shell session. Copy and paste the command to activate the profile.

### ➕ Add New Profile
```
awdx profile add
```
Interactively prompts for profile name, access key, secret key, and region, then adds the new profile to your AWS credentials file.

---

All commands use unique emojis and concise info for a delightful, out-of-the-box CLI experience. Profilyze is your friendly AWS profile manager, now part of the awdx DevSecOps toolkit. 