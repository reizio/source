import json
import os
import shelve
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# For debug mode, all requests are cached
CACHE_PATH = Path("~/.local/source_cache").expanduser()
if not CACHE_PATH.exists():
    CACHE_PATH.mkdir()


def query(url, **query_args):
    """Perform a HTTP request against an endpoint
    and decode the response in JSON format"""

    url += "?"
    url += urlencode(query_args)
    return _cached(url)


def _cached(url, db_path=os.fspath(CACHE_PATH / "cache.db")):
    db = shelve.open(db_path)
    if url not in db:
        db[url] = _real_fetch(url)
        db.sync()
    return db[url]


def _real_fetch(url):
    request = Request(url)
    with urlopen(request) as page:
        return json.load(page)
