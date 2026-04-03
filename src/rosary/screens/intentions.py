"""Intentions prompt screen."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Markdown

_INTENTIONS_EN = """\
Before we begin, take a moment to offer your intentions to God.

You may pray silently or aloud:

---

*"Lord, I offer this Rosary for…"*

Pause here and speak your intentions from the heart.

---

When you are ready, press **Begin** or **Space** to start the Rosary.
"""


class IntentionsScreen(Screen):
    """Prompt the user to verbally offer their intentions before beginning."""

    CSS = """
    IntentionsScreen {
        align: center middle;
    }

    #title {
        text-align: center;
        text-style: bold;
        color: $accent;
        padding: 1 2;
        width: 100%;
    }

    #body {
        width: 70;
        max-width: 100%;
        height: auto;
        padding: 0 4;
    }

    #begin-btn {
        margin: 1 2;
    }
    """

    BINDINGS = [
        Binding("space", "begin", "Begin", priority=True),
        Binding("escape", "go_back", "Back", priority=True),
        Binding("q", "app.quit", "Quit", priority=True),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Label("✝  Offer Your Intentions", id="title")
        yield Markdown(_INTENTIONS_EN, id="body")
        yield Button("Begin Rosary", id="begin-btn", variant="primary")
        yield Footer()

    def action_begin(self) -> None:
        from rosary.screens.rosary import RosaryScreen

        self.app.push_screen(RosaryScreen())

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "begin-btn":
            self.action_begin()
