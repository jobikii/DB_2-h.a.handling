from datetime import date


class View:
    MAIN_MENU = [
        ("1", "Archives"),
        ("2", "Documents"),
        ("3", "Signers"),
        ("4", "Signer-document"),
        ("5", "Search"),
        ("6", "Generation"),
    ]

    ARCHIVE_MENU = [
        ("1", "Show all archives"),
        ("2", "Add archive"),
        ("3", "Update archive"),
        ("4", "Delete archive"),
    ]

    DOCUMENT_MENU = [
        ("1", "Show all documents"),
        ("2", "Add document"),
        ("3", "Update document"),
        ("4", "Delete document"),
    ]

    SIGNER_MENU = [
        ("1", "Show all signers"),
        ("2", "Add signer"),
        ("3", "Update signer"),
        ("4", "Delete signer"),
    ]

    LINK_MENU = [
        ("1", "Show all links"),
        ("2", "Add link"),
        ("3", "Delete link"),
    ]

    SEARCH_MENU = [
        ("1", "Documents"),
        ("2", "Archives"),
        ("3", "Signers"),
    ]

    GENERATION_MENU = [
        ("1", "Generate test data"),
    ]

    def show_submenu(self, title, options, back_label="Back"):
        print(f"\n=== {title} ===")
        for key, label in options:
            print(f"{key}. {label}")
        print(f"0. {back_label}")
        return input("Choose an option: ").strip()

    def show_message(self, text):
        print(text)

    def show_error(self, text):
        print(f"error: {text}")

    def ask_text(self, prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("this field cannot be empty")

    def ask_int(self, prompt):
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("enter a whole number")

    def ask_date(self, prompt):
        while True:
            raw = input(prompt).strip()
            try:
                return date.fromisoformat(raw)
            except ValueError:
                print("invalid date or date format")

    def ask_yes_no(self, prompt):
        return input(prompt).strip().lower() == "y"

    def _ask_count(self, prompt):
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return 0
            if raw.isdigit():
                return int(raw)
            print("enter a non-negative whole number")

    def ask_optional_text(self, prompt):
        return input(prompt).strip() or None

    def ask_optional_date(self, prompt):
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            try:
                return date.fromisoformat(raw)
            except ValueError:
                print("invalid date or date format")

    def ask_optional_yes_no(self, prompt):
        while True:
            raw = input(prompt).strip().lower()
            if raw == "":
                return None
            if raw in ("y", "n"):
                return raw == "y"
            print("enter y/n")

    def ask_optional_int(self, prompt, default):
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return default
            if raw.isdigit():
                return int(raw)
            print("enter a non-negative whole number, or press Enter to use the default")

    def get_archive_input(self):
        archive_id = self.ask_int("archive ID: ")
        adress = self.ask_text("address: ")
        public_state = self.ask_yes_no("public (y/n): ")
        ownership = self.ask_text("ownership: ")
        return archive_id, adress, public_state, ownership

    def show_archives(self, archives):
        if not archives:
            print("no archives found")
            return
        print("\narchives:")
        for archive_id, adress, public_state, ownership in archives:
            print(f"ID: {archive_id}, address: {adress}, public: {public_state}, ownership: {ownership}")

    def get_document_input(self):
        doc_id = self.ask_int("document ID: ")
        sign_date = self.ask_date("sign date (yyyy-mm-dd): ")
        doc_type = self.ask_text("document type: ")
        digitalized = self.ask_yes_no("digitalized? (y/n): ")
        archive_id = self.ask_int("archive ID: ")
        return doc_id, sign_date, doc_type, digitalized, archive_id

    def show_documents(self, documents):
        if not documents:
            print("no documents found")
            return
        print("\ndocuments:")
        for doc_id, sign_date, doc_type, digitalized, archive_id in documents:
            print(f"ID: {doc_id}, date: {sign_date}, type: {doc_type}, "
                  f"digitalized: {digitalized}, archive ID: {archive_id}")

    def get_generate_counts(self):
        doc_count = self._ask_count("enter documents amount: ")
        archive_count = self._ask_count("enter archives amount: ")
        signer_count = self._ask_count("enter signers amount: ")
        return doc_count, archive_count, signer_count

    def show_table(self, headers, rows, elapsed_ms):
        if not rows:
            print("no results found")
        else:
            print("\n" + " | ".join(headers))
            print("-" * 70)
            for row in rows:
                print(" | ".join(str(value) for value in row))
        print(f"Rows: {len(rows)}, query time: {elapsed_ms:.2f} ms")

    def get_signer_input(self):
        signer_id = self.ask_int("signer ID: ")
        fullname = self.ask_text("full name: ")
        signer_role = self.ask_text("role: ")
        return signer_id, fullname, signer_role

    def show_signers(self, signers):
        if not signers:
            print("no signers found")
            return
        print("\nsigners:")
        for signer_id, fullname, signer_role in signers:
            print(f"ID: {signer_id}, name: {fullname}, role: {signer_role}")