import json
import subprocess
from pathlib import Path
from typing import Tuple, Union

from source.order import Order
from source.protocols import BaseProtocol
from source.utilities import logger


class GITProtocol(BaseProtocol):
    def execute(self, orders: Tuple[Order]) -> Tuple[Union[Exception, Path]]:
        with self.get_executor() as mapper:
            for result in mapper(self._clone, orders):
                if result is not None:
                    yield result

    def _clone(self, order: Order) -> None:
        artifact = self.path / order.metadata.owner / order.metadata.name
        if artifact.exists():
            self.update(order, artifact)
            return None

        qualname = order.metadata.qualified_name
        try:
            logger.debug("Starting cloning %s", qualname)
            subprocess.check_call(
                ["git", "clone", "--quiet", order.data, artifact]
            )
        except subprocess.CalledProcessError as exc:
            logger.exception("Couldn't clone %s/.", qualname)
            return None
        else:
            logger.debug("Successfully cloned %s", qualname)

        self.update(order, artifact)
        return artifact

    def update(self, order: Order, artifact: Path):
        if order.metadata is not None:
            with open(artifact / "SOURCE_METADATA.json", "w") as metadata_f:
                json.dump(order.metadata.as_json(), metadata_f)
