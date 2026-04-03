"""Tests for rosary.screens.rosary — pure logic (build_steps, _md)."""

import pytest

from rosary.mysteries import GLORIOUS, JOYFUL, LUMINOUS, SORROWFUL
from rosary.prayers import get_prayers
from rosary.screens.rosary import Step, _md, build_steps

# ── _md helper ───────────────────────────────────────────────────────────────


def test_md_converts_newlines_to_markdown_linebreaks():
    result = _md("line one\nline two")
    assert result == "line one  \nline two"


def test_md_preserves_text_without_newlines():
    result = _md("no newlines here")
    assert result == "no newlines here"


def test_md_empty_string():
    assert _md("") == ""


# ── build_steps structure ─────────────────────────────────────────────────────

PRAYERS_EN = get_prayers("English")
PRAYERS_LA = get_prayers("Latin")


@pytest.mark.parametrize(
    "mystery_set,prayers",
    [
        (JOYFUL, PRAYERS_EN),
        (SORROWFUL, PRAYERS_EN),
        (GLORIOUS, PRAYERS_EN),
        (LUMINOUS, PRAYERS_EN),
        (JOYFUL, PRAYERS_LA),
    ],
)
def test_build_steps_returns_list_of_step(mystery_set, prayers):
    steps = build_steps(mystery_set, prayers)
    assert all(isinstance(s, Step) for s in steps)


@pytest.mark.parametrize("mystery_set", [JOYFUL, SORROWFUL, GLORIOUS, LUMINOUS])
def test_build_steps_total_count(mystery_set):
    # Opening: Sign of Cross, Creed, Our Father, 3×Hail Mary, Glory Be = 7
    # Per decade: mystery + decade prayers = 2 × 5 = 10
    # Closing: Hail Holy Queen, Closing Prayer, Sign of Cross = 3
    # Total = 7 + 10 + 3 = 20
    steps = build_steps(mystery_set, PRAYERS_EN)
    assert len(steps) == 20


def test_build_steps_first_step_is_sign_of_cross():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    assert steps[0].title == "Sign of the Cross"


def test_build_steps_last_step_is_sign_of_cross():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    assert steps[-1].title == "Sign of the Cross"


def test_build_steps_second_step_is_apostles_creed():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    assert steps[1].title == "The Apostles' Creed"


def test_build_steps_opening_non_mystery_steps_have_decade_zero():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    opening = steps[:7]
    for step in opening:
        assert step.decade == 0


def test_build_steps_five_mystery_steps():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    mystery_steps = [s for s in steps if s.is_mystery]
    assert len(mystery_steps) == 5


def test_build_steps_five_decade_steps():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    decade_steps = [s for s in steps if s.is_decade]
    assert len(decade_steps) == 5


def test_build_steps_mystery_steps_have_correct_decade_numbers():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    mystery_steps = [s for s in steps if s.is_mystery]
    for i, step in enumerate(mystery_steps, start=1):
        assert step.decade == i


def test_build_steps_decade_steps_have_correct_decade_numbers():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    decade_steps = [s for s in steps if s.is_decade]
    for i, step in enumerate(decade_steps, start=1):
        assert step.decade == i


def test_build_steps_mystery_and_decade_alternate():
    """After opening (7 steps), mystery and decade steps should alternate."""
    steps = build_steps(JOYFUL, PRAYERS_EN)
    body = steps[7:17]  # 5 decades × 2 steps
    for i in range(0, 10, 2):
        assert body[i].is_mystery, f"Step {i} should be a mystery"
        assert body[i + 1].is_decade, f"Step {i+1} should be a decade"


def test_build_steps_mystery_titles_match_mystery_set():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    mystery_steps = [s for s in steps if s.is_mystery]
    for i, (step, mystery) in enumerate(zip(mystery_steps, JOYFUL.mysteries), start=1):
        assert mystery.name in step.title
        assert f"{i}/5" in step.title


def test_build_steps_mystery_body_is_description():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    mystery_steps = [s for s in steps if s.is_mystery]
    for step, mystery in zip(mystery_steps, JOYFUL.mysteries):
        assert step.body == mystery.description


def test_build_steps_mystery_steps_carry_bible_ref():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    mystery_steps = [s for s in steps if s.is_mystery]
    for step, mystery in zip(mystery_steps, JOYFUL.mysteries):
        assert step.bible_ref == mystery.scripture_ref


def test_build_steps_closing_titles():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    closing = steps[17:]
    assert closing[0].title == "Hail Holy Queen"
    assert closing[1].title == "Closing Prayer"
    assert closing[2].title == "Sign of the Cross"


def test_build_steps_non_mystery_decade_zero_steps_not_flagged():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    for step in steps:
        if step.decade == 0:
            assert not step.is_mystery
            assert not step.is_decade


def test_build_steps_hail_mary_steps_for_faith_hope_charity():
    steps = build_steps(JOYFUL, PRAYERS_EN)
    virtue_steps = [s for s in steps if "Hail Mary" in s.title]
    titles = [s.title for s in virtue_steps]
    assert "Hail Mary (for Faith)" in titles
    assert "Hail Mary (for Hope)" in titles
    assert "Hail Mary (for Charity)" in titles
