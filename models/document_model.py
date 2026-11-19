from db import get_connection


def get_all_documents():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT doc_id, sign_date, doc_type, didgitalization, archive_id "
            "FROM document ORDER BY doc_id"
        )
        return cur.fetchall()


def add_document(doc_id, sign_date, doc_type, didgitalization, archive_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO document (doc_id, sign_date, doc_type, didgitalization, archive_id) "
            "VALUES (%s, %s, %s, %s, %s)",
            (doc_id, sign_date, doc_type, didgitalization, archive_id),
        )


def update_document(doc_id, sign_date, doc_type, didgitalization, archive_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE document SET sign_date = %s, doc_type = %s, "
            "didgitalization = %s, archive_id = %s WHERE doc_id = %s",
            (sign_date, doc_type, didgitalization, archive_id, doc_id),
        )
        return cur.rowcount


def delete_document(doc_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM signer_document WHERE document_doc_id = %s", (doc_id,))
        cur.execute("DELETE FROM document WHERE doc_id = %s", (doc_id,))
        return cur.rowcount