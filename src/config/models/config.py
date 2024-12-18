from dataclasses import dataclass
from src.config.models.channels_config import ChannelsConfig


@dataclass
class Config:
    channels: ChannelsConfig
