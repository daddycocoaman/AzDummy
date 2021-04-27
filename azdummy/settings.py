from typing import Dict, List, Optional

from pydantic import BaseModel, conint, validator, Field

from .enums import AuthTypeEnum, LocaleEnum


class StrictModel(BaseModel):
    class Config:
        extra = "forbid"


class GroupConfig(StrictModel):
    """Configuration parameters for a group"""

    max: Optional[int] = Field(description="Maximum amount of users for group")
    underscore_space: Optional[bool] = Field(
        description="Underscore in group name in config should be interpreted as a space"
    )


class GroupSettings(StrictModel):
    """GroupSettings for provided TOML file"""

    names: List[str]
    config: Optional[Dict[str, GroupConfig]]

    @validator("config")
    def validate_groups(cls, value: dict, values):
        corrected_dict = {
            k.replace("_", " ") if v.underscore_space else k: v
            for k, v in value.items()
        }

        if not all((failed := name) in values["names"] for name in corrected_dict):
            raise ValueError(f"Configured group {failed} is not in the groups list!")
        return corrected_dict


class AZDSettings(StrictModel):
    """Settings model generated from provided TOML file"""

    tenant: str
    locale: LocaleEnum
    authtype: AuthTypeEnum
    block_login: bool
    num_users: conint(le=50000)
    force_password_change: bool
    groups: GroupSettings
