"""Test the functionality of letter_boxed.py"""

from hypothesis import given, strategies as st
from pytest import raises


from letter_boxed.letter_boxed import find_valid_words  # type: ignore


@given(...)
def test_find_valid_words(words: list[str]):
    """find_valid_words should find a valid word given valid inputs"""
    sides = [["l", "i", "m"], ["k", "n", "r"], ["t", "a", "e"], ["p", "j", "o"]]
    target = "kleptomania"
    words.append(target)

    assert target in find_valid_words(words, sides)


@given(st.lists(st.lists(st.characters())))
def test_find_valid_words_empty_dictionary(sides: list[list[str]]):
    words: list[str] = []

    result = find_valid_words(words, sides)

    with raises(StopIteration):
        next(result)
