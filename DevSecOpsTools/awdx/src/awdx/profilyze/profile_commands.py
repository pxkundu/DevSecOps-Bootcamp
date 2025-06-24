import typer
import os
from configparser import ConfigParser
import json
import csv
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

profile_app = typer.Typer(help="Profile management commands.")

AWS_CREDENTIALS = os.path.expanduser("~/.aws/credentials")
AWS_CONFIG = os.path.expanduser("~/.aws/config")

PROFILE_EMOJI = "👤"
CURRENT_EMOJI = "🎯"
INFO_EMOJI = "ℹ️"
SUCCESS_EMOJI = "✅"
WARNING_EMOJI = "⚠️"
ERROR_EMOJI = "❌"
KEY_EMOJI = "🔑"
TIP_EMOJI = "💡"
SECURITY_EMOJI = "🔒"
DANGER_EMOJI = "❗"
BEST_PRACTICE_EMOJI = "✅"
AVOID_EMOJI = "🚫"

def get_profiles():
    profiles = set()
    if os.path.exists(AWS_CREDENTIALS):
        cp = ConfigParser()
        cp.read(AWS_CREDENTIALS)
        profiles.update(cp.sections())
    if os.path.exists(AWS_CONFIG):
        cp = ConfigParser()
        cp.read(AWS_CONFIG)
        for section in cp.sections():
            if section.startswith("profile "):
                profiles.add(section.replace("profile ", ""))
            else:
                profiles.add(section)
    return sorted(profiles)

def get_current_profile():
    return os.environ.get("AWS_PROFILE") or "default"

@profile_app.command("list", help="List all AWS profiles 👤")
def list_profiles():
    """Show all available AWS profiles."""
    profiles = get_profiles()
    current = get_current_profile()
    typer.echo(f"{INFO_EMOJI} Found {len(profiles)} profiles:")
    for p in profiles:
        if p == current:
            typer.echo(f"{CURRENT_EMOJI} {PROFILE_EMOJI} {p} (current)")
        else:
            typer.echo(f"{PROFILE_EMOJI} {p}")
    typer.echo(f"{TIP_EMOJI} Tip: Use 'awdx profile info <PROFILE>' to see details about a profile.")

@profile_app.command("current", help="Show current AWS profile 🎯")
def show_current():
    """Display the current AWS profile in use."""
    current = get_current_profile()
    typer.echo(f"{CURRENT_EMOJI} {PROFILE_EMOJI} Current profile: {current}")
    typer.echo(f"{TIP_EMOJI} Tip: Use 'awdx profile switch <PROFILE>' to change the active profile.")

@profile_app.command("switch", help="Switch AWS profile for this shell session 🔄")
def switch_profile(profile: str = typer.Argument(..., help="Profile name to switch to")):
    """Switch the AWS profile for the current shell session."""
    profiles = get_profiles()
    if profile not in profiles:
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} Profile '{profile}' not found.")
        raise typer.Exit(1)
    # Print export command for user to run in their shell
    typer.echo(f"{SUCCESS_EMOJI} To switch profile, run:")
    typer.echo(f"\n  export AWS_PROFILE={profile}\n")
    typer.echo(f"{INFO_EMOJI} (Copy and paste the above command in your shell)")
    typer.echo(f"{TIP_EMOJI} Tip: Switching profiles helps you manage different AWS environments easily.")

@profile_app.command("add", help="Add a new AWS profile ➕")
def add_profile():
    """Interactively add a new AWS profile."""
    profile = typer.prompt(f"{PROFILE_EMOJI} Enter new profile name")
    access_key = typer.prompt(f"{KEY_EMOJI} AWS Access Key ID")
    secret_key = typer.prompt(f"{SECURITY_EMOJI} AWS Secret Access Key", hide_input=True)
    region = typer.prompt("🌍 Default region name", default="us-east-1")

    cp = ConfigParser()
    if os.path.exists(AWS_CREDENTIALS):
        cp.read(AWS_CREDENTIALS)
    cp[profile] = {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
        "region": region
    }
    with open(AWS_CREDENTIALS, "w") as f:
        cp.write(f)
    typer.echo(f"{SUCCESS_EMOJI} Profile '{profile}' added!")
    typer.echo(f"{TIP_EMOJI} Tip: Use strong secrets {SECURITY_EMOJI} and never share your AWS credentials {AVOID_EMOJI}.")

@profile_app.command("edit", help="Edit an existing AWS profile ✏️")
def edit_profile(profile: str = typer.Argument(..., help="Profile name to edit")):
    """Edit an existing AWS profile."""
    profiles = get_profiles()
    if profile not in profiles:
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} Profile '{profile}' not found.")
        raise typer.Exit(1)
    cp = ConfigParser()
    if os.path.exists(AWS_CREDENTIALS):
        cp.read(AWS_CREDENTIALS)
    if profile not in cp:
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} Profile '{profile}' not found in credentials file.")
        raise typer.Exit(1)
    typer.echo(f"✏️ Editing profile: {profile}")
    # Prompt for fields to edit
    edit_access_key = typer.confirm(f"Edit AWS Access Key ID {KEY_EMOJI}?", default=False)
    edit_secret_key = typer.confirm(f"Edit AWS Secret Access Key {SECURITY_EMOJI}?", default=False)
    edit_region = typer.confirm("Edit region?", default=False)
    if edit_access_key:
        cp[profile]["aws_access_key_id"] = typer.prompt(f"{KEY_EMOJI} New AWS Access Key ID")
    if edit_secret_key:
        cp[profile]["aws_secret_access_key"] = typer.prompt(f"{SECURITY_EMOJI} New AWS Secret Access Key", hide_input=True)
    if edit_region:
        cp[profile]["region"] = typer.prompt("🌍 New region name", default=cp[profile].get("region", "us-east-1"))
    with open(AWS_CREDENTIALS, "w") as f:
        cp.write(f)
    typer.echo(f"{SUCCESS_EMOJI} Profile '{profile}' updated!")
    typer.echo(f"{TIP_EMOJI} Tip: Regularly update your credentials and region settings.")

@profile_app.command("delete", help="Delete an AWS profile 🗑️")
def delete_profile(profile: str = typer.Argument(..., help="Profile name to delete")):
    """Delete an AWS profile."""
    profiles = get_profiles()
    if profile not in profiles:
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} Profile '{profile}' not found.")
        raise typer.Exit(1)
    confirm = typer.confirm(f"{DANGER_EMOJI} Are you sure you want to delete profile '{profile}'? This cannot be undone.")
    if not confirm:
        typer.echo("Aborted.")
        raise typer.Exit(0)
    # Remove from credentials
    cp = ConfigParser()
    if os.path.exists(AWS_CREDENTIALS):
        cp.read(AWS_CREDENTIALS)
        if profile in cp:
            cp.remove_section(profile)
            with open(AWS_CREDENTIALS, "w") as f:
                cp.write(f)
    # Remove from config
    cp2 = ConfigParser()
    if os.path.exists(AWS_CONFIG):
        cp2.read(AWS_CONFIG)
        section_name = f"profile {profile}" if f"profile {profile}" in cp2 else profile
        if section_name in cp2:
            cp2.remove_section(section_name)
            with open(AWS_CONFIG, "w") as f:
                cp2.write(f)
    typer.echo(f"{SUCCESS_EMOJI} Profile '{profile}' deleted!")
    typer.echo(f"{TIP_EMOJI} Tip: Remove unused profiles to keep your environment clean and secure {BEST_PRACTICE_EMOJI}.")

@profile_app.command("validate", help="Validate AWS profile credentials and permissions ✅")
def validate_profile(profile: str = typer.Argument(..., help="Profile name to validate")):
    """Validate credentials and permissions for a profile."""
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound
    try:
        session = boto3.Session(profile_name=profile)
        sts = session.client("sts")
        identity = sts.get_caller_identity()
        typer.echo(f"{SUCCESS_EMOJI} Profile '{profile}' is valid. Account: {identity['Account']}, ARN: {identity['Arn']}")
        typer.echo(f"{TIP_EMOJI} Tip: Validate profiles regularly to avoid unexpected permission issues {BEST_PRACTICE_EMOJI}.")
    except ProfileNotFound:
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} Profile '{profile}' not found.")
    except NoCredentialsError:
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} No credentials found for profile '{profile}'.")
    except ClientError as e:
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} Profile '{profile}' is invalid or lacks permissions: {e}")
    except Exception as e:
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} Unexpected error: {e}")

@profile_app.command("info", help="Show profile details and security posture ℹ️")
def info_profile(profile: str = typer.Argument(..., help="Profile name to show info for")):
    """Show profile details and security posture."""
    profiles = get_profiles()
    if profile not in profiles:
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} Profile '{profile}' not found.")
        raise typer.Exit(1)
    cp = ConfigParser()
    if os.path.exists(AWS_CREDENTIALS):
        cp.read(AWS_CREDENTIALS)
    if profile not in cp:
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} Profile '{profile}' not found in credentials file.")
        raise typer.Exit(1)
    typer.echo(f"{INFO_EMOJI} Profile: {profile}")
    typer.echo(f"  {KEY_EMOJI} AWS Access Key ID: {cp[profile].get('aws_access_key_id', 'N/A')}")
    typer.echo(f"  🌍 Region: {cp[profile].get('region', 'N/A')}")
    # Security posture (static for now)
    typer.echo(f"{SECURITY_EMOJI} Security posture:")
    typer.echo(f"    {BEST_PRACTICE_EMOJI} MFA: Check if enabled in AWS Console")
    typer.echo(f"    {BEST_PRACTICE_EMOJI} Key rotation: Rotate keys every 90 days")
    typer.echo(f"    {AVOID_EMOJI} Avoid using root credentials")
    typer.echo(f"{TIP_EMOJI} Tip: Check for MFA and key rotation status for better security.")

@profile_app.command("suggest", help="Show best-practice suggestions for a profile 💡")
def suggest_profile(profile: str = typer.Argument(..., help="Profile name to suggest for")):
    """Show best-practice suggestions for a profile."""
    profiles = get_profiles()
    if profile not in profiles:
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} Profile '{profile}' not found.")
        raise typer.Exit(1)
    cp = ConfigParser()
    if os.path.exists(AWS_CREDENTIALS):
        cp.read(AWS_CREDENTIALS)
    typer.echo(f"{TIP_EMOJI} Suggestions for profile: {profile}")
    # Static suggestions for now
    typer.echo(f"{BEST_PRACTICE_EMOJI} Enable MFA for all IAM users.")
    typer.echo(f"{BEST_PRACTICE_EMOJI} Rotate access keys every 90 days.")
    typer.echo(f"{BEST_PRACTICE_EMOJI} Remove unused or old access keys.")
    typer.echo(f"{AVOID_EMOJI} Avoid using root credentials for automation.")
    typer.echo(f"{BEST_PRACTICE_EMOJI} Use least privilege IAM policies.")
    typer.echo(f"{TIP_EMOJI} Tip: Enable MFA, rotate keys regularly, and avoid using root credentials.")

@profile_app.command("import", help="Import profiles from a file 📥")
def import_profiles(file: str = typer.Argument(..., help="File to import profiles from")):
    """Import profiles from a YAML, JSON, or CSV file."""
    if not os.path.exists(file):
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} File '{file}' not found.")
        raise typer.Exit(1)
    data = None
    if file.endswith(".csv"):
        data = {}
        with open(file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            required_fields = {"profile", "aws_access_key_id", "aws_secret_access_key", "region"}
            if not required_fields.issubset(reader.fieldnames):
                typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} CSV must have columns: profile, aws_access_key_id, aws_secret_access_key, region.")
                raise typer.Exit(1)
            for row in reader:
                prof = row["profile"].strip()
                vals = {
                    "aws_access_key_id": row["aws_access_key_id"].strip(),
                    "aws_secret_access_key": row["aws_secret_access_key"].strip(),
                    "region": row["region"].strip()
                }
                data[prof] = vals
    else:
        with open(file, "r") as f:
            if HAS_YAML and (file.endswith(".yaml") or file.endswith(".yml")):
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
    if not isinstance(data, dict):
        typer.echo(f"{DANGER_EMOJI} {ERROR_EMOJI} Invalid file format. Expected a dict of profiles.")
        raise typer.Exit(1)
    cp = ConfigParser()
    if os.path.exists(AWS_CREDENTIALS):
        cp.read(AWS_CREDENTIALS)
    for prof, vals in data.items():
        if prof in cp:
            overwrite = typer.confirm(f"{WARNING_EMOJI} Profile '{prof}' exists. Overwrite?", default=False)
            if not overwrite:
                continue
        cp[prof] = vals
    with open(AWS_CREDENTIALS, "w") as f:
        cp.write(f)
    typer.echo(f"{SUCCESS_EMOJI} Imported {len(data)} profiles from '{file}'.")
    typer.echo(f"{TIP_EMOJI} Tip: Use import to quickly set up profiles on a new machine.")

@profile_app.command("export", help="Export profiles to a file 📤")
def export_profiles(file: str = typer.Argument(..., help="File to export profiles to")):
    """Export all profiles to a YAML or JSON file."""
    cp = ConfigParser()
    if os.path.exists(AWS_CREDENTIALS):
        cp.read(AWS_CREDENTIALS)
    data = {section: dict(cp[section]) for section in cp.sections()}
    with open(file, "w") as f:
        if HAS_YAML and (file.endswith(".yaml") or file.endswith(".yml")):
            yaml.safe_dump(data, f)
        else:
            json.dump(data, f, indent=2)
    typer.echo(f"{SUCCESS_EMOJI} Exported {len(data)} profiles to '{file}'.")
    typer.echo(f"{TIP_EMOJI} Tip: Export your profiles regularly for backup and disaster recovery {BEST_PRACTICE_EMOJI}.") 