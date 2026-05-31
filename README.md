# 📚 Library Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-30%2B-brightgreen)]()

A fully modular, console-based Library Management System built with Python, demonstrating core software engineering principles including OOP, inheritance, file-based persistence, exception handling, and unit testing.

---

## 📖 Overview

This system manages the day-to-day operations of a library:
- Book catalogue management
- Member & librarian registration
- Borrow/return transactions with fine calculation
- Persistent JSON file storage
- Full search and filter functionality

---

## ✨ Features

| Feature | Description |
|---|---|
| 📖 Book Management | Add, remove, search, filter by category |
| 👥 Member Management | Register members, view profiles and loan history |
| 📋 Loan Management | Borrow/return books, track overdue loans |
| 💰 Fine Calculation | Automatic PKR 5/day fine for overdue returns |
| 💾 File Persistence | All data saved as JSON — no database needed |
| 🔍 Search | Search books (title/author/ISBN) & members |
| 📊 Statistics | Live dashboard of library metrics |
| 🧪 Unit Tests | 30+ tests with PyTest covering all modules |

---

## 🏗️ Project Structure

```
LibraryMS/
├── library/
│   ├── __init__.py         # Package init
│   ├── book.py             # Book entity class
│   ├── person.py           # Person (base), Member, Librarian (inheritance)
│   ├── loan.py             # Loan transaction class
│   ├── manager.py          # Core business logic manager
│   ├── file_handler.py     # JSON file persistence layer
│   └── ui.py               # Console UI helpers
├── data/                   # Auto-generated JSON data files
│   ├── books.json
│   ├── members.json
│   ├── librarians.json
│   ├── loans.json
│   └── counters.json
├── tests/
│   ├── __init__.py
│   └── test_library.py     # 30+ unit tests
├── main.py                 # Application entry point
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ OOP Design

```
Person (Base Class)
├── Member    (Inheritance + Polymorphism)
└── Librarian (Inheritance + Polymorphism)

LibraryManager (Composition)
├── uses → Book
├── uses → Member / Librarian
└── uses → Loan
```

**OOP Principles Applied:**
- **Encapsulation** — All attributes are private (`_name`) with public properties
- **Inheritance** — `Member` and `Librarian` extend `Person`
- **Polymorphism** — `get_role()` overridden in each subclass
- **Abstraction** — `LibraryManager` hides complexity behind simple method calls

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/LibraryMS.git
cd LibraryMS

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=library --cov-report=term-missing
```

---

## 📂 Data Storage

All data is stored as human-readable JSON files in the `data/` directory:

- `books.json` — Book catalogue
- `members.json` — Registered members
- `librarians.json` — Library staff
- `loans.json` — All borrow/return transactions
- `counters.json` — Auto-increment ID counters

Data persists between sessions automatically.

---

## 🔧 Exception Handling

The system handles:
- Invalid inputs (empty fields, invalid email)
- Borrowing unavailable books
- Duplicate ISBN / email registration
- Removing members/books with active loans
- Corrupt or missing data files
- Empty search queries

---

## 📊 Statistics Dashboard

The statistics view provides:
- Total book titles and copies
- Available vs borrowed counts
- Total and active members
- Active and overdue loan counts
- Total outstanding fines

---

## 🧪 Testing

Tests cover all major modules with 30+ test functions:

| Module | Tests |
|---|---|
| `book.py` | 11 tests |
| `person.py` | 9 tests |
| `loan.py` | 5 tests |
| `manager.py` | 15 tests |

---

## 👥 Group Members

| Name | Role |
|---|---|
| Member 1 | Book & Loan Module |
| Member 2 | Member Management & UI |
| Member 3 | File Handling & Testing |
| Member 4 | Manager & Integration |
| Member 5 | Documentation & README |

---

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **Storage:** JSON files
- **Testing:** PyTest
- **Version Control:** Git & GitHub

---

## 📄 License

This project is open-source under the MIT License.
