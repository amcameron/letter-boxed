"""Solve the Letter Boxed game."""

import re
from collections.abc import Callable
from typing import Iterator


type Side = str


class IllegalBoardError(Exception):
    """An error representing an illegal game configuration"""


def _build_matcher(sides: list[Side]) -> Callable[[str], bool]:
    """Build a predicate to decide whether a word can be spelled using the given sides."""
    valid_letters = "".join(sides)
    if not valid_letters:
        raise IllegalBoardError("No non-empty sides were provided: {sides=}")
    if len(set(valid_letters)) != len(valid_letters):
        raise IllegalBoardError(f"Duplicate letters: {sides=}")

    allowed_letters = re.compile(f"^[{re.escape(valid_letters)}]+$")

    disallowed_repeats = [
        re.compile(f"[{re.escape(side)}]{2,}") for side in sides if side
    ]

    def predicate(word: str) -> bool:
        return bool(allowed_letters.match(word)) and not any(
            repeated_side.match(word) for repeated_side in disallowed_repeats
        )

    return predicate


def find_valid_words(words: list[str], sides: list[Side]) -> Iterator[str]:
    """Filter the given set of words to just those which match the given "sides".

    A word matches the given sides if it can be spelled by choosing letters from
    one side at a time, consecutively, without taking from the same side consecutively.
    Letters and sides may be reused, just so long as the same side is not used
    twice in a row."""
    is_valid = _build_matcher(sides)
    for word in words:
        if is_valid(word):
            yield word


def find_phrases(words: list[str], letters_to_cover: str, starting_letters=None):
    """Build phrases from the given words which "cover" the given letters.

    Consecutive words must share their neighbouring letters, e.g. THY > YES > SINCE"""
    # TODO


if __name__ == "__main__":
    print("hello world")
