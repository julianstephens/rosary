"""Main rosary prayer screen: step-by-step guidance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer, Label, RichLog

from rosary.api import fetch_verse
from rosary.mysteries import ALL_SETS, MysterySet
from rosary.prayers import (
    APOSTLES_CREED,
    CLOSING_PRAYER,
    FATIMA_PRAYER,
    GLORY_BE,
    HAIL_HOLY_QUEEN,
    HAIL_MARY,
    OUR_FATHER,
    SIGN_OF_THE_CROSS,
)


@dataclass
class Step:
    title: str
    body: str
    # If set, the body will be replaced with the fetched verse once loaded.
    bible_ref: Optional[str] = None
    # Calculated fields for display
    decade: int = 0  # 0 = opening/closing, 1-5 = decade number
    is_mystery: bool = False


def build_steps(mystery_set: MysterySet) -> list[Step]:
    """Return the full ordered list of prayer steps for one Rosary."""
    steps: list[Step] = []

    # ── Opening ──────────────────────────────────────────────────────────────
    steps.append(Step(title="Sign of the Cross", body=SIGN_OF_THE_CROSS))
    steps.append(Step(title="The Apostles' Creed", body=APOSTLES_CREED))
    steps.append(Step(title="Our Father", body=OUR_FATHER))

    intentions = [
        ("Hail Mary (for Faith)", HAIL_MARY),
        ("Hail Mary (for Hope)", HAIL_MARY),
        ("Hail Mary (for Charity)", HAIL_MARY),
    ]
    for title, text in intentions:
        steps.append(Step(title=title, body=text))
    steps.append(Step(title="Glory Be", body=GLORY_BE))

    # ── Five Decades ─────────────────────────────────────────────────────────
    for decade_num, mystery in enumerate(mystery_set.mysteries, start=1):
        steps.append(
            Step(
                title=f"Mystery {decade_num}/5 — {mystery.name}",
                body=mystery.description,
                bible_ref=mystery.scripture_ref,
                decade=decade_num,
                is_mystery=True,
            )
        )
        steps.append(Step(title="Our Father", body=OUR_FATHER, decade=decade_num))
        for bead in range(1, 11):
            steps.append(
                Step(
                    title=f"Hail Mary {bead}/10",
                    body=HAIL_MARY,
                    decade=decade_num,
                )
            )
        steps.append(Step(title="Glory Be", body=GLORY_BE, decade=decade_num))
        steps.append(Step(title="Fatima Prayer", body=FATIMA_PRAYER, decade=decade_num))

    # ── Closing ───────────────────────────────────────────────────────────────
    steps.append(Step(title="Hail Holy Queen", body=HAIL_HOLY_QUEEN))
    steps.append(Step(title="Closing Prayer", body=CLOSING_PRAYER))
    steps.append(Step(title="Sign of the Cross", body=SIGN_OF_THE_CROSS))

    return steps


class RosaryScreen(Screen):
    """Third screen: walks the user through every prayer step."""

    CSS = """
    RosaryScreen {
        layout: vertical;
    }

    #header-bar {
        dock: top;
        height: 3;
        background: $boost;
        padding: 0 2;
        align: left middle;
    }

    #set-label {
        color: $accent;
        text-style: bold;
        content-align: left middle;
        width: 1fr;
    }

    #progress-label {
        color: $text-muted;
        content-align: right middle;
        width: auto;
    }

    #step-title {
        text-align: center;
        text-style: bold;
        color: $accent;
        padding: 1 4;
        width: 100%;
    }

    #step-body {
        width: 100%;
        height: 1fr;
        padding: 0 6;
        overflow-y: auto;
    }

    #verse-label {
        text-align: center;
        color: $text-muted;
        padding: 0 4 1 4;
        width: 100%;
    }

    #step-counter {
        dock: bottom;
        height: 3;
        background: $boost;
        color: $text-muted;
        text-align: center;
        width: 100%;
        content-align: center middle;
    }
    """

    BINDINGS = [
        Binding("space", "next_step", "Next", priority=True),
        Binding("right", "next_step", "Next", priority=True, show=False),
        Binding("backspace", "prev_step", "Back", priority=True),
        Binding("left", "prev_step", "Back", priority=True, show=False),
        Binding("q", "app.quit", "Quit", priority=True),
    ]

    def __init__(self) -> None:
        super().__init__()
        mystery_set = ALL_SETS[self.app.mystery_set_key]  # type: ignore[attr-defined]
        self._steps = build_steps(mystery_set)
        self._index = 0
        self._mystery_set_name = mystery_set.name
        # Cache for fetched verses: step index → verse text
        self._verse_cache: dict[int, str] = {}

    @property
    def _current(self) -> Step:
        return self._steps[self._index]

    def compose(self) -> ComposeResult:
        with Horizontal(id="header-bar"):
            yield Label("", id="set-label")
            yield Label("", id="progress-label")
        yield Label("", id="step-title")
        yield Label("", id="verse-label")
        yield RichLog(id="step-body", highlight=False, markup=False, wrap=True)
        yield Label("", id="step-counter")
        yield Footer()

    def on_mount(self) -> None:
        self._render_step()

    def _render_step(self) -> None:
        step = self._current
        total = len(self._steps)

        # Header
        self.query_one("#set-label", Label).update(self._mystery_set_name)
        decade_text = f"Decade {step.decade}/5" if step.decade else "Opening / Closing"
        self.query_one("#progress-label", Label).update(decade_text)

        # Step title
        self.query_one("#step-title", Label).update(step.title)

        # Verse reference label
        verse_label = self.query_one("#verse-label", Label)
        if step.bible_ref:
            verse_label.update(f"Scripture: {step.bible_ref}")
            verse_label.display = True
        else:
            verse_label.update("")
            verse_label.display = False

        # Body
        body_log = self.query_one("#step-body", RichLog)
        body_log.clear()

        if step.is_mystery and step.bible_ref:
            if self._index in self._verse_cache:
                verse_text = self._verse_cache[self._index]
                body_log.write(step.body)
                body_log.write("")
                body_log.write("─" * 40)
                body_log.write("")
                body_log.write(verse_text)
            else:
                body_log.write(step.body)
                body_log.write("")
                body_log.write("Loading scripture verse…")
                self._fetch_verse_for_current(self._index, step.bible_ref)
        else:
            body_log.write(step.body)

        # Step counter
        self.query_one("#step-counter", Label).update(
            f"Step {self._index + 1} of {total}  ·  Space = Next  ·  Backspace = Back  ·  Q = Quit"
        )

    @work(exclusive=False)
    async def _fetch_verse_for_current(self, step_index: int, ref: str) -> None:
        translation_id: str = self.app.translation_id  # type: ignore[attr-defined]
        verse_text = await fetch_verse(ref, translation_id)
        if verse_text:
            self._verse_cache[step_index] = verse_text
        else:
            self._verse_cache[step_index] = "(Verse not available for this translation)"
        # Only re-render if we are still on the same step
        if self._index == step_index:
            self._render_step()

    def action_next_step(self) -> None:
        if self._index < len(self._steps) - 1:
            self._index += 1
            self._render_step()
        else:
            self._show_completion()

    def action_prev_step(self) -> None:
        if self._index > 0:
            self._index -= 1
            self._render_step()

    def _show_completion(self) -> None:
        body_log = self.query_one("#step-body", RichLog)
        self.query_one("#step-title", Label).update("Rosary Complete ✝")
        self.query_one("#verse-label", Label).display = False
        body_log.clear()
        body_log.write(
            "You have completed the Rosary.\n\n"
            "May Our Lady intercede for you.\n\n"
            "Press Q to exit or Backspace to go back."
        )
        self.query_one("#step-counter", Label).update(
            "Complete  ·  Backspace = Back  ·  Q = Quit"
        )
