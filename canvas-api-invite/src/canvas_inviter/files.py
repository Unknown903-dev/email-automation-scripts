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