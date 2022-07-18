from dataclasses import dataclass


@dataclass
class ParamType:
    name:str
    type:str
    required: bool
    description: str

