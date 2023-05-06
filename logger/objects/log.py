from dataclasses import dataclass, asdict
import datetime


@dataclass
class Log:
    created: datetime.datetime
    level: str
    msg: str
    task_id: str = None
    task_type: str = None

    def __repr__(self) -> str:
        string = ''
        for prop, value in vars(self).items():
            string += f"{str(prop)}: {str(value)}\n"
        return string

    def convert_to_dict(self) -> dict:
        return asdict(self)
