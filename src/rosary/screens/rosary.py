"""Main rosary prayer screen: step-by-step guidance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer, Label, Markdown

from rosary.api import fetch_verse
from rosary.mysteries import ALL_SETS, MysterySet
from rosary.prayers import get_prayers


@dataclass
class Step:
    title: str
    body: str  # Markdown-formatted content
    bible_ref: Optional[str] = None
    decade: int = 0  # 0 = opening/closing, 1-5 = decade number
    is_mystery: bool = False
    is_decade: bool = False


def _md(text: str) -> str:
    """Convert plain prayer text to Markdown with preserved line breaks."""
    return text.replace("\n", "  \n")


def _build_decade_markdown(prayers: dict) -> str:
    return (
        f"## Our Father\n\n{_md(prayers['our_father'])}\n\n"
        f"---\n\n"
        f"## Hail Mary × 10\n\n{_md(prayers['hail_mary'])}\n\n"
        f"---\n\n"
        f"## Glory Be\n\n{_md(prayers['glory_be'])}\n\n"
        f"---\n\n"
        f"## Fatima Prayer\n\n{_md(prayers['fatima_prayer'])}"
    )


def build_steps(mystery_set: MysterySet, prayers: dict) -> list[Step]:
    """Return the full ordered list of prayer steps for one Rosary."""
    steps: list[Step] = []

    # ── Opening ──────────────────────────────────────────────────────────────
    steps.append(
        Step(title="Sign of the Cross", body=_md(prayers["sign_of_the_cross"]))
    )
    steps.append(Step(title="The Apostles' Creed", body=_md(prayers["apostles_creed"])))
    steps.append(Step(title="Our Father", body=_md(prayers["our_father"])))
    for label in (
        "Hail Mary (for Faith)",
        "Hail Mary (for Hope)",
        "Hail Mary (for Charity)",
    ):
        steps.append(Step(title=label, body=_md(prayers["hail_mary"])))
    steps.append(Step(title="Glory Be", body=_md(prayers["glory_be"])))

    # ── Five Decades ─────────────────────────────────────────────────────────
    decade_md = _build_decade_markdown(prayers)
    for decade_num, mystery in enumerate(mystery_set.mysteries, start=1):
        # Mystery announcement — verse fetched lazily
        steps.append(
            Step(
                title=f"Mystery {decade_num}/5 — {mystery.name}",
                body=mystery.description,
                bible_ref=mystery.scripture_ref,
                decade=decade_num,
                is_mystery=True,
            )
        )
        # Full decade prayers on a single screen
        steps.append(
            Step(
                title=f"Decade {decade_num} — Prayers",
                body=decade_md,
                decade=decade_num,
                is_decade=True,
            )
        )

    # ── Closing ───────────────────────────────────────────────────────────────
    steps.append(Step(title="Hail Holy Queen", body=_md(prayers["hail_holy_queen"])))
    steps.append(Step(title="Closing Prayer", body=_md(prayers["closing_prayer"])))
    steps.append(
        Step(title="Sign of the Cross", body=_md(prayers["sign_of_the_cross"]))
    )

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
        language: str = getattr(self.app, "language", "English")
        self._steps = build_steps(mystery_set, get_prayers(language))
        self._index = 0
        self._mystery_set_name = mystery_set.name
        self._verse_cache: dict[int, str] = {}

    @property
    def _current(self) -> Step:
        return self._steps[self._index]

    def compose(self) -> ComposeResult:
        with Horizontal(id="header-bar"):
            yield Label("", id="set-label")
            yield Label("", id="progress-label")
        yield Label("", id="step-title")
        yield Markdown("", id="step-body")
        yield Label("", id="step-counter")
        yield Footer()

    def on_mount(self) -> None:
        self._render_step()

    def _build_content(self) -> str:
        step = self._current
        if step.is_mystery and step.bible_ref:
            verse = self._verse_cache.get(self._index, "_Loading scripture verse…_")
            language: str = getattr(self.app, "language", "English")
            ref_note = (
                f"**Scripture: {step.bible_ref}** _(KJV)_"
                if language == "Latin"
                else f"**Scripture: {step.bible_ref}**"
            )
            return (
                f"{step.body}\n\n"
                f"---\n\n"
                f"{ref_note}\n\n"
                f"{verse}"
            )
        return step.body

    def _render_step(self) -> None:
        step = self._current
        total = len(self._steps)

        self.query_one("#set-label", Label).update(self._mystery_set_name)
        decade_text = f"Decade {step.decade}/5" if step.decade else "Opening / Closing"
        self.query_one("#progress-label", Label).update(decade_text)
        self.query_one("#step-title", Label).update(step.title)
        self.query_one("#step-body", Markdown).update(self._build_content())
        self.query_one("#step-counter", Label).update(
            f"Step {self._index + 1} of {total}"
            "  ·  Space = Next  ·  Backspace = Back  ·  Q = Quit"
        )

        if step.is_mystery and step.bible_ref and self._index not in self._verse_cache:
            self._fetch_verse_for_current(self._index, step.bible_ref)

    @work(exclusive=False)
    async def _fetch_verse_for_current(self, step_index: int, ref: str) -> None:
        language: str = getattr(self.app, "language", "English")
        # The Clementine Vulgate API requires Latin book names for ref parsing.
        # Always use KJV for scripture lookups so English refs resolve correctly.
        translation_id = "kjv" if language == "Latin" else self.app.translation_id  # type: ignore[attr-defined]
        verse_text = await fetch_verse(ref, translation_id)
        self._verse_cache[step_index] = (
            verse_text or "_(Verse not available for this translation.)_"
        )
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
        self.query_one("#step-title", Label).update("Rosary Complete ✝")
        self.query_one("#step-body", Markdown).update(
            "You have completed the Rosary.\n\n"
            "May Our Lady intercede for you.\n\n"
            "---\n\n"
            "Press **Q** to exit or **Backspace** to go back."
        )
        self.query_one("#step-counter", Label).update(
            "Complete  ·  Backspace = Back  ·  Q = Quit"
        )
