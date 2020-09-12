import ast
import warnings
from pathlib import Path

from source.metadata import SemanticMetadata


def collect_semantic(root: Path) -> SemanticMetadata:
    sources = []
    total_lines = 0
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        for possible_source in root.glob("**/*.py"):
            if not possible_source.is_file():
                continue
            try:
                with open(possible_source) as f:
                    source = f.read()
                ast.parse(source)
            except (SyntaxError, UnicodeDecodeError):
                continue
            else:
                total_lines += source.count("\n")
                sources.append(possible_source)

    return SemanticMetadata(
        total_lines=total_lines, source_files=tuple(sources)
    )


if __name__ == "__main__":
    from argparse import ArgumentParser
    from concurrent.futures import ProcessPoolExecutor

    parser = ArgumentParser()
    parser.add_argument("paths", type=Path, nargs="+")
    options = parser.parse_args()

    with ProcessPoolExecutor(max_workers=12) as pool:
        for collection in pool.map(collect_semantic, options.paths):
            print(
                "Total lines: ",
                collection.total_lines,
                "Total files:",
                len(collection.source_files),
            )
