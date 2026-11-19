from db import get_connection


def get_all_signers():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT signer_id, fullname, signer_role "
            "FROM signer ORDER BY signer_id"
        )
        return cur.fetchall()


def add_signer(signer_id, fullname, signer_role):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO signer (signer_id, fullname, signer_role) "
            "VALUES (%s, %s, %s)",
            (signer_id, fullname, signer_role),
        )


def update_signer(signer_id, fullname, signer_role):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE signer SET fullname = %s, signer_role = %s "
            "WHERE signer_id = %s",
            (fullname, signer_role, signer_id),
        )
        return cur.rowcount


def delete_signer(signer_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM signer WHERE signer_id = %s", (signer_id,))
        return cur.rowcount