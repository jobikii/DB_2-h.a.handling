from db import get_connection


def generate_data(doc_count, archive_count, signer_count):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT COALESCE(MAX(archive_id), 0) FROM archive")
        arch_start = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO archive (archive_id, adress, public_state, ownership)
            SELECT %s + gs,
                   (ARRAY['м. Київ','м. Львів','м. Одеса','м. Івано-Франківськ','м. Бурштин'])[1 + floor(random()*5)::int],
                   random() < 0.7,
                   (ARRAY['державний','приватний'])[1 + floor(random()*2)::int]
            FROM generate_series(1, %s) AS gs
        """, (arch_start, archive_count))

        cur.execute("SELECT COALESCE(MAX(signer_id), 0) FROM signer")
        sig_start = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO signer (signer_id, fullname, signer_role)
            SELECT %s + gs,
                   (ARRAY['Оленка','Іванка','Йосип','Ждан','Перислав'])[1 + floor(random()*5)::int]
                   || ' ' || (ARRAY['Пайтоненко','Петренко','Шевченко','Селенко','Бобер'])[1 + floor(random()*5)::int],
                   (ARRAY['нотаріус','писар','секретар','керівник'])[1 + floor(random()*4)::int]
            FROM generate_series(1, %s) AS gs
        """, (sig_start, signer_count))

        cur.execute("SELECT COALESCE(MAX(doc_id), 0) FROM document")
        doc_start = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO document (doc_id, sign_date, doc_type, didgitalization, archive_id)
            SELECT %s + gs,
                   (DATE '1900-01-01' + floor(random() * 45000)::integer),
                   (ARRAY['закон','указ','лист','протокол','акт'])[1 + floor(random()*5)::int],
                   random() < 0.5,
                   (SELECT archive_id FROM archive ORDER BY random() LIMIT 1)
            FROM generate_series(1, %s) AS gs
        """, (doc_start, doc_count))

        cur.execute("""
            INSERT INTO signer_document (signer_signer_id, document_doc_id)
            SELECT DISTINCT sg.ids[1 + floor(random() * array_length(sg.ids, 1))::int], d.doc_id
            FROM document d
            CROSS JOIN generate_series(1, 2) AS k
            CROSS JOIN (SELECT array_agg(signer_id) AS ids FROM signer) AS sg
            WHERE d.doc_id > %s
        """, (doc_start,))