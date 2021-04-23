from typing import Dict, List, Optional

from pydantic import BaseModel, ValidationError, conint, validator

from .enums import AuthTypeEnum, LocaleEnum


class GroupConfig(BaseModel):
    """Configuration parameters for a group"""

    min: Optional[int]
    max: Optional[int]
    underscore_space: Optional[bool]

    class Config:
        extra = "forbid"


class GroupSettings(BaseModel):
    """GroupSettings for provided TOML file"""

    names: List[str]
    config: Optional[Dict[str, GroupConfig]]

    class Config:
        extra = "forbid"

    @validator("config")
    def validate_groups(cls, value: dict, values):
        corrected_dict = {
            k.replace("_", " ") if v.underscore_space else k: v
            for k, v in value.items()
        }

        if not all((failed := name) in values["names"] for name in corrected_dict):
            raise ValueError(f"Configured group {failed} is not in the groups list!")
        return corrected_dict


class AZDSettings(BaseModel):
    """Settings model generated from provided TOML file"""

    tenant: str
    locale: LocaleEnum
    authtype: AuthTypeEnum
    block_login: bool
    num_users: conint(le=50000)
    force_password_change: bool
    groups: GroupSettings

    class Config:
        extra = "forbid"