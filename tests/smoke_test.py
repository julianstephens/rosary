"""Standalone smoke test for installed rosary distributions.

This file is intended to be run directly, for example:
    uv run --isolated --no-project --with dist/*.whl tests/smoke_test.py
"""

from __future__ import annotations

import asyncio
import importlib.metadata as metadata
import shutil

import rosary.screens.welcome as welcome_module
from rosary.app import RosaryApp
from rosary.screens.rosary import RosaryScreen


async def _fake_fetch_translations() -> tuple[list[dict[str, str]], bool]:
    """Avoid live network access during the smoke test."""
    return (
        [
            {
                "identifier": "kjv",
                "name": "King James Version",
                "language": "English",
            }
        ],
        False,
    )


async def _exercise_app() -> None:
    welcome_module.fetch_translations = _fake_fetch_translations

    app = RosaryApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        assert app.screen.__class__.__name__ == "WelcomeScreen"

        await pilot.click("#continue-btn")
        await pilot.pause()
        assert app.screen.__class__.__name__ == "MysterySelectScreen"

        await pilot.click("#begin-btn")
        await pilot.pause()
        assert app.screen.__class__.__name__ == "IntentionsScreen"

        await pilot.click("#begin-btn")
        await pilot.pause()
        assert isinstance(app.screen, RosaryScreen)
        assert app.screen._current.title == "Sign of the Cross"


def main() -> None:
    version = metadata.version("rosary")
    assert version, "Installed package version should be available"

    console_scripts = metadata.entry_points(group="console_scripts")
    rosary_entry = next((ep for ep in console_scripts if ep.name == "rosary"), None)
    assert rosary_entry is not None, "Expected a 'rosary' console script"
    assert rosary_entry.value == "rosary.main:main"

    assert shutil.which("rosary") is not None, "Expected 'rosary' on PATH"

    asyncio.run(_exercise_app())
    print(f"Smoke test passed for rosary {version}")


if __name__ == "__main__":
    main()
