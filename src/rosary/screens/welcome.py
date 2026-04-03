"""Welcome screen: select prayer language and Bible translation."""

from __future__ import annotations

from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    LoadingIndicator,
    RadioButton,
    RadioSet,
)

from rosary.api import fetch_translations


class WelcomeScreen(Screen):
    """First screen shown to the user. Choose language and Bible translation."""

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

    #api-error {
        text-align: center;
        color: $error;
        background: $error 10%;
        padding: 0 2;
        width: 100%;
    }

    #lang-label {
        text-align: center;
        color: $text-muted;
        padding: 0 2;
        width: 100%;
    }

    #lang-select {
        width: 30;
        height: auto;
        margin: 0 0 1 0;
    }

    #trans-label {
        text-align: center;
        color: $text-muted;
        padding: 0 2;
        width: 100%;
    }

    #loading {
        width: 100%;
        height: auto;
    }

    #translation-list {
        width: 60;
        height: auto;
        max-height: 14;
        border: round $accent;
    }

    #continue-btn {
        margin: 1 2;
    }
    """

    BINDINGS = [Binding("q", "app.quit", "Quit", priority=True)]

    def __init__(self) -> None:
        super().__init__()
        self._translations: dict[str, dict] = {}
        self._loaded = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Label("✝  The Holy Rosary", id="title")
        yield Label("", id="api-error")
        yield Label("Pray in:", id="lang-label")
        with RadioSet(id="lang-select"):
            yield RadioButton("English", value=True, id="lang-en")
            yield RadioButton("Latin", id="lang-la")
        yield Label("Select a Bible translation:", id="trans-label")
        yield LoadingIndicator(id="loading")
        yield ListView(id="translation-list")
        yield Button("Continue →", id="continue-btn", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#api-error", Label).display = False
        self.query_one("#translation-list", ListView).display = False
        self._load_translations()

    @work(exclusive=True)
    async def _load_translations(self) -> None:
        translations, api_error = await fetch_translations()
        self._translations = {t["identifier"]: t for t in translations}

        if api_error:
            err = self.query_one("#api-error", Label)
            err.update(
                "⚠  Could not reach bible-api.com — showing cached translations."
            )
            err.display = True

        # Sort: KJV first, then remaining English, then other languages
        def _sort_key(t: dict) -> tuple:
            if t["identifier"] == "kjv":
                return (0, "")
            lang = t.get("language", "")
            if lang.startswith("English"):
                return (1, t["name"])
            return (2, t["name"])

        sorted_translations = sorted(translations, key=_sort_key)

        list_view = self.query_one("#translation-list", ListView)
        for t in sorted_translations:
            lang = t.get("language", "")
            display = f"{t['name']}  [{lang}]" if lang else t["name"]
            list_view.append(ListItem(Label(display), id=f"trans-{t['identifier']}"))

        self.query_one("#loading", LoadingIndicator).display = False
        self._loaded = True

        # Only show the list if English is currently selected
        lang_set = self.query_one("#lang-select", RadioSet)
        if lang_set.pressed_button and lang_set.pressed_button.id == "lang-en":
            list_view.display = True
            list_view.index = 0  # pre-highlight KJV

    @on(RadioSet.Changed, "#lang-select")
    def on_language_changed(self, event: RadioSet.Changed) -> None:
        is_latin = event.pressed.id == "lang-la"
        self.query_one("#trans-label", Label).display = not is_latin
        lv = self.query_one("#translation-list", ListView)
        lv.display = not is_latin and self._loaded

    @on(ListView.Selected, "#translation-list")
    def on_translation_selected(self, event: ListView.Selected) -> None:
        item_id: str = event.item.id or ""
        translation_id = item_id.removeprefix("trans-")
        self.app.translation_id = translation_id  # type: ignore[attr-defined]
        self.app.translation_name = self._translations.get(translation_id, {}).get(  # type: ignore[attr-defined]
            "name", translation_id
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "continue-btn":
            return
        lang_set = self.query_one("#lang-select", RadioSet)
        is_latin = (
            lang_set.pressed_button is not None
            and lang_set.pressed_button.id == "lang-la"
        )
        if is_latin:
            self.app.language = "Latin"  # type: ignore[attr-defined]
            self.app.translation_id = "clementine"  # type: ignore[attr-defined]
            self.app.translation_name = "Clementine Latin Vulgate"  # type: ignore[attr-defined]
        else:
            self.app.language = "English"  # type: ignore[attr-defined]

        from rosary.screens.mystery_select import MysterySelectScreen

        self.app.push_screen(MysterySelectScreen())
