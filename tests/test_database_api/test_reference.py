import pytest

from catena_vetus.database_api.code_verse import reference

from catena_vetus.database_api.errors import (
    BookNotFoundError,
    ReferenceStyleNotRecognisedError,
)


@pytest.mark.parametrize(
    "ref,parsed",
    [
        ("Ecclesiastes 3:1", ("ecclesiastes", 3000001, 3000001)),
        ("Genesis 1:1", ("genesis", 1000001, 1000001)),
        ("Song of Solomon 1:1", ("songofsolomon", 1000001, 1000001)),
    ],
)
def test_correct_references(ref, parsed):
    assert reference(ref) == parsed


@pytest.mark.parametrize(
    "incorrect_reference", ["Jon 1", "Jack 3:16", "Test 3:1-16", "Not 1:1-2:16"]
)
def test_incorrect_book_names(incorrect_reference):
    with pytest.raises(BookNotFoundError):
        reference(incorrect_reference)


@pytest.mark.parametrize(
    "abbreviated_ref,parsed",
    [
        ("Mk 3:16", ("mark", 3000016, 3000016)),
        ("Mt 3:16-17", ("matthew", 3000016, 3000017)),
    ],
)
def test_correct_abbreviations(abbreviated_ref, parsed):
    assert reference(abbreviated_ref) == parsed


@pytest.mark.parametrize(
    "alternative_ref,parsed",
    [
        ("Song of Songs 1:1", ("songofsolomon", 1000001, 1000001)),
        ("Qoheleth 3:1", ("ecclesiastes", 3000001, 3000001)),
        ("Apocalypse 3:1", ("revelation", 3000001, 3000001)),
        ("III John 1:1", ("3john", 1000001, 1000001)),
    ],
)
def test_correct_alternatives(alternative_ref, parsed):
    assert reference(alternative_ref) == parsed


@pytest.mark.parametrize(
    "lowercase_ref,parsed",
    [
        ("mark 3:16", ("mark", 3000016, 3000016)),
        ("iii john 1:1", ("3john", 1000001, 1000001)),
    ],
)
def test_lowercase_names(lowercase_ref, parsed):
    assert reference(lowercase_ref) == parsed


@pytest.mark.parametrize(
    "range_ref,parsed",
    [
        ("Mark 3:16-17", ("mark", 3000016, 3000017)),
        ("Mark 3:16-14:17", ("mark", 3000016, 14000017)),
        ("Mark 3:16-17", ("mark", 3000016, 3000017)),
    ],
)
def test_range_references(range_ref, parsed):
    assert reference(range_ref) == parsed


def test_with_range_wrong_way_around():
    assert reference("Mark 3:16-14") == ("mark", 3000014, 3000016)


def test_with_grammatically_correct_nonexistant_verse():
    assert reference("Mark 900000:9321") == ("mark", 900000009321, 900000009321)


@pytest.mark.parametrize("illegal_ref", ["Mark", "jon", "John3:16"])
def test_with_grammatically_incorrect_raises_style_not_recognised(illegal_ref):
    with pytest.raises(ReferenceStyleNotRecognisedError):
        reference(illegal_ref)
