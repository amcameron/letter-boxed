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
