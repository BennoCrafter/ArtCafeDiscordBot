from dataclasses import dataclass

@dataclass
class ChannelsConfig:
    counting: int
    welcome: int
    bump: int
    event_info: int
    ticket_setup: int
    tickets_category: int
    rules: int
