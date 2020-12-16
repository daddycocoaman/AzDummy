import time
from pathlib import Path

import typer
from rich.panel import Panel

from azdummy import console, state
from azdummy.commands import config, gen
from azdummy.core.typer import AZDTyper

app = AZDTyper(name="azdummy")
app.add_typer(config.app, name="config", help="Show or edit configuration data")
app.add_typer(gen.app, name="gen", help="Generate fake data for specified type")


def command_finish(*args, **kwargs):
    if state["timeStart"]:
        elapsedTime = time.time() - state["timeStart"]
        console.print(
            Panel.fit(f":stopwatch:  Execution time: [bold yellow]{elapsedTime}"),
            style="bold green",
        )


@app.callback(result_callback=command_finish)
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    timer: bool = typer.Option(
        False, "--timer", help="Print execution time after output"
    ),
):
    if verbose:
        state["verbose"] = True
    if timer:
        state["timeStart"] = time.time()
    print()


if __name__ == "__main__":
    app()
