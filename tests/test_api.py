"""Tests for rosary.api."""

import httpx
import pytest
import respx

from rosary.api import (
    _FALLBACK_TRANSLATIONS,
    BASE_URL,
    fetch_translations,
    fetch_verse,
)

# ── fetch_translations ────────────────────────────────────────────────────────


@respx.mock
@pytest.mark.asyncio
async def test_fetch_translations_returns_data_on_success():
    payload = {
        "translations": [
            {"identifier": "web", "name": "World English Bible", "language": "English"}
        ]
    }
    respx.get(f"{BASE_URL}/data").mock(return_value=httpx.Response(200, json=payload))

    translations, api_error = await fetch_translations()

    assert api_error is False
    assert translations == payload["translations"]


@respx.mock
@pytest.mark.asyncio
async def test_fetch_translations_falls_back_on_http_error():
    respx.get(f"{BASE_URL}/data").mock(return_value=httpx.Response(500))

    translations, api_error = await fetch_translations()

    assert api_error is True
    assert translations == _FALLBACK_TRANSLATIONS


@respx.mock
@pytest.mark.asyncio
async def test_fetch_translations_falls_back_on_network_error():
    respx.get(f"{BASE_URL}/data").mock(side_effect=httpx.ConnectError("timeout"))

    translations, api_error = await fetch_translations()

    assert api_error is True
    assert translations == _FALLBACK_TRANSLATIONS


@respx.mock
@pytest.mark.asyncio
async def test_fetch_translations_falls_back_when_key_missing():
    respx.get(f"{BASE_URL}/data").mock(return_value=httpx.Response(200, json={}))

    translations, api_error = await fetch_translations()

    # No "translations" key → falls back to _FALLBACK_TRANSLATIONS but api_error is False
    assert api_error is False
    assert translations == _FALLBACK_TRANSLATIONS


# ── fetch_verse ───────────────────────────────────────────────────────────────


@respx.mock
@pytest.mark.asyncio
async def test_fetch_verse_returns_text_on_success():
    ref = "John 3:16"
    payload = {"text": "  For God so loved the world…  "}
    respx.get(f"{BASE_URL}/{ref}").mock(return_value=httpx.Response(200, json=payload))

    text = await fetch_verse(ref, "web")

    assert text == "For God so loved the world…"


@respx.mock
@pytest.mark.asyncio
async def test_fetch_verse_returns_empty_string_on_http_error():
    ref = "John 3:16"
    respx.get(f"{BASE_URL}/{ref}").mock(return_value=httpx.Response(404))

    text = await fetch_verse(ref, "web")

    assert text == ""


@respx.mock
@pytest.mark.asyncio
async def test_fetch_verse_returns_empty_string_on_network_error():
    ref = "John 3:16"
    respx.get(f"{BASE_URL}/{ref}").mock(side_effect=httpx.ConnectError("unreachable"))

    text = await fetch_verse(ref, "web")

    assert text == ""


@respx.mock
@pytest.mark.asyncio
async def test_fetch_verse_returns_empty_string_when_text_key_missing():
    ref = "John 3:16"
    respx.get(f"{BASE_URL}/{ref}").mock(return_value=httpx.Response(200, json={}))

    text = await fetch_verse(ref, "web")

    assert text == ""
