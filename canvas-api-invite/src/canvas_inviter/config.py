from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# define a dataclass to hold the settings
# frozen=True makes the dataclass immutable, so that the settings cannot be changed after they are loaded
@dataclass(frozen=True)
class Settings:
    canvas_base_url: str
    canvas_token: str

#load the settings from the environment variables
def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        canvas_base_url=os.getenv("CANVAS_BASE_URL", "").strip(),
        canvas_token=os.getenv("CANVAS_TOKEN", "").strip(),
    )