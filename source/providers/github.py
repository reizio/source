import math
from typing import Any, Dict, Iterator, List, Tuple

from source.datum import Qualifier, Shard
from source.metadata import Metadata
from source.order import Order
from source.protocols.git import GITProtocol
from source.providers import BaseProvider, InsufficientResults
from source.providers.utilities import query

BASE = "https://api.github.com"
PAGE_LIMIT = 100
DEFAULT_QUERY_ARGS = {"order": "desc", "q": "language:python"}


class GithubSourceProvider(BaseProvider):

    SUPPORTED_QUALIFIERS = (Qualifier.FRESH, Qualifier.POPULARITY)

    def provide(self, shard: Shard) -> Tuple[Order]:
        url = BASE + "/search/repositories"
        sort = self._determine_sorting(shard.qualifier)
        start, end = self._calculate_pagination(shard.position)

        orders = []
        for page in range(start, end + 1):
            data = query(
                url,
                page=page,
                sort=sort,
                per_page=PAGE_LIMIT,
                **DEFAULT_QUERY_ARGS,
            )

            if len(data["items"]) != PAGE_LIMIT:
                raise InsufficientResults

            orders.extend(self.generate_orders(data["items"]))

        return tuple(orders)

    def generate_orders(
        self, dataset: List[Dict[str, Any]]
    ) -> Iterator[Order]:
        for entry in dataset:
            name = entry["name"]
            owner = entry["owner"]["login"]
            last_update = entry["updated_at"]
            estimated_popularity = self._calculate_popularity(
                entry["forks_count"],
                entry["watchers_count"],
                entry["stargazers_count"],
                entry["open_issues_count"],
            )

            # FIXME: Currently the 'data' (clone url) calculated by using
            # the presented html_url and adding a `.git` extension at the
            # end. But the problem is, it is not the best and the most
            # reliable way. Solution is making an extra request and
            # obtaining clone_url from the API.

            data = entry["html_url"] + ".git"
            metadata = Metadata(
                name=name,
                owner=owner,
                popularity=estimated_popularity,
                last_update=last_update,
            )
            yield Order(
                data=data,
                metadata=metadata,
                protocol=GITProtocol,
            )

    def _determine_sorting(self, qualifier: Qualifier) -> str:
        if qualifier is Qualifier.FRESH:
            return "updated"
        elif qualifier is Qualifier.POPULARITY:
            return "stars"

    def _calculate_pagination(self, position: slice) -> Tuple[int, int]:
        end_page = math.floor(position.stop // 100)
        start_page = math.ceil(position.start // 100)
        return start_page, end_page

    def _calculate_popularity(
        self, forks: int, watchers: int, stars: int, issues: int
    ) -> int:
        "estimate(f, w, s, i) => s + f * 3 + i * 5 + w * 7"
        return stars + forks * 3 + issues * 5 + watchers * 7
