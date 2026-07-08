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

    