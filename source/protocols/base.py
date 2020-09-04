from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Tuple

if TYPE_CHECKING:
    from source.order import Order


class BaseProtocol(Protocol):
    def execute(self, orders: Tuple[Order]) -> None:
        ...
