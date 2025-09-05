"""Solve the Letter Boxed game."""

type Side = str


def find_valid_words(words: list[str], sides: list[Side]):
    yield "word"
    # TODO: yield words which:
    #       - have at least 3 letters;
    #       - use only the set of letters present in sides;
    #       - do not use two consecutive letters from the same side
    return


def find_phrases(words: list[str], letters_to_cover: str, starting_letters=None):
    # TODO
    pass


if __name__ == "__main__":
    print("hello world")
