"""Solve the Letter Boxed game."""

import re
from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from typing import Iterator


type Side = str


class IllegalBoardError(Exception):
    """An error representing an illegal game configuration"""


@dataclass(frozen=True)
class LetterBoxWord:
    """Wrapper around str to provide utility properties."""

    value: str

    @cached_property
    def letters(self):
        """The set of letters in this word."""
        return frozenset(self.value)

    @property
    def first(self):
        """The first letter in this word."""
        return self.value[0]

    @property
    def last(self):
        """The last letter in this word."""
        return self.value[-1]


def _build_matcher(sides: list[Side]) -> Callable[[str], bool]:
    """Build a predicate to decide whether a word can be spelled using the given sides."""
    valid_letters = "".join(sides)
    if not valid_letters:
        raise IllegalBoardError("No non-empty sides were provided: {sides=}")
    if len(set(valid_letters)) != len(valid_letters):
        raise IllegalBoardError(f"Duplicate letters: {sides=}")

    allowed_letters = re.compile(f"^[{re.escape(valid_letters)}]+$")

    disallowed_repeats = [
        re.compile(f"[{re.escape(side)}]{{2,}}") for side in sides if side
    ]

    def predicate(word: str) -> bool:
        return bool(allowed_letters.match(word)) and not any(
            repeated_side.search(word) for repeated_side in disallowed_repeats
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


def _generate_phrases(
    words: frozenset[LetterBoxWord],
    desired_length: int,
    starting_word: LetterBoxWord,
) -> Iterator[list[LetterBoxWord]]:
    if desired_length == 0:
        return
    phrase = [starting_word]
    visited: list[set[LetterBoxWord]] = [set() for _ in range(desired_length)]
    visited[0].update(words)  # Only allowed to use the given word.
    while True:
        while len(phrase) < desired_length:
            if not phrase:
                return
            phrase_idx = len(phrase)
            next_start = phrase[-1].last
            next_word = next(
                (
                    w
                    for w in words
                    if w.first == next_start
                    and w not in phrase
                    and w not in visited[phrase_idx]
                ),
                None,
            )
            if next_word is None:
                visited[phrase_idx].clear()
                phrase.pop()
                continue
            phrase.append(next_word)
            visited[phrase_idx].add(next_word)
        yield phrase
        phrase.pop()


def find_phrases(
    words: list[str], letters_to_cover: str, starting_letters: None | str = None
) -> Iterator[list[str]]:
    """Build phrases from the given words which "cover" the given letters.

    Consecutive words must share their neighbouring letters, e.g. THY > YES > SINCE"""

    def _starts(word: LetterBoxWord) -> bool:
        return not starting_letters or word.value[0] in starting_letters

    words_copy = frozenset(LetterBoxWord(word) for word in words)
    starting_words = frozenset(word for word in words_copy if _starts(word))
    if not starting_words:
        return

    set_to_cover = frozenset(letters_to_cover)

    phrase_length = 0
    while phrase_length < len(words):
        phrase_length += 1
        found_any_phrase = False
        for word in starting_words:
            for phrase in _generate_phrases(words_copy, phrase_length, word):
                # Only return phrases which require EVERY word to achieve coverage.
                # (Any shorter phrase which works can be vacuously made longer by appending words.)
                if set_to_cover <= set(
                    letter for word in phrase[:-1] for letter in word.letters
                ):
                    continue
                found_any_phrase = True
                if set_to_cover <= set(
                    letter for word in phrase for letter in word.letters
                ):
                    yield [w.value for w in phrase]

        if not found_any_phrase:
            break


if __name__ == "__main__":
    with open("/usr/share/dict/words", "r", encoding="utf-8") as f:
        dictionary_words = [l.strip() for l in f if len(l.strip()) >= 3]

    _sides = ["wvt", "for", "eld", "aig"]
    _valid_words = list(find_valid_words(dictionary_words, _sides))
    _phrases = find_phrases(_valid_words, "".join(_sides))
    print(next(_phrases))
