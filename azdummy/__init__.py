import shutil
from pathlib import Path

import typer
from dotenv import load_dotenv
from rich import pretty, traceback
from rich.console import Console
from rich.prompt import Confirm

from .settings import AzDummySettings

APP_NAME = "azdummy"

state = {"verbose": False, "timeStart": None, "resetConfig": True}

console = Console()
traceback.install(show_locals=True)
pretty.install()

app_dir = typer.get_app_dir(APP_NAME)
config_path = Path(app_dir) / "settings.env"


def reset_config():
    """Reset the configuration to default"""
    try:
        Path(app_dir).mkdir(parents=True, exist_ok=True)
        shutil.copy(Path(__file__).parent / "settings.env", config_path)
    except:
        console.print_exception()


if not config_path.exists():
    if Confirm.ask(
        "\n:grimacing face: :thumbs_down_dark_skin_tone: Looks like your first time running azdummy. Would you like initialize a new config?"
    ):
        reset_config()

load_dotenv(config_path, verbose=True)
settings = AzDummySettings(config_path)
