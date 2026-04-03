"""Mystery selection screen."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, RadioButton, RadioSet

from rosary.mysteries import ALL_SETS, suggest_mystery_set


class MysterySelectScreen(Screen):
    """Second screen: pick the mystery set to pray today."""

    CSS = """
    MysterySelectScreen {
        align: center middle;
    }

    #title {
        text-align: center;
        text-style: bold;
        color: $accent;
        padding: 1 2;
        width: 100%;
    }

    #subtitle {
        text-align: center;
        color: $text-muted;
        padding: 0 2 1 2;
        width: 100%;
    }

    #mystery-set {
        width: 50;
        height: auto;
        border: round $accent;
        padding: 1 2;
    }

    #begin-btn {
        margin: 1 2;
    }
    """

    BINDINGS = [
        Binding("escape", "go_back", "Back", priority=True),
        Binding("q", "app.quit", "Quit", priority=True),
    ]

    def compose(self) -> ComposeResult:
        suggested = suggest_mystery_set()
        yield Header(show_clock=False)
        yield Label("✝  Choose the Mysteries", id="title")
        yield Label(
            f"Traditionally prayed today: {ALL_SETS[suggested].name}",
            id="subtitle",
        )
        with RadioSet(id="mystery-set"):
            for key, mystery_set in ALL_SETS.items():
                yield RadioButton(
                    mystery_set.name,
                    value=(key == suggested),
                    id=f"mystery-{key}",
                )
        yield Button("Begin Rosary", id="begin-btn", variant="primary")
        yield Footer()

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "begin-btn":
            radio_set = self.query_one("#mystery-set", RadioSet)
            selected = radio_set.pressed_button
            if selected is None:
                return
            key = (selected.id or "").removeprefix("mystery-")
            self.app.mystery_set_key = key  # type: ignore
            from rosary.screens.rosary import RosaryScreen

            self.app.push_screen(RosaryScreen())
