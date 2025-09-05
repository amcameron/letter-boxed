"""Test the functionality of letter_boxed.py"""

from hypothesis import given, strategies as st
from pytest import raises


from letter_boxed.letter_boxed import find_valid_words, Side  # type: ignore


@given(...)
def test_find_valid_words(words: list[str]):
    """find_valid_words should find a valid word given valid inputs"""
    sides = ["lim", "knr", "tae", "pjo"]
    target = "kleptomania"
    words.append(target)

    assert target in find_valid_words(words, sides)


@given(...)
def test_find_valid_words_empty_dictionary(sides: list[Side]):
    words: list[str] = []

    with raises(StopIteration):
        next(find_valid_words(words, sides))
