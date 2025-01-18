from dataclasses import dataclass
from typing import Optional, List, Any, Union

@dataclass
class Channels:
    counting: int
    welcome: int
    bump: int
    event_info: int
    ticket_setup: int
    tickets_category: int
    rules: int