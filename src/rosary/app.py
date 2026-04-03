"""RosaryApp — top-level Textual application."""

from __future__ import annotations

from textual.app import App

from rosary.screens.welcome import WelcomeScreen


class RosaryApp(App):
    """A TUI guide through the Holy Rosary."""

    TITLE = "The Holy Rosary"
    CSS = """
    App {
        background: $surface;
    }
    """

    # Shared state written by WelcomeScreen / MysterySelectScreen,
    # read by RosaryScreen.
    translation_id: str = "kjv"
    translation_name: str = "King James Version"
    mystery_set_key: str = "Joyful"
    language: str = "English"

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())
