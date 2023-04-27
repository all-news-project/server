import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Timestamp:
    status: str
    start_time: datetime.datetime
    end_time: datetime.datetime

    def __repr__(self) -> str:
        string = ''
        for prop, value in vars(self).items():
            string += f"{str(prop)}: {str(value)}\n"
        return string

    def convert_to_dict(self) -> dict:
        return asdict(self)
