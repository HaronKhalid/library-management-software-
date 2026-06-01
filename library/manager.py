# manager.py - Core Library Manager
# Orchestrates all library operations: books, members, loans

from library.book import Book
from library.person import Member, Librarian
from library.loan import Loan
from library import file_handler as fh


class LibraryManager:
    """
    Central manager for the Library Management System.
    Handles all CRUD operations and business logic.
    """

    def __init__(self):
        fh.ensure_data_directory()
        self._books: dict[str, Book] = {}
        self._members: dict[str, Member] = {}
        self._librarians: dict[str, Librarian] = {}
        self._loans: dict[str, Loan] = {}
        self._load_all()

    # =========================================================
    # DATA PERSISTENCE
    # =========================================================

    def _load_all(self):
        """Load all data from JSON files into memory."""
        for data in fh.load_books():
            book = Book.from_dict(data)
            self._books[book.book_id] = book

        for data in fh.load_members():
            member = Member.from_dict(data)
            self._members[member.person_id] = member

        for data in fh.load_librarians():
            lib = Librarian.from_dict(data)
            self._librarians[lib.person_id] = lib

        for data in fh.load_loans():
            loan = Loan.from_dict(data)
            self._loans[loan.loan_id] = loan

    def _save_all(self):
        """Save all in-memory data back to JSON files."""
        fh.save_books([b.to_dict() for b in self._books.values()])
        fh.save_members([m.to_dict() for m in self._members.values()])
        fh.save_librarians([l.to_dict() for l in self._librarians.values()])
        fh.save_loans([l.to_dict() for l in self._loans.values()])

    # =========================================================
    # BOOK MANAGEMENT
    # =========================================================

    def add_book(self, title: str, author: str, isbn: str,
                 category: str, total_copies: int = 1,
                 publication_year: int = None) -> Book:
        """Add a new book to the library."""
        if not title.strip() or not author.strip():
            raise ValueError("Title and author cannot be empty.")
        if total_copies < 1:
            raise ValueError("Total copies must be at least 1.")

        # Check for duplicate ISBN
        for book in self._books.values():
            if book.isbn == isbn:
                raise ValueError(f"A book with ISBN '{isbn}' already exists.")

        book_id = fh.get_next_id("book")
        book = Book(book_id, title.strip(), author.strip(),
                    isbn.strip(), category, total_copies, publication_year)
        self._books[book_id] = book
        self._save_all()
        return book

    def remove_book(self, book_id: str) -> Book:
        """Remove a book from the library (only if no active loans)."""
        book = self._get_book_or_raise(book_id)
        active = [l for l in self._loans.values()
                  if l.book_id == book_id and l.status == Loan.STATUS_ACTIVE]
        if active:
            raise ValueError(f"Cannot remove '{book.title}': it has {len(active)} active loan(s).")
        del self._books[book_id]
        self._save_all()
        return book

    def update_book(self, book_id: str, **kwargs) -> Book:
        """Update book fields (title, author, category, publication_year)."""
        book = self._get_book_or_raise(book_id)
        allowed = {"title", "author", "category", "publication_year"}
        for key, value in kwargs.items():
            if key in allowed:
                setattr(book, f"_{key}", value)
        self._save_all()
        return book

    def get_book(self, book_id: str) -> Book:
        return self._get_book_or_raise(book_id)

    def list_books(self, category: str = None, available_only: bool = False) -> list[Book]:
        """Return all books, optionally filtered by category or availability."""
        books = list(self._books.values())
        if category:
            books = [b for b in books if b.category.lower() == category.lower()]
        if available_only:
            books = [b for b in books if b.is_available()]
        return books

    def search_books(self, query: str) -> list[Book]:
        """Search books by title, author, or ISBN (case-insensitive)."""
        query = query.lower().strip()
        if not query:
            raise ValueError("Search query cannot be empty.")
        return [
            b for b in self._books.values()
            if query in b.title.lower()
            or query in b.author.lower()
            or query in b.isbn.lower()
        ]

    # =========================================================
    # MEMBER MANAGEMENT
    # =========================================================

    def register_member(self, name: str, email: str, phone: str,
                        membership_type: str = "Standard") -> Member:
        """Register a new library member."""
        self._validate_person_fields(name, email, phone)
        self._check_email_unique(email)

        member_id = fh.get_next_id("member")
        member = Member(member_id, name.strip(), email.strip(),
                        phone.strip(), membership_type)
        self._members[member_id] = member
        self._save_all()
        return member

    def remove_member(self, member_id: str) -> Member:
        """Remove a member (only if no active loans)."""
        member = self._get_member_or_raise(member_id)
        if member.active_loans:
            raise ValueError(
                f"Cannot remove '{member.name}': they have {len(member.active_loans)} active loan(s)."
            )
        del self._members[member_id]
        self._save_all()
        return member

    def get_member(self, member_id: str) -> Member:
        return self._get_member_or_raise(member_id)

    def list_members(self, active_only: bool = False) -> list[Member]:
        members = list(self._members.values())
        if active_only:
            members = [m for m in members if m.is_active]
        return members

    def search_members(self, query: str) -> list[Member]:
        """Search members by name or email."""
        query = query.lower().strip()
        if not query:
            raise ValueError("Search query cannot be empty.")
        return [
            m for m in self._members.values()
            if query in m.name.lower() or query in m.email.lower()
        ]

    def toggle_member_status(self, member_id: str) -> Member:
        """Toggle a member's active/inactive status."""
        member = self._get_member_or_raise(member_id)
        if member.is_active:
            member.deactivate()
        else:
            member.activate()
        self._save_all()
        return member

    def update_member(self, member_id: str, name: str = None, email: str = None,
                      phone: str = None, membership_type: str = None) -> Member:
        """Update member details (name, email, phone, membership_type)."""
        member = self._get_member_or_raise(member_id)

        new_name = name.strip() if name is not None else member.name
        new_email = email.strip() if email is not None else member.email
        new_phone = phone.strip() if phone is not None else member.phone
        new_m_type = membership_type.strip() if membership_type is not None else member.membership_type

        self._validate_person_fields(new_name, new_email, new_phone)

        if new_email.lower() != member.email.lower():
            self._check_email_unique(new_email)

        member.name = new_name
        member.email = new_email
        member.phone = new_phone
        member._membership_type = new_m_type

        self._save_all()
        return member

    # =========================================================
    # LIBRARIAN MANAGEMENT
    # =========================================================

    def add_librarian(self, name: str, email: str, phone: str,
                      employee_id: str, department: str = "General") -> Librarian:
        """Add a new librarian/staff member."""
        self._validate_person_fields(name, email, phone)
        self._check_email_unique(email)

        librarian_id = fh.get_next_id("librarian")
        librarian = Librarian(librarian_id, name.strip(), email.strip(),
                              phone.strip(), employee_id.strip(), department)
        self._librarians[librarian_id] = librarian
        self._save_all()
        return librarian

    def list_librarians(self) -> list[Librarian]:
        return list(self._librarians.values())

    # =========================================================
    # LOAN MANAGEMENT
    # =========================================================

    def borrow_book(self, member_id: str, book_id: str) -> Loan:
        """Process a book borrowing transaction."""
        member = self._get_member_or_raise(member_id)
        book = self._get_book_or_raise(book_id)

        if not member.is_active:
            raise ValueError(f"Member '{member.name}' account is inactive.")
        if not member.can_borrow():
            raise ValueError(
                f"Member '{member.name}' has reached the borrowing limit "
                f"({Member.MAX_BORROW_LIMIT} books)."
            )
        if not book.is_available():
            raise ValueError(f"No available copies of '{book.title}'.")

        # Check if member already has this book
        for loan in self._loans.values():
            if (loan.member_id == member_id and loan.book_id == book_id
                    and loan.status == Loan.STATUS_ACTIVE):
                raise ValueError(f"'{member.name}' already has '{book.title}' borrowed.")

        loan_id = fh.get_next_id("loan")
        loan = Loan(loan_id, member_id, book_id, book.title, member.name)

        book.borrow_copy()
        member.add_loan(loan_id)
        self._loans[loan_id] = loan
        self._save_all()
        return loan

    def return_book(self, loan_id: str) -> tuple[Loan, float]:
        """Process a book return. Returns (loan, fine_amount)."""
        loan = self._get_loan_or_raise(loan_id)

        if loan.status == Loan.STATUS_RETURNED:
            raise ValueError(f"Loan {loan_id} has already been returned.")

        book = self._get_book_or_raise(loan.book_id)
        member = self._get_member_or_raise(loan.member_id)

        loan.process_return()
        book.return_copy()
        member.remove_loan(loan_id)
        self._save_all()
        return loan, loan.fine_amount

    def get_active_loans(self) -> list[Loan]:
        return [l for l in self._loans.values() if l.status == Loan.STATUS_ACTIVE]

    def get_overdue_loans(self) -> list[Loan]:
        return [l for l in self._loans.values() if l.is_overdue()]

    def get_member_loans(self, member_id: str) -> list[Loan]:
        self._get_member_or_raise(member_id)
        return [l for l in self._loans.values() if l.member_id == member_id]

    def get_loan(self, loan_id: str) -> Loan:
        return self._get_loan_or_raise(loan_id)

    # =========================================================
    # STATISTICS
    # =========================================================

    def get_statistics(self) -> dict:
        """Return a summary of library statistics."""
        total_books = sum(b.total_copies for b in self._books.values())
        available = sum(b.available_copies for b in self._books.values())
        return {
            "total_titles": len(self._books),
            "total_copies": total_books,
            "available_copies": available,
            "borrowed_copies": total_books - available,
            "total_members": len(self._members),
            "active_members": sum(1 for m in self._members.values() if m.is_active),
            "total_librarians": len(self._librarians),
            "total_loans": len(self._loans),
            "active_loans": len(self.get_active_loans()),
            "overdue_loans": len(self.get_overdue_loans()),
            "total_fines": round(
                sum(l.calculate_fine() for l in self._loans.values()), 2
            ),
        }

    # =========================================================
    # PRIVATE HELPERS
    # =========================================================

    def _get_book_or_raise(self, book_id: str) -> Book:
        if book_id not in self._books:
            raise KeyError(f"Book with ID '{book_id}' not found.")
        return self._books[book_id]

    def _get_member_or_raise(self, member_id: str) -> Member:
        if member_id not in self._members:
            raise KeyError(f"Member with ID '{member_id}' not found.")
        return self._members[member_id]

    def _get_loan_or_raise(self, loan_id: str) -> Loan:
        if loan_id not in self._loans:
            raise KeyError(f"Loan with ID '{loan_id}' not found.")
        return self._loans[loan_id]

    def _validate_person_fields(self, name: str, email: str, phone: str):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email address.")
        if not phone.strip():
            raise ValueError("Phone cannot be empty.")

    def _check_email_unique(self, email: str):
        all_people = list(self._members.values()) + list(self._librarians.values())
        for person in all_people:
            if person.email.lower() == email.lower():
                raise ValueError(f"Email '{email}' is already registered.")
