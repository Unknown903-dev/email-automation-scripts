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

    # list the users in the chosen course
    #by defaul only list students
    def list_course_users(
        self,
        course_id: int | str,
        enrollment_type: str = "student",
        include_uuid: bool = True,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {
            "per_page": 100,
            "enrollment_type[]": enrollment_type,
            "enrollment_state[]": "active",
        }
        if include_uuid:
            params["include[]"] = "uuid"
        return self.get_paginated(f"courses/{course_id}/users", params=params)

    # creates a new conversation with the given recipients, subject, and body
    def create_conversation(
        self,
        recipients: Iterable[int | str],
        subject: str,
        body: str,
        course_id: int | str | None = None,
        group_conversation: bool = False,
        force_new: bool = True,
        mode: str = "sync",
    ) -> Any:
        recipient_list = [str(r) for r in recipients]
        if not recipient_list:
            raise ValueError("No recipients provided")

        payload: dict[str, Any] = {
            "recipients[]": recipient_list,
            "subject": subject,
            "body": body,
            "group_conversation": str(group_conversation).lower(),
            "force_new": str(force_new).lower(),
            "mode": mode,
        }
        if course_id is not None:
            payload["context_code"] = f"course_{course_id}"

        return self.request("POST", "conversations", data=payload)

# reads the canvas link header and returns the next link if it exists, otherwise returns None
def _next_link(link_header: str) -> str | None:
    if not link_header:
        return None
    for part in link_header.split(","):
        section = part.strip().split(";")
        if len(section) < 2:
            continue
        url_part = section[0].strip()
        rel_parts = [s.strip() for s in section[1:]]
        if 'rel="next"' in rel_parts:
            return url_part.strip("<>")
    return None
