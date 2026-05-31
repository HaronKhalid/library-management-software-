 
# book.py - Book entity class
# Represents a book in the library system

from datetime import datetime


class Book:
    """Represents a single book in the library."""

    VALID_CATEGORIES = [
        "Fiction", "Non-Fiction", "Science", "Technology",
        "History", "Mathematics", "Literature", "Self-Help",
        "Biography", "Children", "Reference", "Other"
    ]

    def __init__(self, book_id: str, title: str, author: str,
                 isbn: str, category: str, total_copies: int = 1,
                 publication_year: int = None):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._isbn = isbn
        self._category = category if category in self.VALID_CATEGORIES else "Other"
        self._total_copies = total_copies
        self._available_copies = total_copies
        self._publication_year = publication_year or datetime.now().year
        self._added_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Properties ---
    @property
    def book_id(self):
        return self._book_id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def isbn(self):
        return self._isbn

    @property
    def category(self):
        return self._category

    @property
    def total_copies(self):
        return self._total_copies

    @property
    def available_copies(self):
        return self._available_copies

    @property
    def publication_year(self):
        return self._publication_year

    @property
    def added_at(self):
        return self._added_at

    def is_available(self) -> bool:
        """Check if at least one copy is available for borrowing."""
        return self._available_copies > 0

    def borrow_copy(self):
        """Reduce available copies when a book is borrowed."""
        if not self.is_available():
            raise ValueError(f"No available copies of '{self._title}'.")
        self._available_copies -= 1

    def return_copy(self):
        """Increase available copies when a book is returned."""
        if self._available_copies >= self._total_copies:
            raise ValueError(f"All copies of '{self._title}' are already returned.")
        self._available_copies += 1

    def add_copies(self, count: int):
        """Add more copies to the library."""
        if count <= 0:
            raise ValueError("Count must be a positive integer.")
        self._total_copies += count
        self._available_copies += count

    def to_dict(self) -> dict:
        """Serialize book to dictionary for file storage."""
        return {
            "book_id": self._book_id,
            "title": self._title,
            "author": self._author,
            "isbn": self._isbn,
            "category": self._category,
            "total_copies": self._total_copies,
            "available_copies": self._available_copies,
            "publication_year": self._publication_year,
            "added_at": self._added_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Deserialize a Book object from a dictionary."""
        obj = cls(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            category=data.get("category", "Other"),
            total_copies=data.get("total_copies", 1),
            publication_year=data.get("publication_year"),
        )
        obj._available_copies = data.get("available_copies", obj._total_copies)
        obj._added_at = data.get("added_at", obj._added_at)
        return obj

    def display_info(self) -> str:
        status = f"Available: {self._available_copies}/{self._total_copies}"
        return (
            f"[{self._book_id}] '{self._title}' by {self._author} | "
            f"ISBN: {self._isbn} | Category: {self._category} | "
            f"Year: {self._publication_year} | {status}"
        )

    def __str__(self):
        return self.display_info()

    def __repr__(self):
        return f"Book(id={self._book_id}, title={self._title}, available={self._available_copies})"
