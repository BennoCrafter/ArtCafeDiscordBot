from dataclasses import dataclass

@dataclass
class ChannelsConfig:
    counting: int
    welcome: int
    bump: int