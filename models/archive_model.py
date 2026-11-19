from db import get_connection


def get_all_archives():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT archive_id, adress, public_state, ownership "
                    "FROM archive ORDER BY archive_id")
        return cur.fetchall()


def add_archive(archive_id, adress, public_state, ownership):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO archive (archive_id, adress, public_state, ownership) "
            "VALUES (%s, %s, %s, %s)",
            (archive_id, adress, public_state, ownership),
        )

def update_archive(archive_id, adress, public_state, ownership):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE archive SET adress = %s, public_state = %s, ownership = %s "
            "WHERE archive_id = %s",
            (adress, public_state, ownership, archive_id),
        )
        return cur.rowcount


def delete_archive(archive_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM archive WHERE archive_id = %s", (archive_id,))
        return cur.rowcount
