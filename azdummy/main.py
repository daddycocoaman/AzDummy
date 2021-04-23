import shutil
from pathlib import Path
from rich.prompt import Confirm
import rtoml
import typer

from . import console
from .core.typer import AZDTyper
from .settings import AZDSettings
from .generators.csv import CSVGenerator
from .core.styles import AZURE_BOLD

app = AZDTyper(name="azdummy")


@app.command(help="Generate a new config template")
def new(
    file: Path = typer.Argument(
        "azd_settings.toml",
        dir_okay=False,
        file_okay=True,
        writable=True,
        resolve_path=True,
        help="Filename output",
    )
):
    if file.exists():
        if Confirm.ask(
            f":warning: [{AZURE_BOLD}]{file}[/{AZURE_BOLD}] exists. Do you want to overwrite?"
        ):
            shutil.copyfile(Path(__file__).parent / "settings.toml", file)
        else:
            exit(-1)
    else:
        shutil.copyfile(Path(__file__).parent / "settings.toml", file)

    console.print(f":white_heavy_check_mark:[{AZURE_BOLD}] {file} created!")


@app.command(help="Generate fake data for CSV upload")
def csv(
    config_file: Path = typer.Argument(
        ..., exists=True, dir_okay=False, resolve_path=True, help="Configuration file"
    ),
    output_dir: Path = typer.Option(
        ".",
        "-o",
        "--output-dir",
        dir_okay=True,
        file_okay=False,
        exists=True,
        writable=True,
        help="Filename prefix for output",
    ),
    file_prefix: str = typer.Option(
        "azdummy_output",
        "-f",
        "--file-prefix",
        help="Filename prefix for output",
    ),
):
    config = rtoml.load(config_file)
    settings = AZDSettings.parse_obj(config)
    generator = CSVGenerator(settings, output_dir, file_prefix)
    generator.write()


if __name__ == "__main__":
    app()
