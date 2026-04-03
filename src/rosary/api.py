"""Async client for bible-api.com."""

from __future__ import annotations

import httpx

BASE_URL = "https://bible-api.com"

# Translations available on bible-api.com (identifier → display name).
# This is fetched live; this list is kept as a static fallback.
_FALLBACK_TRANSLATIONS: list[dict] = [
    {"identifier": "web", "name": "World English Bible", "language": "English"},
    {"identifier": "kjv", "name": "King James Version", "language": "English"},
    {
        "identifier": "asv",
        "name": "American Standard Version (1901)",
        "language": "English",
    },
    {"identifier": "bbe", "name": "Bible in Basic English", "language": "English"},
    {"identifier": "darby", "name": "Darby Bible", "language": "English"},
    {
        "identifier": "dra",
        "name": "Douay-Rheims 1899 American Edition",
        "language": "English",
    },
    {"identifier": "ylt", "name": "Young's Literal Translation", "language": "English"},
    {
        "identifier": "oeb-cw",
        "name": "Open English Bible, Commonwealth Edition",
        "language": "English (UK)",
    },
    {
        "identifier": "oeb-us",
        "name": "Open English Bible, US Edition",
        "language": "English (US)",
    },
    {
        "identifier": "webbe",
        "name": "World English Bible, British Edition",
        "language": "English (UK)",
    },
    {
        "identifier": "clementine",
        "name": "Clementine Latin Vulgate",
        "language": "Latin",
    },
    {
        "identifier": "almeida",
        "name": "João Ferreira de Almeida",
        "language": "Portuguese",
    },
    {
        "identifier": "rccv",
        "name": "Protestant Romanian Cornilescu Version",
        "language": "Romanian",
    },
    {"identifier": "cuv", "name": "Chinese Union Version", "language": "Chinese"},
    {"identifier": "bkr", "name": "Bible kralická", "language": "Czech"},
    {
        "identifier": "cherokee",
        "name": "Cherokee New Testament",
        "language": "Cherokee",
    },
]


async def fetch_translations() -> tuple[list[dict], bool]:
    """Return (translations, api_error).

    translations: list of dicts with keys identifier, name, language.
    api_error: True if the live API could not be reached (fallback used).
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/data")
            response.raise_for_status()
            data = response.json()
            return data.get("translations", _FALLBACK_TRANSLATIONS), False
        except (httpx.HTTPError, KeyError, ValueError):
            return _FALLBACK_TRANSLATIONS, True


async def fetch_verse(ref: str, translation_id: str) -> str:
    """Fetch the text for a scripture reference.

    Returns the combined verse text, or an empty string on failure.
    """
    url = f"{BASE_URL}/{ref}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, params={"translation": translation_id})
            response.raise_for_status()
            data = response.json()
            return data.get("text", "").strip()
        except (httpx.HTTPError, KeyError, ValueError):
            return ""
