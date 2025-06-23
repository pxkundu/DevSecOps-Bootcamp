import typer
import os
from configparser import ConfigParser

app = typer.Typer()

AWS_CREDENTIALS = os.path.expanduser("~/.aws/credentials")
AWS_CONFIG = os.path.expanduser("~/.aws/config")

PROFILE_EMOJI = "👤"
CURRENT_EMOJI = "🎯"
INFO_EMOJI = "ℹ️"
SUCCESS_EMOJI = "✅"
WARNING_EMOJI = "⚠️"
ERROR_EMOJI = "❌"


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


@app.command("list", help="List all AWS profiles 👤")
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


@app.command("current", help="Show current AWS profile 🎯")
def show_current():
    """Display the current AWS profile in use."""
    current = get_current_profile()
    typer.echo(f"{CURRENT_EMOJI} {PROFILE_EMOJI} Current profile: {current}")


@app.command("switch", help="Switch AWS profile for this shell session 🔄")
def switch_profile(profile: str = typer.Argument(..., help="Profile name to switch to")):
    """Switch the AWS profile for the current shell session."""
    profiles = get_profiles()
    if profile not in profiles:
        typer.echo(f"{ERROR_EMOJI} Profile '{profile}' not found.")
        raise typer.Exit(1)
    # Print export command for user to run in their shell
    typer.echo(f"{SUCCESS_EMOJI} To switch profile, run:")
    typer.echo(f"\n  export AWS_PROFILE={profile}\n")
    typer.echo(f"{INFO_EMOJI} (Copy and paste the above command in your shell)")


@app.command("add", help="Add a new AWS profile ➕")
def add_profile():
    """Interactively add a new AWS profile."""
    profile = typer.prompt(f"{PROFILE_EMOJI} Enter new profile name")
    access_key = typer.prompt("🔑 AWS Access Key ID")
    secret_key = typer.prompt("🔒 AWS Secret Access Key", hide_input=True)
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