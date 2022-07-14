from enum import Enum



class BaseTypes(str, Enum):

    def __repr__(self):
        return self._value_
