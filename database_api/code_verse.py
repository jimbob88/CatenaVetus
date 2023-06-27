"""
Code for encoding/decoding references.
"""

import re
from typing import Dict, NamedTuple, Tuple

# https://catholic-resources.org/Bible/Abbreviations-Abreviaciones.htm
# Abbreviations and alternative names
abbr_and_alt = {
    "Genesis": ["Gen"],
    "Exodus": ["Exod"],
    "Leviticus": ["Lev"],
    "Numbers": ["Num"],
    "Deuteronomy": ["Deut"],
    "Joshua": ["Josh"],
    "Judges": ["Judg"],
    "Ruth": ["Ruth"],
    "1 Samuel": ["1 Sam"],
    "2 Samuel": ["2 Sam"],
    "1 Kings": ["1 Kgs"],
    "2 Kings": ["2 Kgs"],
    "1 Chronicles": ["1 Chr"],
    "2 Chronicles": ["2 Chr"],
    "Ezra": ["Ezra"],
    "Nehemiah": ["Neh"],
    "Tobit": ["Tob"],
    "Judith": ["Jud"],
    "Esther": ["Esth"],
    "1 Maccabees": ["1 Macc"],
    "2 Maccabees": ["2 Macc"],
    "Job": ["Job"],
    "Psalms": ["Ps"],
    "Proverbs": ["Prov"],
    "Ecclesiastes": ["Eccel", "Qoheleth", "Qoh"],
    "Song of Solomon": ["Song", "Song of Songs", "Canticle of Canticles", "Cant"],
    "Wisdom": ["Wisdom of Solomon", "Wis"],
    "Sirach": ["Sir", "Ecclesiasticus", "Ecclus"],
    "Isaiah": ["Isa"],
    "Jeremiah": ["Jer"],
    "Lamentations": ["Lam"],
    "Baruch": ["Bar"],
    "Ezekiel": ["Ezek"],
    "Daniel": ["Dan"],
    "Hosea": ["Hos"],
    "Joel": ["Joel"],
    "Amos": ["Amos"],
    "Obadiah": ["Obad"],
    "Jonah": ["Jonah"],
    "Micah": ["Mic"],
    "Nahum": ["Nah"],
    "Habakkuk": ["Hab"],
    "Zephaniah": ["Zeph"],
    "Haggai": ["Hag"],
    "Zechariah": ["Zech"],
    "Malachi": ["Mal"],
    "Matthew": ["Matt", "Mat", "Mt"],
    "Mark": ["Mark", "Mk"],
    "Luke": ["Luke", "Lu", "Lk"],
    "John": ["John", "Jn"],
    "Acts": ["Acts of the Apostles", "Acts"],
    "Romans": ["Rom"],
    "1 Corinthians": ["1 Cor"],
    "2 Corinthians": ["2 Cor"],
    "Galatians": ["Gal"],
    "Ephesians": ["Eph"],
    "Philippians": ["Phil"],
    "Colossians": ["Col"],
    "1 Thessalonians": ["1 Thess"],
    "2 Thessalonians": ["2 Thess"],
    "1 Timothy": ["1 Tim"],
    "2 Timothy": ["2 Tim"],
    "Titus": ["Titus"],
    "Philemon": ["Phlm", "Philem"],
    "Hebrews": ["Heb"],
    "James": ["Jas"],
    "1 Peter": ["1 Pet", "1 Pt"],
    "2 Peter": ["2 Pet", "2 Pt"],
    "1 John": ["1 John", "1 Jn"],
    "2 John": ["2 John", "2 Jn"],
    "3 John": ["3 John", "3 Jn"],
    "Jude": ["Jude"],
    "Revelation": ["Rev", "Apocalypse", "Apoc"]
}

# Allows you to reverse Mk -> Mark
alt_to_database: Dict[str, str] = {
    alt_name: database_name
    for database_name, alt_names in abbr_and_alt.items()
    for alt_name in alt_names
}


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
    verse_pieces = re.split('[:-]', verse_string)
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
    # if selecting a whole chapter
    if ":" not in verse:
        verse += ":1-99999"

    book_name = " ".join(verse.split(' ')[:-1])
    db_name = alt_to_database[book_name].lower().replace(' ', '')

    chap_v = verse.split(' ')[-1]
    verse_range = string_to_verse_range(chap_v)

    start_verse = encode_chapter_verse(verse_range.start_chapter, verse_range.start_verse)
    end_verse = encode_chapter_verse(verse_range.end_chapter, verse_range.end_verse)
    return db_name, start_verse, end_verse
