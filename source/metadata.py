import mmap
from dataclasses import asdict, dataclass
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, Set, Tuple


@dataclass(frozen=True)
class Metadata:

    name: str
    owner: str
    popularity: int
    last_update: str

    # https://github.com/python/typing/issues/182#issuecomment-185996450

    @cached_property
    def qualified_name(self):
        return self.name + "/" + self.owner

    def as_json(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SemanticMetadata:

    total_lines: int
    source_files: Tuple[Path]
