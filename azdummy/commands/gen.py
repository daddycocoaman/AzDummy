import csv
from dataclasses import fields
from enum import Enum

import typer
from rich.panel import Panel
from rich.progress import track
from rich.table import Table

from azdummy import console, settings, state

from azdummy.provider import generic

app = typer.Typer()


class OutputFormat(str, Enum):
    CONSOLE = "console"
    CSV = "csv"


@app.command()
def users(
    tenant: str = typer.Option(settings.AZD_TENANT_FQDN, help="Tenant name"),
    count: int = typer.Option(
        settings.AZD_NUM_USERS,
        metavar=None,
        max=50000,
        help="Number of users to generate. Max 50000.",
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.CSV,
        show_choices=True,
        case_sensitive=False,
        help="Format for output.",
    ),
    block_login: bool = typer.Option(
        settings.AZD_BLOCK_LOGIN,
        "--block-login",
        "-b",
        help="Prevent generated users from logging in",
    ),
    output_file: typer.FileTextWrite = typer.Option(
        "output", help="File to output. Extension not required."
    ),
):
    """
    Generate fake user data.

    The output format determines which fields are generated. CSV format
    will output two CSVs: one for bulk create and one for bulk delete.

    Console output generates the users and outputs them to the console. Does
    not create the CSV files.
    """
    if format.value in [OutputFormat.CONSOLE, OutputFormat.CSV]:
        users = generic.AzureADProvider.AzUsers(tenant, count, block_login)

        if format.value == OutputFormat.CONSOLE:
            table = Table(title=" ", header_style="bold green")
            cols = [c.name for c in filter(lambda x: x.repr == True, fields(users[0]))]
            for col in cols:
                table.add_column(col, no_wrap=False)

            for user in track(users, description="Generating table..."):
                values = []
                for col in cols:
                    values.append(user.__dict__.get(col))
                table.add_row(*values)

            with console.status(
                f"[bold green] Generating output for {count} users. Please be patient for large datasets.\n",
                spinner="runner",
            ) as status:
                console.print(table)
        elif format.value == OutputFormat.CSV:

            user_headers = [
                "User name [userPrincipalName] *",
                "Name [displayName] *",
                "Initial password [passwordProfile] *",
                "Block sign in (Yes/No) [accountEnabled] *",
                "First name [givenName]",
                "Last name [surname]",
                "Job title [jobTitle]",
                "Department [department]",
                "Usage location [usageLocation]",
                "Street address [streetAddress]",
                "State or province [state]",
                "Country or region [country]",
                "Office [physicalDeliveryOfficeName]",
                "City [city]",
                "ZIP or postal code [postalCode]",
                "Office phone [telephoneNumber]",
                "Mobile phone [mobile]",
            ]
            with console.status(
                f"[bold green]Generating bulk upload and delete files. Please be patient for large datasets.\n",
                spinner="hamburger",
            ) as status:
                with open(
                    f"{output_file.name}_create.csv", "w", newline="", encoding="utf-8"
                ) as createfile:
                    with open(
                        f"{output_file.name}_delete.csv",
                        "w",
                        newline="",
                        encoding="utf-8",
                    ) as deletefile:
                        createwriter = csv.writer(createfile)
                        createwriter.writerow(
                            ["version:v1.0"] + [""] * len(user_headers)
                        )
                        createwriter.writerow(user_headers)

                        deletewriter = csv.writer(deletefile)
                        deletewriter.writerow(["version:v1.0"])
                        deletewriter.writerow(
                            ["User name [userPrincipalName] Required"]
                        )

                        for user in users:
                            createwriter.writerow(user.to_list())
                            deletewriter.writerow([user.userPrincipalName])

                    console.print(
                        Panel.fit(
                            f":white_heavy_check_mark: Generated {count} users. Output files: [bold yellow] {createfile.name}, {deletefile.name}",
                            style="bold green",
                        )
                    )
