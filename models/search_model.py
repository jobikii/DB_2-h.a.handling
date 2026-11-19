import time

from db import get_connection


def _run(sql, params):
    with get_connection() as conn, conn.cursor() as cur:
        start = time.perf_counter()
        cur.execute(sql, params)
        rows = cur.fetchall()
        elapsed_ms = (time.perf_counter() - start) * 1000
    return rows, elapsed_ms


def search_documents(date_from, date_to, doc_type_pattern, digitalized, limit):
    sql = """
        SELECT d.doc_id, d.sign_date, d.doc_type, d.didgitalization,
               a.archive_id, a.adress
        FROM document AS d
        JOIN archive AS a ON a.archive_id = d.archive_id
        WHERE (%s::date IS NULL OR d.sign_date >= %s::date)
          AND (%s::date IS NULL OR d.sign_date < %s::date + INTERVAL '1 day')
          AND d.doc_type ILIKE %s
          AND (%s::boolean IS NULL OR d.didgitalization = %s::boolean)
        ORDER BY d.sign_date
        LIMIT %s
    """
    params = (
        date_from, date_from,
        date_to, date_to,
        doc_type_pattern,
        digitalized, digitalized,
        limit,
    )
    return _run(sql, params)


def search_archives_with_counts(ownership_pattern, min_docs):
    sql = """
        SELECT a.archive_id, a.adress, a.ownership, COUNT(d.doc_id) AS doc_count
        FROM archive AS a
        LEFT JOIN document AS d ON d.archive_id = a.archive_id
        WHERE a.ownership ILIKE %s
        GROUP BY a.archive_id, a.adress, a.ownership
        HAVING COUNT(d.doc_id) >= %s
        ORDER BY doc_count DESC, a.archive_id
    """
    return _run(sql, (ownership_pattern, min_docs))


def search_signers(name_pattern, role_pattern):
    sql = """
        SELECT s.signer_id, s.fullname, s.signer_role,
        COUNT(sd.document_doc_id) AS doc_count
        FROM signer AS s
        LEFT JOIN signer_document AS sd ON sd.signer_signer_id = s.signer_id
        WHERE s.fullname ILIKE %s
        AND s.signer_role ILIKE %s
        GROUP BY s.signer_id, s.fullname, s.signer_role
        ORDER BY s.fullname
    """
    return _run(sql, (name_pattern, role_pattern))