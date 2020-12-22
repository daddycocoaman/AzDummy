import random
from dataclasses import asdict, dataclass, field, fields
from typing import List

from mimesis import Address, Generic, Person
from mimesis.providers.base import BaseProvider
from rich.progress import track
from rich import markup
from azdummy import settings
from azdummy.styles import AZURE_BOLD

person = Person("en")
address = Address(settings.AZD_LOCALE)
generic = Generic(settings.AZD_LOCALE)


@dataclass
class AzUser:
    """Dataclass for creating an AzUser object"""

    domain: str = field(repr=False, hash=False)
    userPrincipalName: str = field(init=False)
    name: str = field(init=False)
    passwordProfile: str = field(init=False)
    blockSignIn: bool = False
    givenName: str = field(init=False)
    surname: str = field(init=False)
    jobTitle: str = "Employee"
    department: str = field(init=False)
    usageLocation: str = field(init=False)
    streetAddress: str = field(init=False)
    state: str = field(init=False)
    country: str = field(init=False)
    physicalDeliveryOfficeName: str = None
    city: str = field(init=False)
    postalCode: str = field(init=False)
    telephoneNumber: str = field(init=False)
    mobile: str = field(init=False)

    def __post_init__(self):
        self.name = person.full_name()
        while "'" in self.name:
            self.name = person.full_name()

        self.givenName, self.surname = self.name.split()
        self.userPrincipalName = f"{self.givenName}.{self.surname}@{self.domain}"
        self.passwordProfile = markup.escape(person.password(length=20))
        self.department = random.choice(settings.AZD_GROUP_NAMES)
        self.streetAddress = f"{address.street_number()} {address.street_name()} {address.street_suffix()}"
        self.state = address.state(True)
        self.city = address.city()
        self.postalCode = address.postal_code()
        self.usageLocation = address.country()
        self.country = address.country()
        self.telephoneNumber = person.telephone("###-###-####")
        self.mobile = person.telephone("###-###-####")
        self.blockSignIn = "Yes" if self.blockSignIn else "No"

    def to_list(self) -> list:
        """Returns the AzUser object fields as a list"""
        return [
            v
            for k, v in asdict(self).items()
            if k
            not in [a.name for a in filter(lambda x: x.repr == False, fields(self))]
        ]


class AzureADProvider(BaseProvider):
    class Meta:
        name = "AzureADProvider"

    @staticmethod
    def AzUsers(domain: str, number: int, block_login: bool) -> List[AzUser]:
        """Returns a list of AzUsers"""

        users = []
        existingNames = set()
        for _ in track(range(number), description=f"[{AZURE_BOLD}]Generating users..."):
            while True:
                user = AzUser(domain, blockSignIn=block_login)
                if user.name not in existingNames:
                    users.append(user)
                    existingNames.add(user.name)
                    break
        return users


generic.add_provider(AzureADProvider)
