# tests/test_app.py
# Integration tests for Flask Web interface routing and forms
import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, manager
from library import file_handler as fh


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Provide a test client with a temp data directory."""
    monkeypatch.setattr(fh, "DATA_DIR", str(tmp_path))
    fh.FILES["books"] = str(tmp_path / "books.json")
    fh.FILES["members"] = str(tmp_path / "members.json")
    fh.FILES["librarians"] = str(tmp_path / "librarians.json")
    fh.FILES["loans"] = str(tmp_path / "loans.json")
    fh.FILES["counters"] = str(tmp_path / "counters.json")
    
    # Re-initialize the manager with the new mock directory
    manager.__init__()
    
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    
    with app.test_client() as client:
        yield client


def test_dashboard_route(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Library Dashboard" in rv.data
    assert b"Total Titles" in rv.data


def test_books_list_route(client):
    rv = client.get("/books")
    assert rv.status_code == 200
    assert b"Books Catalogue" in rv.data


def test_book_add_and_details_route(client):
    # Test GET request for the add book form
    rv = client.get("/book/add")
    assert rv.status_code == 200
    assert b"Add New Book" in rv.data

    # Add a book via form POST
    post_data = {
        "title": "Unit Test Book",
        "author": "Test Author",
        "isbn": "978-1234567890",
        "category": "Technology",
        "total_copies": "3",
        "publication_year": "2024"
    }
    rv = client.post("/book/add", data=post_data, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Unit Test Book" in rv.data
    
    # View details of the added book (BK0001 is generated as the first ID)
    rv = client.get("/book/BK0001")
    assert rv.status_code == 200
    assert b"BK0001" in rv.data
    assert b"Unit Test Book" in rv.data

    # Test GET request for the edit book form
    rv = client.get("/book/edit/BK0001")
    assert rv.status_code == 200
    assert b"Edit Book: Unit Test Book" in rv.data


def test_member_register_route(client):
    # Register member via form
    post_data = {
        "name": "Alex Mercer",
        "email": "alex@mercer.com",
        "phone": "0300-9999999",
        "membership_type": "Premium"
    }
    rv = client.post("/member/register", data=post_data, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Alex Mercer" in rv.data
    assert b"MB0001" in rv.data


def test_librarian_add_route(client):
    post_data = {
        "name": "Staff User",
        "email": "staff@library.pk",
        "phone": "0321-2222222",
        "employee_id": "EMP-999",
        "department": "Security"
    }
    rv = client.post("/librarian/add", data=post_data, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Staff User" in rv.data
    assert b"EMP-999" in rv.data


def test_loans_route(client):
    rv = client.get("/loans")
    assert rv.status_code == 200
    assert b"Issue New Book Loan" in rv.data


def test_search_route(client):
    rv = client.get("/search?query=clean&type=books")
    assert rv.status_code == 200
    assert b"Search Results" in rv.data
