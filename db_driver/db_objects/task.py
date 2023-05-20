import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Union

from db_driver.db_objects.status_timestamp import StatusTimestamp


@dataclass
class Task:
    task_id: str
    url: str
    domain: str
    status: str
    type: str
    status_timestamp: List[Union[StatusTimestamp, dict]] = field(default_factory=lambda: [])
    creation_time: datetime.datetime = None
    def __repr__(self) -> str:
        string = ''
        for prop, value in vars(self).items():
            string += f"{str(prop)}: {str(value)}\n"
        return string

    def convert_to_dict(self) -> dict:
        return asdict(self)
