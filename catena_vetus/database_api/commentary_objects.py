from typing_extensions import NamedTuple


class Commentary(NamedTuple):
    id: str
    father_name: str
    file_name: str
    append_to_author_name: str
    ts: int  # Year
    book: str
    location_start: int
    location_end: int
    txt: str
    source_url: str
    source_title: str
    wiki_url: str
