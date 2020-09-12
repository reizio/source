from __future__ import annotations

import builtins
import contextlib
from concurrent.futures import ProcessPoolExecutor
from typing import TYPE_CHECKING, Protocol, Tuple

if TYPE_CHECKING:
    from source.order import Order


class BaseProtocol:
    def __init__(self, path: Path, workers: int = 1) -> None:
        self.path = path
        if not self.path.exists():
            self.path.mkdir(parents=True)
        self.workers = workers

    @contextlib.contextmanager
    def get_executor(self):
        if self.workers > 1:
            executor = ProcessPoolExecutor(max_workers=self.workers)
        else:
            executor = contextlib.nullcontext(builtins)

        with executor as pool:
            yield pool.map

    def execute(self, orders: Tuple[Order]) -> Tuple[Order]:
        ...
