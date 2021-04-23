from rich import pretty, traceback
from rich.console import Console

console = Console()
traceback.install(show_locals=True)
pretty.install()
