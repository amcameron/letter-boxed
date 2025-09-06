"""Test the functionality of letter_boxed.py"""

from itertools import pairwise
from random import sample

from hypothesis import assume, given, strategies as st
from pytest import raises


from letter_boxed.letter_boxed import (  # type: ignore
    find_phrases,
    find_valid_words,
    IllegalBoardError,
    Side,
)


@given(...)
def test_find_valid_words(words: list[str]):
    """find_valid_words should find a valid word given valid inputs"""
    sides = ["lim", "knr", "tae", "pjo"]
    target = "kleptomania"
    words.append(target)

    assert target in find_valid_words(words, sides)


@st.composite
def words_with_distinct_letters(draw: st.DrawFn) -> list[str]:
    """Strategy for generating words which do not share any letters."""
    letters = list(draw(st.sets(st.characters(), min_size=1)))
    num_partitions = draw(st.integers(min_value=1, max_value=len(letters) or 1))
    partitions: list[str] = []
    for _ in range(num_partitions):
        partition_size = draw(
            st.integers(
                min_value=1,
                max_value=len(letters) + 1,
            )
        )
        partitions.append("".join(letters[:partition_size]))
        letters = letters[partition_size:]
    return partitions


@given(words_with_distinct_letters())
def test_find_valid_words_empty_dictionary(sides: list[Side]):
    """find_valid_words should find nothing if given an empty list of valid words."""
    words: list[str] = []

    with raises(StopIteration):
        next(find_valid_words(words, sides))


@given(
    words=..., sides=st.lists(st.text(), min_size=2), repeated_character=st.characters()
)
def test_find_valid_words_with_shared_letters(
    words: list[str], sides: list[Side], repeated_character: str
):
    """find_valid_words should raise an error if two or more sides share a letter."""
    for idx in sample(range(len(sides)), 2):
        sides[idx] = sides[idx] + repeated_character

    with raises(IllegalBoardError):
        next(find_valid_words(words, sides))


@given(...)
def test_find_phrases_returns_legal_phrases(words: list[str], letters_to_cover: str):
    """find_phrases should return legal phrases, i.e. ones where the last letter
    of each word is the starting letter of the next word"""
    assume(set(letters_to_cover) <= set(letter for word in words for letter in word))

    for phrase in find_phrases(words, letters_to_cover):
        for word, next_word in pairwise(phrase):
            assert word[-1] == next_word[0]


@given(words=st.lists(st.text(min_size=1)), letters_to_cover=..., starting_letters=...)
def test_find_phrases_covers_requested_letters(
    words: list[str], letters_to_cover: str, starting_letters: None | str
):
    for phrase in find_phrases(words, letters_to_cover, starting_letters):
        assert set(letters_to_cover) <= set(
            letter for word in phrase for letter in word
        )
