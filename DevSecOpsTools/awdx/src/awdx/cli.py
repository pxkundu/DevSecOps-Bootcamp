import typer
from .profilyze.profile_commands import profile_app

app = typer.Typer(help="awdx: AWS DevOps X - Human-friendly AWS DevSecOps CLI tool.")
app.add_typer(profile_app, name="profile")

ASCII_ART = r"""
 █████╗ ██╗    ██╗█████╗ ██╗  ██╗
██╔══██╗██║    ██║██╔═██╗╚██╗██╔╝
███████║██║ █╗ ██║██║ ██║ ╚███╔╝
██╔══██║██║███╗██║██║ ██║ ██╔██╗
██║  ██║╚███╔███╔╝█████╔╝██╔╝ ██╗
╚═╝  ╚═╝ ╚══╝╚══╝ ╚════╝ ╚═╝  ╚═╝
"""

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ASCII_ART)
        help_text = ctx.get_help()
        typer.echo(help_text)
        about_block = (
            "\u256D\u2500 About " + "\u2500" * 56 + "\u256E\n"
            "\u2502 Developed by: Partha Sarathi Kundu" + " " * 29 + "\u2502\n"
            "\u2502 Github: @pxkundu" + " " * 47 + "\u2502\n"
            "\u2570" + "\u2500" * 64 + "\u256F\n"
        )
        typer.echo(about_block)

if __name__ == "__main__":
    app() 