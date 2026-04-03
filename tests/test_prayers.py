"""Tests for rosary.prayers."""


from rosary.prayers import (
    FINAL_SIGN_OF_THE_CROSS,
    HAIL_MARY,
    OUR_FATHER,
    SIGN_OF_THE_CROSS,
    get_prayers,
)

EXPECTED_KEYS = {
    "sign_of_the_cross",
    "apostles_creed",
    "our_father",
    "hail_mary",
    "glory_be",
    "fatima_prayer",
    "hail_holy_queen",
    "closing_prayer",
}


def test_get_prayers_english_returns_all_keys():
    prayers = get_prayers("English")
    assert set(prayers.keys()) == EXPECTED_KEYS


def test_get_prayers_latin_returns_all_keys():
    prayers = get_prayers("Latin")
    assert set(prayers.keys()) == EXPECTED_KEYS


def test_get_prayers_unknown_language_falls_back_to_english():
    prayers = get_prayers("Klingon")
    assert prayers["sign_of_the_cross"] == SIGN_OF_THE_CROSS


def test_get_prayers_english_values_are_nonempty():
    prayers = get_prayers("English")
    for key, text in prayers.items():
        assert text.strip(), f"Prayer '{key}' is empty"


def test_get_prayers_latin_values_are_nonempty():
    prayers = get_prayers("Latin")
    for key, text in prayers.items():
        assert text.strip(), f"Latin prayer '{key}' is empty"


def test_english_and_latin_prayers_differ():
    en = get_prayers("English")
    la = get_prayers("Latin")
    for key in EXPECTED_KEYS:
        assert en[key] != la[key], f"English and Latin '{key}' should differ"


def test_final_sign_of_the_cross_equals_sign_of_the_cross():
    assert FINAL_SIGN_OF_THE_CROSS == SIGN_OF_THE_CROSS


def test_english_sign_of_the_cross_contains_expected_text():
    assert "Father" in SIGN_OF_THE_CROSS
    assert "Amen" in SIGN_OF_THE_CROSS


def test_latin_sign_of_the_cross_contains_expected_text():
    la = get_prayers("Latin")
    assert "Patris" in la["sign_of_the_cross"]
    assert "Amen" in la["sign_of_the_cross"]


def test_hail_mary_ends_with_amen():
    assert HAIL_MARY.strip().endswith("Amen.")


def test_our_father_ends_with_amen():
    assert OUR_FATHER.strip().endswith("Amen.")
