import datetime
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class StatusTimestamp:
    status: str
    time_changed: datetime.datetime
    desc: Optional[str] = None

    def __repr__(self) -> str:
        string = ''
        for prop, value in vars(self).items():
            string += f"{str(prop)}: {str(value)}\n"
        return string

    def convert_to_dict(self) -> dict:
        return asdict(self)
