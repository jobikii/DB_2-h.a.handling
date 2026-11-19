import time
import psycopg
from models.generator_model import generate_data
from models.archive_model import get_all_archives, add_archive, update_archive, delete_archive
from models.document_model import get_all_documents, add_document, update_document, delete_document
from models.search_model import search_documents, search_archives_with_counts, search_signers
from models.signer_model import get_all_signers, add_signer, update_signer, delete_signer
from models.signer_document_model import get_all_links, add_link, delete_link
from view import View


class Controller:
    def __init__(self):
        self.view = View()

        self.main_handlers = {
            "1": self.archive_menu,
            "2": self.document_menu,
            "3": self.signer_menu,
            "4": self.link_menu,
            "5": self.search_menu,
            "6": self.generation_menu,
        }

        self.archive_handlers = {
            "1": self.archive_show,
            "2": self.archive_add,
            "3": self.archive_update,
            "4": self.archive_delete,
        }

        self.document_handlers = {
            "1": self.document_show,
            "2": self.document_add,
            "3": self.document_update,
            "4": self.document_delete,
        }

        self.signer_handlers = {
            "1": self.signer_show,
            "2": self.signer_add,
            "3": self.signer_update,
            "4": self.signer_delete,
        }

        self.link_handlers = {
            "1": self.link_show,
            "2": self.link_add,
            "3": self.link_delete,
        }
        
        self.search_handlers = {
            "1": self.search_documents_action,
            "2": self.search_archives_action,
            "3": self.search_signers_action,
        }

        self.generation_handlers = {
            "1": self.generate_test_data,
        }

    def run(self):
        self._run_menu("Main Menu", View.MAIN_MENU, self.main_handlers, back_label="Exit")
        print("\n/// session ended ///\n")

    def _run_menu(self, title, options, handlers, back_label="Back"):
        while True:
            choice = self.view.show_submenu(title, options, back_label)
            if choice == "0":
                return
            handler = handlers.get(choice)
            if handler is None:
                self.view.show_message("unknown option")
                continue
            self._safe_call(handler)

    def _safe_call(self, action):
        try:
            action()
        except ValueError:
            self.view.show_error("invalid input")
        except psycopg.errors.UniqueViolation:
            self.view.show_error("record with this ID already exists")
        except psycopg.errors.ForeignKeyViolation:
            self.view.show_error("the operation conflicts with related records")
        except psycopg.errors.NotNullViolation:
            self.view.show_error("required field is missing")
        except psycopg.errors.DataError:
            self.view.show_error("one of the values is out of range or in the wrong format")
        except psycopg.OperationalError:
            self.view.show_error("cannot reach the database, check that PostgreSQL is running")
        except psycopg.Error as e:
            self.view.show_error(f"database operation failed (SQLSTATE {e.sqlstate})")

    def archive_menu(self):
        self._run_menu("Archives", View.ARCHIVE_MENU, self.archive_handlers)

    def document_menu(self):
        self._run_menu("Documents", View.DOCUMENT_MENU, self.document_handlers)

    def signer_menu(self):
        self._run_menu("Signers", View.SIGNER_MENU, self.signer_handlers)

    def link_menu(self):
        self._run_menu("Signer-document", View.LINK_MENU, self.link_handlers)

    def search_menu(self):
        self._run_menu("Search", View.SEARCH_MENU, self.search_handlers)

    def generation_menu(self):
        self._run_menu("Generation", View.GENERATION_MENU, self.generation_handlers)

    def archive_show(self):
        self.view.show_archives(get_all_archives())

    def archive_add(self):
        archive = self.view.get_archive_input()
        add_archive(*archive)
        self.view.show_message("archive added")

    def archive_update(self):
        archive = self.view.get_archive_input()
        if update_archive(*archive):
            self.view.show_message("archive updated")
        else:
            self.view.show_error("no archive with this ID")

    def archive_delete(self):
        archive_id = self.view.ask_int("archive ID to delete: ")
        try:
            deleted = delete_archive(archive_id)
        except psycopg.errors.ForeignKeyViolation:
            self.view.show_error("this archive has documents and cannot be deleted")
            return
        if deleted:
            self.view.show_message("archive deleted")
        else:
            self.view.show_error("no archive with this ID")

    def document_show(self):
        self.view.show_documents(get_all_documents())

    def document_add(self):
        document = self.view.get_document_input()
        try:
            add_document(*document)
        except psycopg.errors.ForeignKeyViolation:
            self.view.show_error("no archive with this ID, add the archive first")
            return
        self.view.show_message("document added")

    def document_update(self):
        document = self.view.get_document_input()
        try:
            updated = update_document(*document)
        except psycopg.errors.ForeignKeyViolation:
            self.view.show_error("mo archive with this ID")
            return
        if updated:
            self.view.show_message("document updated")
        else:
            self.view.show_error("no document with this ID")

    def document_delete(self):
        doc_id = self.view.ask_int("document ID to delete: ")
        try:
            deleted = delete_document(doc_id)
        except psycopg.errors.ForeignKeyViolation:
            self.view.show_error(
                "this document is linked to signers and cannot be deleted"
                "remove the links first."
            )
            return
        if deleted:
            self.view.show_message("document deleted")
        else:
            self.view.show_error("no document with this ID")

    def generate_test_data(self):
        doc_count, archive_count, signer_count = self.view.get_generate_counts()
        if doc_count <= 0:
            self.view.show_error("enter a number of documents > 0")
            return

        start = time.perf_counter()
        generate_data(doc_count, archive_count, signer_count)
        elapsed_ms = (time.perf_counter() - start) * 1000

        self.view.show_message(
            f"generated {doc_count} documents, {archive_count} archives, {signer_count} signers"
            f"{signer_count} signers in {elapsed_ms:.0f} ms."
        )


    def search_documents_action(self):
        date_from = self.view.ask_optional_date("sign date from (yyyy-mm-dd): ")
        date_to = self.view.ask_optional_date("sign date to (yyyy-mm-dd): ")
        if date_from and date_to and date_from > date_to:
            self.view.show_error("start date must be before the end date")
            return
        doc_type = self.view.ask_optional_text("document type (part of the name): ")
        digitalized = self.view.ask_optional_yes_no("digitalized? (y/n): ")
        limit = self.view.ask_int("max rows: ")
        if limit <= 0:
            self.view.show_error("enter a number greater than 0.")
            return

        pattern = f"%{doc_type}%" if doc_type else "%"
        rows, elapsed_ms = search_documents(date_from, date_to, pattern, digitalized, limit)
        self.view.show_table(
            ["doc ID", "sign date", "type", "digitalized", "archive ID", "address"],
            rows, elapsed_ms,
        )

    def search_archives_action(self):
        ownership = self.view.ask_optional_text("ownership (part of the name): ")
        min_docs = self.view.ask_optional_int("minimum number of documents: ", default=0)

        pattern = f"%{ownership}%" if ownership else "%"
        rows, elapsed_ms = search_archives_with_counts(pattern, min_docs)
        self.view.show_table(
            ["archive ID", "address", "ownership", "documents"], rows, elapsed_ms
        )

    def search_signers_action(self):
        name = self.view.ask_optional_text("name (part of the name): ")
        role = self.view.ask_optional_text("role (part of the word): ")

        name_pattern = f"%{name}%" if name else "%"
        role_pattern = f"%{role}%" if role else "%"
        rows, elapsed_ms = search_signers(name_pattern, role_pattern)
        self.view.show_table(
            ["signer ID", "full name", "role", "documents"], rows, elapsed_ms
        )

    def signer_show(self):
        self.view.show_signers(get_all_signers())

    def signer_add(self):
        signer = self.view.get_signer_input()
        add_signer(*signer)
        self.view.show_message("signer added")

    def signer_update(self):
        signer = self.view.get_signer_input()
        if update_signer(*signer):
            self.view.show_message("signer updated")
        else:
            self.view.show_error("no signer with this ID")

    def signer_delete(self):
        signer_id = self.view.ask_int("signer ID to delete: ")
        try:
            deleted = delete_signer(signer_id)
        except psycopg.errors.ForeignKeyViolation:
            self.view.show_error(
                "this signer is linked to documents and cannot be deleted"
                "remove the links first"
            )
            return
        if deleted:
            self.view.show_message("signer deleted")
        else:
            self.view.show_error("no signer with this ID")

    def link_show(self):
        rows, elapsed_ms = get_all_links()
        self.view.show_table(
            ["signer ID", "full name", "doc ID", "doc type"], rows, elapsed_ms
        )

    def link_add(self):
        signer_id = self.view.ask_int("signer ID: ")
        doc_id = self.view.ask_int("document ID: ")
        try:
            add_link(signer_id, doc_id)
        except psycopg.errors.UniqueViolation:
            self.view.show_error("this signer is already linked to this document")
            return
        except psycopg.errors.ForeignKeyViolation:
            self.view.show_error("no signer or document with this ID")
            return
        self.view.show_message("link added")

    def link_delete(self):
        signer_id = self.view.ask_int("signer ID: ")
        doc_id = self.view.ask_int("document ID: ")
        if delete_link(signer_id, doc_id):
            self.view.show_message("link deleted")
        else:
            self.view.show_error("no link between this signer and this document")