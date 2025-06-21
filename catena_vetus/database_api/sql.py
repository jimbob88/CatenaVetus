# ""
import sqlite3
from typing import List

from catena_vetus.database_api.commentary_objects import Commentary

sql_function = """SELECT c.*,fm.wiki_url FROM commentary c LEFT JOIN father_meta fm ON c.father_name=fm.name
WHERE c.book=(?) and
c.location_end >= (?) and
c.location_start <= (?)
ORDER BY c.ts ASC, c.location_start ASC;"""


def commentaries(
    sql_conn: sqlite3.Connection, book_name: str, start_id: int, end_id: int
) -> List[Commentary]:
    """
    The following SQL is taken directly from Historical Christian Faith:
    SELECT c.*,fm.wiki_url FROM commentary c LEFT JOIN father_meta fm ON c.father_name=fm.name
    WHERE c.book=(:book) and
    c.location_end >= (:location_start) and
    c.location_start <= (:location_end)
    ORDER BY c.ts ASC, c.location_start ASC

    :param book_name: The title of the book, in the format of the database i.e. genesis, mark, john, revelation
    :param start_id: 11000011
    :param end_id: 15000008
    :return:
    """
    curr = sql_conn.cursor()
    curr.execute(sql_function, (book_name, start_id, end_id))

    return [Commentary(*row) for row in curr.fetchall()]
