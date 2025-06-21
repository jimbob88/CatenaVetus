from typing import List

from catena_vetus.database_api.code_verse import (
    verse_id_range_to_str,
    normalize_book_name,
)
from catena_vetus.database_api.commentary_objects import Commentary
from string import Template

COMMENTARY_MARKDOWN_TEMPLATE = """
# [$year] [$author_name]($wiki_url) on $book $verse_range
$commentary
$source
""".strip()


def commentary_year(commentary: Commentary) -> str:
    if 0 < commentary.ts < 9999999:
        return f"AD {commentary.ts}"

    if commentary.ts < 0:
        return f"{commentary.ts} BC"

    return "Unknown Year"


def commentary_author(commentary: Commentary) -> str:
    author = commentary.father_name.strip()

    if commentary.append_to_author_name.strip():
        author += f" {commentary.append_to_author_name.strip()}"

    return author


def commentary_to_markdown(
    commentary: Commentary, markdown_template: str = COMMENTARY_MARKDOWN_TEMPLATE
) -> str:
    template = Template(markdown_template)
    return template.substitute(
        year=commentary_year(commentary),
        author_name=commentary_author(commentary),
        wiki_url=commentary.wiki_url,
        book=normalize_book_name(commentary.book),
        verse_range=verse_id_range_to_str(
            commentary.location_start, commentary.location_end
        ),
        commentary=commentary.txt,
        source=f"`{commentary.source_title}`" if commentary.source_title else "",
    )


def commentaries_to_markdown(commentaries: List[Commentary]) -> str:
    mkdown = []
    for commentary in commentaries:
        mkdown.extend(
            (
                commentary_to_markdown(commentary),
                "\n\n ---",
            )
        )
    return "\n".join(mkdown)
