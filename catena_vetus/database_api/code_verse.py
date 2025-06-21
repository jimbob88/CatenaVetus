"""
Code for encoding/decoding references.
"""

import re
from typing import NamedTuple, Tuple

from catena_vetus.database_api.abbreviations import alt_to_fullname
from catena_vetus.database_api.errors import BookNotFoundError, ReferenceStyleNotRecognisedError


class VerseRange(NamedTuple):
    start_chapter: int
    start_verse: int
    end_chapter: int
    end_verse: int


def string_to_verse_range(verse_string: str) -> VerseRange:
    """

    :param verse_string: A verse string i.e. 1:57-58 or 1:57-2:32
    :return:
    """
    verse_pieces = re.split(r'[:-]', verse_string)
    start_chapter = verse_pieces[0]
    start_verse = verse_pieces[1]
    if len(verse_pieces) == 2:
        # i.e. 1_56
        end_chapter = start_chapter
        end_verse = start_verse
    elif len(verse_pieces) == 3:
        # i.e. 1_57-57
        end_chapter = start_chapter
        end_verse = verse_pieces[2]
    elif len(verse_pieces) == 4:
        # i.e. 1_57-2_32
        end_chapter = verse_pieces[2]
        end_verse = verse_pieces[3]
    else:
        raise ValueError(f'Unexpected format of verse_string: {verse_string}')

    return VerseRange(
        start_chapter=int(start_chapter),
        start_verse=int(start_verse),
        end_chapter=int(end_chapter),
        end_verse=int(end_verse)
    )


def encode_chapter_verse(chapter: int, verse: int) -> int:
    return (chapter * 1000000) + verse


def reference(verse: str) -> Tuple[str, int, int]:
    """

    :param verse: i.e. John 1:13 or John 1:13-14 or 1 Jn 1:4-2:1
    :return: book name, start id, end id
    """
    verse = verse.strip()
    if not validate_bible_verse(verse):
        raise ReferenceStyleNotRecognisedError(f"{verse} did not conform to standard reference style BookName ChapNum[:VerseNum][-ChapNum:VerseNum]")

    # if selecting a whole chapter
    if ":" not in verse:
        verse += ":1-99999"

    book_name = " ".join(verse.split(' ')[:-1])
    if book_name.lower() not in alt_to_fullname:
        raise BookNotFoundError(f"Book `{book_name}` not found, please check `abbreviations.py` for available names.")
    db_name = alt_to_fullname[book_name.lower()].lower().replace(' ', '')

    chap_v = verse.split(' ')[-1]
    verse_range = string_to_verse_range(chap_v)

    start_verse = encode_chapter_verse(verse_range.start_chapter, verse_range.start_verse)
    end_verse = encode_chapter_verse(verse_range.end_chapter, verse_range.end_verse)
    if start_verse > end_verse:
        return db_name, end_verse, start_verse
    return db_name, start_verse, end_verse


def decode_chapter_verse(chap_verse: int) -> Tuple[int, int]:
    chapter = int(str(chap_verse)[:-6])
    verse = int(str(chap_verse)[-6:])
    return chapter, verse


def verse_range_to_str(start_chap: int, start_verse: int, end_chap: int, end_verse: int) -> str:
    """Takes for example 1:2 to 3:4 and returns 1:2-3:4. Or 1:1 to 1:2 and returns 1:1-2 [A normative function]"""
    if start_chap != end_chap:
        return f"{start_chap}:{start_verse}-{end_chap}:{end_verse}"

    if start_verse == end_verse:
        return f"{start_chap}:{start_verse}"

    return f"{start_chap}:{start_verse}-{end_verse}"


def verse_id_range_to_str(start_id: int, end_id: int) -> str:
    """Takes something like 13000001 to 13000002 and returns 13:1-2 [A normative function]"""
    start_chap, start_verse = decode_chapter_verse(start_id)
    end_chap, end_verse = decode_chapter_verse(end_id)
    return verse_range_to_str(start_chap, start_verse, end_chap, end_verse)


def normalize_book_name(abbr_name: str) -> str:
    """i.e. converts john -> John"""
    return alt_to_fullname[abbr_name]


def validate_bible_verse(verse: str):
    """
    Credit: https://regex101.com/library/fS3wA0 https://regex101.com/library/wX7nO0
    :return:
    """
    bible_verse_re = r"(.*?)\s(\d{1,2})(?::(\d{1,2})(?:-(\d{1,2})?)?)?"
    return re.match(bible_verse_re, verse)
