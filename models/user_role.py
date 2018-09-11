import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()
    admin = auto()


class QinEncoder(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            return {self.prefix: o.name}
        else:
            return super().default(o)


def qin_decode(d):
    if QinEncoder.prefix in d:
        name = d[QinEncoder.prefix]
        return UserRole[name]
    else:
        return d
