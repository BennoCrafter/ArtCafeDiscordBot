from dataclasses import dataclass
from src.config.models.channels_config import ChannelsConfig
from src.config.models.roles_config import RolesConfig

@dataclass
class Config:
    channels: ChannelsConfig
    roles: RolesConfig
    language: str
