from enum import Enum


class BaseTypes(str, Enum):
    def __repr__(self):
        return f"'{self._value_}'"  # pragma: no cover
