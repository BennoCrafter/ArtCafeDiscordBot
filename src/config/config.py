from dataclasses import dataclass
from src.config.channels import Channels
from src.config.roles import Roles
from typing import Optional, List, Any, Union

@dataclass
class Config:
    channels: Channels
    roles: Roles
    language: str