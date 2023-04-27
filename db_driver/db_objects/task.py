import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Optional

from db_driver.db_objects.timestamp import Timestamp


@dataclass
class Task:
    task_id: str
    url: str
    domain: str
    status: str
    type: str
    status_timestamp: List[Timestamp] = field(default_factory=lambda: [])
    creation_time: datetime.datetime = None
    collecting_time: datetime.datetime = None  # todo: check if needed

    def __repr__(self) -> str:
        string = ''
        for prop, value in vars(self).items():
            string += f"{str(prop)}: {str(value)}\n"
        return string

    def convert_to_dict(self) -> dict:
        return asdict(self)
