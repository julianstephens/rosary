"""Welcome screen: select a Bible translation."""

from __future__ import annotations

from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, LoadingIndicator

from rosary.api import fetch_translations


class WelcomeScreen(Screen):
    """First screen shown to the user. Fetches translations and lets them pick one."""

    CSS = """
    WelcomeScreen {
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

    #loading {
        width: 100%;
        height: auto;
    }

    #translation-list {
        width: 60;
        height: auto;
        max-height: 20;
        border: round $accent;
    }
    """

    BINDINGS = [Binding("q", "app.quit", "Quit", priority=True)]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Label("✝  The Holy Rosary", id="title")
        yield Label("Select a Bible translation to begin", id="subtitle")
        yield LoadingIndicator(id="loading")
        yield ListView(id="translation-list")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#translation-list", ListView).display = False
        self._load_translations()

    @work(exclusive=True)
    async def _load_translations(self) -> None:
        translations = await fetch_translations()
        self._translations = {t["identifier"]: t for t in translations}

        list_view = self.query_one("#translation-list", ListView)
        for t in translations:
            lang = t.get("language", "")
            display = f"{t['name']}  [{lang}]" if lang else t["name"]
            list_view.append(ListItem(Label(display), id=f"trans-{t['identifier']}"))

        self.query_one("#loading", LoadingIndicator).display = False
        list_view.display = True
        list_view.focus()

    @on(ListView.Selected, "#translation-list")
    def on_translation_selected(self, event: ListView.Selected) -> None:
        item_id: str = event.item.id or ""
        translation_id = item_id.removeprefix("trans-")
        translation = self._translations.get(translation_id, {})
        self.app.translation_id = translation_id  # type: ignore
        self.app.translation_name = translation.get("name", translation_id)  # type: ignore
        from rosary.screens.mystery_select import MysterySelectScreen

        self.app.push_screen(MysterySelectScreen())
