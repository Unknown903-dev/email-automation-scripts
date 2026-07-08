from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MATCH_COLUMNS = ("id", "name", "sortable_name", "login_id", "email")

# reads your message template from a text file and returns it as a string
def read_text_file(path: str | Path) -> str:
    text = Path(path).read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Message file is empty: {path}")
    return text

# renders a message template with user data, replacing placeholders with actual values
def render_template(template: str, user: dict[str, Any]) -> str:
    body = template
    replacements = {
        "id": str(user.get("id", "")),
        "name": str(user.get("name", "")),
        "sortable_name": str(user.get("sortable_name", "")),
        "login_id": str(user.get("login_id", "")),
        "email": str(user.get("email", "")),
    }
    for key, value in replacements.items():
        body = body.replace("{{" + key + "}}", value)
    return body

# reads a CSV file containing filter values and returns a set of those values
def read_filter_values(csv_path: str | Path | None) -> set[str]:
    if not csv_path:
        return set()

    path = Path(csv_path)
    values: set[str] = set()
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        # Allow comments and blank lines in simple CSV files.
        lines = [line for line in f if line.strip() and not line.lstrip().startswith("#")]
    if not lines:
        return values

    reader = csv.DictReader(lines)
    if not reader.fieldnames:
        return values

    # check that the CSV file has at least one of the expected columns
    usable_columns = [c for c in reader.fieldnames if c in MATCH_COLUMNS]
    if not usable_columns:
        raise ValueError(
            f"{csv_path} must contain at least one of these columns: {', '.join(MATCH_COLUMNS)}"
        )
    # read the values from the CSV file and add them to the set
    for row in reader:
        for column in usable_columns:
            value = (row.get(column) or "").strip().lower()
            if value:
                values.add(value)
    return values

# keeps only users who match the csv if no csv return all users
def filter_users(users: list[dict[str, Any]], filter_values: set[str]) -> list[dict[str, Any]]:
    if not filter_values:
        return users

    kept: list[dict[str, Any]] = []
    for user in users:
        candidates = {str(user.get(col, "")).strip().lower() for col in MATCH_COLUMNS}
        if candidates & filter_values:
            kept.append(user)
    return kept

# prevent accidental duplicate messages by keeping track of which users have already been sent a message
def load_sent_ids(log_path: str | Path) -> set[str]:
    path = Path(log_path)
    if not path.exists():
        return set()

    sent: set[str] = set()
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = (row.get("user_id") or "").strip()
            if user_id:
                sent.add(user_id)
    return sent

# removes users already in the sent log
def remove_already_sent(users: list[dict[str, Any]], sent_ids: set[str]) -> list[dict[str, Any]]:
    return [u for u in users if str(u.get("id", "")) not in sent_ids]

# after message is sent log them
def append_sent_log(
    log_path: str | Path,
    users: list[dict[str, Any]],
    course_id: int | str,
    subject: str,
) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()

    with path.open("a", encoding="utf-8", newline="") as f:
        fieldnames = ["sent_at", "course_id", "user_id", "name", "login_id", "email", "subject"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if new_file:
            writer.writeheader()
        sent_at = datetime.now(timezone.utc).isoformat()
        for user in users:
            writer.writerow(
                {
                    "sent_at": sent_at,
                    "course_id": course_id,
                    "user_id": user.get("id", ""),
                    "name": user.get("name", ""),
                    "login_id": user.get("login_id", ""),
                    "email": user.get("email", ""),
                    "subject": subject,
                }
            )

# split a list of items into chunks of a specified size
def chunks(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    if size < 1:
        raise ValueError("Batch size must be at least 1")
    return [items[i : i + size] for i in range(0, len(items), size)]
