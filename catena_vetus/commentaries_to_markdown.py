from typing import List

from catena_vetus.database_api.code_verse import verse_id_range_to_str, normalize_book_name
from catena_vetus.database_api.commentary_objects import Commentary


def commentaries_to_markdown(commentaries: List[Commentary]) -> str:
    mkdown = []
    for commentary in commentaries:
        title = ""
        if 0 < commentary.ts < 9999999:
            title += f"# [AD {commentary.ts}]"
        elif commentary.ts < 0:
            title += f"# [{commentary.ts} BC]"
        else:
            title += "# [Unknown Year]"

        title += f" [{commentary.father_name.strip()}"

        if commentary.append_to_author_name.strip():
            title += f" {commentary.append_to_author_name.strip()}"
        title += f"]({commentary.wiki_url})"

        title += f" on {normalize_book_name(commentary.book)} {verse_id_range_to_str(commentary.location_start, commentary.location_end)}"

        mkdown.extend((title, commentary.txt, f"`{commentary.source_title}`" if commentary.source_title else "", "\n\n ---"))
    return "\n".join(mkdown)
