from functools import partial
from dataclasses import dataclass, asdict

# TODO - can't append dict to dataclass ....


def customdataclass(cls=None, /, *, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False):
    def wrap(cls):

        # class Temp(cls):
        #     def __init__(self, *args, **kwargs) -> None:
        #         super().__init__(*args, **kwargs)

        #     def dict(self):
        #         return asdict(self)

        # def dict(cls): 
        #     kw = {k:v for k,v in vars(cls).items() if not k.startswith("__") and k != "dict"}
        #     print(kw)
        #     return asdict(cls(**kw))

        # cls.dict = partial(dict, cls)

        return dataclass(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen)
    
    if cls is None:
        return wrap # pragma no cover

    return wrap(cls)