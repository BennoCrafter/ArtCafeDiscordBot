from dataclasses import dataclass


@dataclass
class RolesConfig:
    staff: int
    member: int
