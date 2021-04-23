import csv
from pathlib import Path

from rich.panel import Panel

from .models import Users
from .. import console
from ..settings import AZDSettings
from ..core.styles import *


class CSVGenerator:
    def __init__(
        self, settings: AZDSettings, output_dir: Path, file_prefix: str
    ) -> None:
        self.output_dir = output_dir
        self.file_prefix = file_prefix
        self._path_base = str(output_dir / file_prefix)
        self.settings = settings
        self.user_headers = [
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
        self.users = Users(settings).run()

    def write(self):
        count = len(self.users)
        groups = {group: [] for group in self.settings.groups.names}

        with open(
            f"{self._path_base}_create.csv", "w", newline="", encoding="utf-8"
        ) as createfile:
            with open(
                f"{self._path_base}_delete.csv",
                "w",
                newline="",
                encoding="utf-8",
            ) as deletefile:
                createwriter = csv.writer(createfile)
                createwriter.writerow(["version:v1.0"] + [""] * len(self.user_headers))
                createwriter.writerow(self.user_headers)

                deletewriter = csv.writer(deletefile)
                deletewriter.writerow(["version:v1.0"])
                deletewriter.writerow(["User name [userPrincipalName] Required"])

                for user in self.users:
                    try:
                        row = [
                            user["userPrincipalName"],
                            user["name"],
                            user["password"],
                            user["blockSignIn"],
                            "Yes",
                            user["givenName"],
                            user["surname"],
                            "Employee",
                            user["department"],
                            user["usageLocation"],
                            user["address"],
                            user["state"],
                            user["country"],
                            "",
                            user["city"],
                            user["postalCode"],
                            user["telephoneNumber"],
                            user["mobile"],
                        ]
                    except:
                        print(user)
                        exit()
                    createwriter.writerow(row)
                    deletewriter.writerow([user["userPrincipalName"]])

                    groups[user["department"]].append(user["userPrincipalName"])

            console.print(
                Panel.fit(
                    f"Generated {count} users. Output files: [white] \n{createfile.name}\n{deletefile.name}",
                    style=AZURE_BOLD,
                )
            )

        for group, members in groups.items():
            if members:
                with open(
                    f"{self._path_base}_{group.replace(' ', '_')}.csv",
                    "w",
                    newline="",
                    encoding="utf-8",
                ) as groupfile:
                    groupwriter = csv.writer(groupfile)
                    groupwriter.writerow(["version:v1.0"])
                    groupwriter.writerow(
                        [
                            "Member object ID or user principal name [memberObjectIdOrUpn] Required"
                        ]
                    )
                    groupwriter.writerows([[member] for member in members])

        group_filelist = "\n".join(
            [f"{self._path_base}_{group.replace(' ', '_')}.csv" for group in groups]
        )
        console.print(
            Panel.fit(
                f"Generated group files. Output files:[white] \n{group_filelist}",
                style=AZURE_BOLD,
            )
        )