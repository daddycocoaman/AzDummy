from enum import Enum
from dotenv import set_key
from pydantic import BaseSettings, SecretBytes, validator


class LocaleEnum(str, Enum):
    CZECH = "cs"
    DANISH = "da"
    GERMAN = "de"
    AUSTRIAN_GERMAN = "de-at"
    SWISS_GERMAN = "de-ch"
    GREEK = "el"
    ENGLISH = "en"
    AUSTRALIAN_ENGLISH = "en-au"
    CANADIAN_ENGLISH = "en-ca"
    BRITISH_ENGLISH = "en-gb"
    SPANISH = "es"
    MEXICAN_SPANISH = "es-mx"
    ESTONIAN = "et"
    FARSI = "fa"
    FINNISH = "fi"
    FRENCH = "fr"
    HUNGARIAN = "hu"
    ICELANDIC = "is"
    ITALIAN = "it"
    JAPANESE = "ja"
    KAZAKH = "kk"
    KOREAN = "ko"
    DUTCH = "nl"
    BELGIUM_DUTCH = "nl-be"
    NORWEGIAN = "no"
    POLISH = "pl"
    PORTUGUESE = "pt"
    BRAZILIAN_PORTUGUESE = "pt-br"
    RUSSIAN = "ru"
    SLOVAK = "sk"
    SWEDISH = "sv"
    TURKISH = "tr"
    UKRAINIAN = "uk"
    CHINESE = "zh"


class AzDummySettings(BaseSettings):
    """Settings for AzDummy"""

    AZD_AUTH_MODE: str
    AZD_TENANT_FQDN: str
    AZD_LOCALE: LocaleEnum
    AZD_CLIENT_ID: str
    AZD_CLIENT_SECRET: SecretBytes
    AZD_NUM_USERS: int
    AZD_NUM_GLOBAL_ADMIN: int
    AZD_BLOCK_LOGIN: bool
    AZD_GROUP_NAMES: list

    @validator("AZD_NUM_USERS")
    def max_limit(cls, v):
        if v > 50000:
            raise ValueError("AZD_NUM_USERS needs to be 50,000 or less")
        return v

    @validator("AZD_NUM_GLOBAL_ADMIN")
    def max_global_limit(cls, v, values):
        if v > 50000:
            raise ValueError("AZD_NUM_GLOBAL_ADMIN needs to be 50,000 or less")
        elif v > values["AZD_NUM_USERS"]:
            raise ValueError(
                "AZD_NUM_GLOBAL_ADMIN number set higher than AZD_NUM_USERS"
            )

    def set_key(self):
        return self.fields