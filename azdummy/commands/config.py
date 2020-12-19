import typer
from dotenv import set_key
from pydantic import SecretBytes
from rich.panel import Panel
from rich.prompt import Confirm

from azdummy import config_path, console, reset_config, settings, state
from azdummy.core.typer import AZDTyper

app = AZDTyper()


@app.command()
def show(
    types: bool = typer.Option(
        False, "--types", help="Show expected field types for configuration"
    )
):
    """
    Show the configuration.

    By default, does not show secrets. If using --verbose, secrets will be shown in plaintext.
    """
    if types:
        console.print(Panel.fit("[bold yellow]Field Types[/bold yellow]"))
        console.print(settings.fields)

    output = {}
    for k, v in settings.dict().items():
        if isinstance(v, SecretBytes):
            if state["verbose"]:
                v = v.get_secret_value().decode()
            else:
                v = v.display()

        output[k] = v

    console.print(Panel.fit(f"[bold red]Config File:[/bold red] {config_path}"))
    console.print(output)


@app.command()
def launch():
    """
    Opens the configuration file in default editor
    """
    if not typer.launch(config_path.as_uri()):
        console.print()


@app.command(name="set")
def set_env_key(
    key: str = typer.Argument(
        ...,
        help="Key to set. Must exist in config.",
        case_sensitive=False,
        callback=lambda x: x.upper(),
    ),
    value: str = typer.Argument(..., help="Value to set for key."),
):
    """
    Set a configuration key/value pair.
    """
    if key not in settings.fields:
        fields_list = "\n".join([k for k in settings.fields])
        raise typer.BadParameter(f"{key}. Config options are: \n{fields_list}\n")

    res, _, _ = set_key(config_path, key, value)
    if res:
        console.print(
            f":thumbs_up_dark_skin_tone: Set {key} to {value}", style="bold green"
        )
    else:
        console.print(
            f":thumbs_down_dark_skin_tone: Could not set {key} to {value}",
            style="bold red",
        )


@app.command()
def reset():
    """
    Reset the configuration to default.
    """

    if Confirm.ask("\n:bomb: Are you sure you want to reset the config file?"):
        reset_config()
        console.print(
            Panel.fit(
                f":thumbs_up_dark_skin_tone: Successfully reset the config file: {config_path} :thumbs_up_dark_skin_tone:"
            ),
            style="bold green",
        )
