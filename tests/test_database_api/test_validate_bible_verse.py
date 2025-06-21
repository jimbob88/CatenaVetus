import pytest

from catena_vetus.database_api.code_verse import validate_bible_verse


@pytest.mark.parametrize(
    "ref",
    ["John 3", "John 3:16", "Genesis 1:1", "1 Samuel 1:12", "1 Kgs 1:3", "1 Cor 1:1"],
)
def test_valid_references(ref):
    assert validate_bible_verse(ref)


@pytest.mark.parametrize(
    "invalid_ref",
    ["John", "1 Samuel ", "1 Samuel:", "1 Samuel1:1"],
)
def test_invalid_references(invalid_ref):
    assert not validate_bible_verse(invalid_ref)


def test_grammatically_correct_references():
    """Tests that books which do not exist still follow a valid reference format."""
    assert validate_bible_verse("Super Secret Book Name Gnostics Probably Believe 3:1")
