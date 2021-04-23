import random
from typing import List

from mimesis.schema import Field, Schema
from mimesis.typing import JSON
from rich.progress import (BarColumn, Progress, SpinnerColumn, TextColumn,
                           TimeElapsedColumn)

from .. import console
from ..core.styles import *
from ..settings import AZDSettings


class Users:
    def __init__(self, settings: AZDSettings) -> None:
        _ = Field(settings.locale)
        self.settings = settings
        self.base_description = lambda: {
            "name": _("full_name"),
            "password": _("person.password", length=20),
            "department": random.choice(settings.groups.names),
            "address": f"{_('address.street_number')} {_('address.street_name')} {_('address.street_suffix')}",
            "state": _("address.state", abbr=True),
            "city": _("address.city"),
            "postalCode": _("address.postal_code"),
            "usageLocation": _("address.country"),
            "country": _("address.country"),
            "telephoneNumber": _("person.telephone", mask="###-###-####"),
            "mobile": _("person.telephone", mask="###-###-####"),
            "blockSignIn": "Yes" if settings.block_login else "No",
        }

    def run(self) -> List[JSON]:
        """Generate the users"""
        schema = Schema(self.base_description)
        users = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(style=WHITE, finished_style=AZURE_BOLD),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:

            generate_task = progress.add_task(
                f"[{AZURE_BOLD}]Generating user data",
                total=self.settings.num_users,
            )

            while not progress.finished:
                # GENERATE TASK STARTS HERE
                for _ in range(self.settings.num_users):
                    users.extend(schema.create())
                    progress.update(generate_task, advance=1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(style=WHITE, finished_style=AZURE_BOLD),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:

            validate_task = progress.add_task(
                f"[{AZURE_BOLD}]Deduplicating users ",
                total=self.settings.num_users,
            )

            while not progress.finished:
                # VALIDATE TASK STARTS HERE
                valid_users = []
                existing_names = []
                progress.start_task(validate_task)
                while users:
                    user = users.pop()

                    # Verify unique names
                    while user["name"] in existing_names:
                        user = schema.create(1)[0]

                    # Fill in other required fields based on generated name
                    user["givenName"], user["surname"] = user["name"].split()
                    upn = (
                        f"{user['givenName']}.{user['surname']}@{self.settings.tenant}"
                    )
                    user["userPrincipalName"] = upn
                    existing_names.append(user["name"])

                    valid_users.append(user)
                    progress.update(
                        validate_task, total=self.settings.num_users, advance=1
                    )
                return valid_users
