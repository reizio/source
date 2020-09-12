# Source
Multi-platform, multi-protocol source code tracking system

```
from pathlib import Path
from source.providers.github import GithubSourceProvider
from source.protocols.git import GITProtocol
from source.datum import Shard, Qualifier

DATA_PATH = Path("rawdata/")

def fetch(start, end):
    shard = Shard(
        slice(start, end),
        Qualifier.POPULARITY
    )
    provider = GithubSourceProvider()
    return provider.provide(shard)

def download(protocol, orders):
    for item in protocol.execute(orders):
        print(item)

repos = fetch(0, 300)
protocol = GITProtocol(DATA_PATH, workers=25)
download(protocol, repos)
```
