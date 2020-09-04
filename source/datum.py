from dataclasses import dataclass
from enum import Enum, auto


class Qualifier(Enum):
    FRESH = auto()
    POPULARITY = auto()


@dataclass(frozen=True)
class Shard:
    """A data shard for specifying the query
    parameters to the provider"""

    position: slice
    qualifier: Qualifier

    def __post_init__(self):
        if self.position.step is not None:
            raise ValueError("Shard objects don't support stepping on slices")
