from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Metadata:

    name: str
    owner: str
    popularity: int
    last_update: str

    # https://github.com/python/typing/issues/182#issuecomment-185996450

    def as_json(self) -> Dict[str, Any]:
        return asdict(self)
