from dataclasses import dataclass
from typing import Optional, List, Any, Union

@dataclass
class Roles:
    staff: int
    member: int
    bump: int