from typing import Protocol, Tuple

from source.datum import Qualifier, Shard
from source.order import Order


class BaseProvider(Protocol):
    SUPPORTED_QUALIFIERS: Tuple[Qualifier] = ()

    def provide(self, shard: Shard) -> Tuple[Order]:
        ...


class InsufficientResults(ValueError):
    ...
