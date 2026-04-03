"""Tests for rosary.mysteries."""

from datetime import date
from unittest.mock import patch

import pytest

from rosary.mysteries import (
    ALL_SETS,
    JOYFUL,
    suggest_mystery_set,
)

# ── Data structure ────────────────────────────────────────────────────────────


def test_all_sets_contains_four_entries():
    assert set(ALL_SETS.keys()) == {"Joyful", "Sorrowful", "Glorious", "Luminous"}


def test_each_set_has_five_mysteries():
    for name, mystery_set in ALL_SETS.items():
        assert len(mystery_set.mysteries) == 5, f"{name} should have 5 mysteries"


def test_mystery_names_are_nonempty():
    for mystery_set in ALL_SETS.values():
        for mystery in mystery_set.mysteries:
            assert mystery.name.strip()
            assert mystery.description.strip()


def test_mystery_is_frozen():
    mystery = JOYFUL.mysteries[0]
    with pytest.raises(Exception):
        mystery.name = "changed"  # type: ignore[misc]


def test_mystery_set_is_frozen():
    with pytest.raises(Exception):
        JOYFUL.name = "changed"  # type: ignore[misc]


def test_mysteries_without_scripture_ref_have_note():
    """Any mystery with scripture_ref=None must provide a scripture_note."""
    for mystery_set in ALL_SETS.values():
        for mystery in mystery_set.mysteries:
            if mystery.scripture_ref is None:
                assert mystery.scripture_note, f"{mystery.name} has no ref and no note"


def test_mysteries_with_scripture_ref_have_no_note():
    """Mysteries with a ref should not also carry a redundant note."""
    for mystery_set in ALL_SETS.values():
        for mystery in mystery_set.mysteries:
            if mystery.scripture_ref is not None:
                assert (
                    mystery.scripture_note is None
                ), f"{mystery.name} has both ref and note"


# ── suggest_mystery_set ───────────────────────────────────────────────────────

# Real dates with known weekdays (2024-01-01 is a Monday)
_DAY_CASES = [
    (date(2024, 1, 1), "Joyful"),     # Monday
    (date(2024, 1, 2), "Sorrowful"),  # Tuesday
    (date(2024, 1, 3), "Glorious"),   # Wednesday
    (date(2024, 1, 4), "Luminous"),   # Thursday
    (date(2024, 1, 5), "Sorrowful"),  # Friday
    (date(2024, 1, 6), "Joyful"),     # Saturday
    (date(2024, 1, 7), "Glorious"),   # Sunday
]


@pytest.mark.parametrize("target_date,expected_key", _DAY_CASES)
def test_suggest_mystery_set_correct_day(target_date, expected_key):
    with patch("rosary.mysteries.date") as mock_date:
        mock_date.today.return_value = target_date
        result = suggest_mystery_set()
        assert result == expected_key, (
            f"{target_date} (weekday {target_date.weekday()}) should suggest "
            f"{expected_key}, got {result}"
        )


def test_suggest_mystery_set_returns_valid_key():
    key = suggest_mystery_set()
    assert key in ALL_SETS
