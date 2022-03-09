import enum
from dataclasses import dataclass


@dataclass
class Jump:
    begin: int
    end: int

    def __repr__(self):
        return f"[{self.begin}:{self.end}]"
