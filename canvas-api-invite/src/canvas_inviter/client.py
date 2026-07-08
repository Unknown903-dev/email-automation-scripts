from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable
#build safe urls for the Canvas API
from urllib.parse import urljoin

#send http requests to the Canvas API
import requests


class CanvasAPIError(RuntimeError):
    """Raised when Canvas returns an unsuccessful response."""

@dataclass(frozen=True)
class CanvasClient:
    base_url: str
    token: str
    timeout_seconds: int = 30

    #if the base_url is incorrect or the token is missing, raise a ValueError
    def __post_init__(self) -> None:
        if not self.base_url.startswith(("http://", "https://")):
            raise ValueError("CANVAS_BASE_URL must start with http:// or https://")
        if not self.token or self.token == "replace_me":
            raise ValueError("CANVAS_TOKEN is missing. Put it in .env or your environment.")

    # base url for canvas api calls
    @property
    def api_base(self) -> str:
        return self.base_url.rstrip("/") + "/api/v1/"

    # every request needs token in the header, so we define a property to return the headers
    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

    # bulds the url
    def _url(self, path: str) -> str:
        return urljoin(self.api_base, path.lstrip("/"))

    # used for normal requests and prints CanvasAPIError if the response is not ok
    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        response = requests.request(
            method=method,
            url=self._url(path),
            headers=self.headers,
            timeout=self.timeout_seconds,
            **kwargs,
        )
        if not response.ok:
            raise CanvasAPIError(
                f"Canvas API error {response.status_code} for {method} {path}: {response.text[:500]}"
            )
        if response.status_code == 204 or not response.text:
            return None
        return response.json()

    # handles canvas endpoints that reurn muiltiple pages and prints CanvasAPIError if the response is not ok
    def get_paginated(self, path: str, params: dict[str, Any] | None = None) -> list[Any]:
        url = self._url(path)
        all_items: list[Any] = []
        query = params.copy() if params else {}

        while url:
            response = requests.get(
                url=url,
                headers=self.headers,
                params=query,
                timeout=self.timeout_seconds,
            )
            if not response.ok:
                raise CanvasAPIError(
                    f"Canvas API error {response.status_code} for GET {url}: {response.text[:500]}"
                )

            page = response.json()
            if not isinstance(page, list):
                raise CanvasAPIError(f"Expected a list response from {url}, got {type(page).__name__}")
            all_items.extend(page)

            url = _next_link(response.headers.get("Link", ""))
            # the next URL already includes query params
            query = None

        return all_items

    #returns the list of courses your token can see
    def list_courses(self) -> list[dict[str, Any]]:
        return self.get_paginated("courses", params={"per_page": 100})