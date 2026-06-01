# tests/test_library.py
# Unit tests for the Library Management System
# Run with: pytest tests/ -v

import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library.book import Book
from library.person import Person, Member, Librarian
from library.loan import Loan
from library.manager import LibraryManager
from library import file_handler as fh


# =========================================================
# FIXTURES
# =========================================================

@pytest.fixture
def sample_book():
    return Book("BK0001", "Clean Code", "Robert C. Martin",
                "978-0132350884", "Technology", 3, 2008)


@pytest.fixture
def sample_member():
    return Member("MB0001", "Ali Raza", "ali@test.com", "0300-1234567", "Standard")


@pytest.fixture
def sample_librarian():
    return Librarian("LB0001", "Ms. Samreen", "samreen@lib.com",
                     "0321-0000000", "EMP-001", "Management")


@pytest.fixture
def sample_loan(sample_member, sample_book):
    return Loan("LN0001", sample_member.person_id, sample_book.book_id,
                sample_book.title, sample_member.name)


@pytest.fixture
def manager(tmp_path, monkeypatch):
    """Provide a LibraryManager with a temp data directory."""
    monkeypatch.setattr(fh, "DATA_DIR", str(tmp_path))
    fh.FILES["books"] = str(tmp_path / "books.json")
    fh.FILES["members"] = str(tmp_path / "members.json")
    fh.FILES["librarians"] = str(tmp_path / "librarians.json")
    fh.FILES["loans"] = str(tmp_path / "loans.json")
    fh.FILES["counters"] = str(tmp_path / "counters.json")
    return LibraryManager()


# =========================================================
# BOOK TESTS
# =========================================================

def test_book_creation(sample_book):
    assert sample_book.book_id == "BK0001"
    assert sample_book.title == "Clean Code"
    assert sample_book.author == "Robert C. Martin"
    assert sample_book.total_copies == 3
    assert sample_book.available_copies == 3


def test_book_is_available(sample_book):
    assert sample_book.is_available() is True


def test_book_borrow_copy(sample_book):
    sample_book.borrow_copy()
    assert sample_book.available_copies == 2


def test_book_return_copy(sample_book):
    sample_book.borrow_copy()
    sample_book.return_copy()
    assert sample_book.available_copies == 3


def test_book_borrow_all_copies_unavailable(sample_book):
    for _ in range(3):
        sample_book.borrow_copy()
    assert sample_book.is_available() is False


def test_book_borrow_raises_when_unavailable(sample_book):
    for _ in range(3):
        sample_book.borrow_copy()
    with pytest.raises(ValueError, match="No available copies"):
        sample_book.borrow_copy()


def test_book_return_raises_when_all_returned(sample_book):
    with pytest.raises(ValueError, match="already returned"):
        sample_book.return_copy()


def test_book_add_copies(sample_book):
    sample_book.add_copies(2)
    assert sample_book.total_copies == 5
    assert sample_book.available_copies == 5


def test_book_add_copies_invalid(sample_book):
    with pytest.raises(ValueError):
        sample_book.add_copies(0)


def test_book_invalid_category_defaults_to_other():
    book = Book("BK0099", "Test", "Author", "000", "InvalidCat", 1)
    assert book.category == "Other"


def test_book_serialization(sample_book):
    d = sample_book.to_dict()
    restored = Book.from_dict(d)
    assert restored.book_id == sample_book.book_id
    assert restored.title == sample_book.title
    assert restored.available_copies == sample_book.available_copies


# =========================================================
# PERSON / MEMBER / LIBRARIAN TESTS
# =========================================================

def test_member_creation(sample_member):
    assert sample_member.person_id == "MB0001"
    assert sample_member.name == "Ali Raza"
    assert sample_member.get_role() == "Member"
    assert sample_member.is_active is True


def test_librarian_creation(sample_librarian):
    assert sample_librarian.get_role() == "Librarian"
    assert sample_librarian.employee_id == "EMP-001"


def test_member_can_borrow(sample_member):
    assert sample_member.can_borrow() is True


def test_member_borrow_limit(sample_member):
    for i in range(Member.MAX_BORROW_LIMIT):
        sample_member.add_loan(f"LN000{i}")
    assert sample_member.can_borrow() is False


def test_member_add_and_remove_loan(sample_member):
    sample_member.add_loan("LN0001")
    assert "LN0001" in sample_member.active_loans
    sample_member.remove_loan("LN0001")
    assert "LN0001" not in sample_member.active_loans


def test_member_loan_history_preserved(sample_member):
    sample_member.add_loan("LN0001")
    sample_member.remove_loan("LN0001")
    assert "LN0001" in sample_member.loan_history


def test_member_deactivate(sample_member):
    sample_member.deactivate()
    assert sample_member.is_active is False
    assert sample_member.can_borrow() is False


def test_member_serialization(sample_member):
    sample_member.add_loan("LN0001")
    d = sample_member.to_dict()
    restored = Member.from_dict(d)
    assert restored.person_id == sample_member.person_id
    assert "LN0001" in restored.active_loans


def test_person_invalid_email(sample_member):
    with pytest.raises(ValueError, match="Invalid email"):
        sample_member.email = "not-an-email"


# =========================================================
# LOAN TESTS
# =========================================================

def test_loan_creation(sample_loan):
    assert sample_loan.loan_id == "LN0001"
    assert sample_loan.status == Loan.STATUS_ACTIVE


def test_loan_not_overdue_on_creation(sample_loan):
    assert sample_loan.is_overdue() is False
    assert sample_loan.calculate_fine() == 0.0


def test_loan_process_return(sample_loan):
    sample_loan.process_return()
    assert sample_loan.status == Loan.STATUS_RETURNED
    assert sample_loan.return_date is not None


def test_loan_double_return_raises(sample_loan):
    sample_loan.process_return()
    with pytest.raises(ValueError, match="already returned"):
        sample_loan.process_return()


def test_loan_serialization(sample_loan):
    d = sample_loan.to_dict()
    restored = Loan.from_dict(d)
    assert restored.loan_id == sample_loan.loan_id
    assert restored.status == sample_loan.status


# =========================================================
# MANAGER INTEGRATION TESTS
# =========================================================

def test_manager_add_book(manager):
    book = manager.add_book("Test Book", "Test Author", "ISBN-001", "Science", 2, 2020)
    assert book.book_id.startswith("BK")
    assert len(manager.list_books()) == 1


def test_manager_duplicate_isbn_raises(manager):
    manager.add_book("Book A", "Author A", "ISBN-001", "Science", 1)
    with pytest.raises(ValueError, match="ISBN"):
        manager.add_book("Book B", "Author B", "ISBN-001", "Fiction", 1)


def test_manager_register_member(manager):
    m = manager.register_member("Sara", "sara@test.com", "0300-000")
    assert m.person_id.startswith("MB")
    assert len(manager.list_members()) == 1


def test_manager_duplicate_email_raises(manager):
    manager.register_member("Sara", "sara@test.com", "0300-000")
    with pytest.raises(ValueError, match="already registered"):
        manager.register_member("Sara2", "sara@test.com", "0300-001")


def test_manager_borrow_and_return(manager):
    book = manager.add_book("Test", "Author", "ISBN-X", "Fiction", 1)
    member = manager.register_member("User", "user@test.com", "0300-111")
    loan = manager.borrow_book(member.person_id, book.book_id)
    assert loan.status == Loan.STATUS_ACTIVE

    updated_book = manager.get_book(book.book_id)
    assert updated_book.available_copies == 0

    returned_loan, fine = manager.return_book(loan.loan_id)
    assert returned_loan.status == Loan.STATUS_RETURNED
    assert manager.get_book(book.book_id).available_copies == 1


def test_manager_borrow_unavailable_raises(manager):
    book = manager.add_book("Test", "Author", "ISBN-Y", "Fiction", 1)
    m1 = manager.register_member("User1", "u1@test.com", "0300-001")
    m2 = manager.register_member("User2", "u2@test.com", "0300-002")
    manager.borrow_book(m1.person_id, book.book_id)
    with pytest.raises(ValueError, match="No available copies"):
        manager.borrow_book(m2.person_id, book.book_id)


def test_manager_search_books(manager):
    manager.add_book("Python Programming", "Guido", "ISBN-P", "Technology", 1)
    manager.add_book("Java Basics", "James", "ISBN-J", "Technology", 1)
    results = manager.search_books("python")
    assert len(results) == 1
    assert results[0].title == "Python Programming"


def test_manager_search_members(manager):
    manager.register_member("Ahmad Ali", "ahmad@test.com", "0300-001")
    manager.register_member("Sara Khan", "sara@test.com", "0300-002")
    results = manager.search_members("ahmad")
    assert len(results) == 1
    assert results[0].name == "Ahmad Ali"


def test_manager_statistics(manager):
    manager.add_book("Test", "Author", "ISBN-S", "Science", 2)
    manager.register_member("User", "u@test.com", "0300-001")
    stats = manager.get_statistics()
    assert stats["total_titles"] == 1
    assert stats["total_copies"] == 2
    assert stats["total_members"] == 1


def test_manager_remove_book_with_active_loan_raises(manager):
    book = manager.add_book("Test", "Author", "ISBN-R", "Fiction", 1)
    member = manager.register_member("User", "user@test.com", "0300-111")
    manager.borrow_book(member.person_id, book.book_id)
    with pytest.raises(ValueError, match="active loan"):
        manager.remove_book(book.book_id)


def test_manager_remove_member_with_active_loan_raises(manager):
    book = manager.add_book("Test", "Author", "ISBN-M", "Fiction", 1)
    member = manager.register_member("User", "user@test.com", "0300-222")
    manager.borrow_book(member.person_id, book.book_id)
    with pytest.raises(ValueError, match="active loan"):
        manager.remove_member(member.person_id)


def test_manager_get_nonexistent_book_raises(manager):
    with pytest.raises(KeyError, match="not found"):
        manager.get_book("BK9999")


def test_manager_filter_by_category(manager):
    manager.add_book("Sci Book", "Author", "ISBN-SC1", "Science", 1)
    manager.add_book("Fic Book", "Author", "ISBN-FC1", "Fiction", 1)
    sci_books = manager.list_books(category="Science")
    assert all(b.category == "Science" for b in sci_books)
    assert len(sci_books) == 1


def test_manager_toggle_member_status(manager):
    member = manager.register_member("John Doe", "john@test.com", "0300-999")
    assert member.is_active is True
    manager.toggle_member_status(member.person_id)
    assert member.is_active is False
    manager.toggle_member_status(member.person_id)
    assert member.is_active is True


def test_manager_update_member(manager):
    member = manager.register_member("Jane Doe", "jane@test.com", "0300-888", "Standard")
    manager.update_member(member.person_id, name="Jane Smith", email="jane.smith@test.com", phone="0300-777", membership_type="Premium")
    updated = manager.get_member(member.person_id)
    assert updated.name == "Jane Smith"
    assert updated.email == "jane.smith@test.com"
    assert updated.phone == "0300-777"
    assert updated.membership_type == "Premium"
