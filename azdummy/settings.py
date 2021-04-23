from pydantic import BaseModel, BaseSettings, conint

from .enums import AuthTypeEnum, LocaleEnum


class GroupSettings(BaseModel):
    """GroupSettings for provided configuration"""

    names: list


class AZDSettings(BaseModel):
    """BaseSettings for provided configuration"""

    tenant: str
    locale: LocaleEnum
    authtype: AuthTypeEnum
    block_login: bool
    num_users: conint(le=50000)
    groups: GroupSettings
    force_password_change: bool