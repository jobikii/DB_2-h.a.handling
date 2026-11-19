import time
from db import get_connection


def get_all_links():
    start = time.perf_counter()
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT s.signer_id, s.fullname, d.doc_id, d.doc_type
            FROM signer_document sd
            JOIN signer s ON s.signer_id = sd.signer_signer_id
            JOIN document d ON d.doc_id = sd.document_doc_id
            ORDER BY d.doc_id, s.signer_id
            """
        )
        rows = cur.fetchall()
    return rows, (time.perf_counter() - start) * 1000


def add_link(signer_id, doc_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO signer_document (signer_signer_id, document_doc_id) VALUES (%s, %s)",
            (signer_id, doc_id),
        )


def delete_link(signer_id, doc_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "DELETE FROM signer_document WHERE signer_signer_id = %s AND document_doc_id = %s",
            (signer_id, doc_id),
        )
        return cur.rowcount > 0