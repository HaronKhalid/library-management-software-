# file_handler.py - JSON file persistence layer
# Handles all read/write operations to the data directory

import json
import os
from typing import Any


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

FILES = {
    "books": os.path.join(DATA_DIR, "books.json"),
    "members": os.path.join(DATA_DIR, "members.json"),
    "librarians": os.path.join(DATA_DIR, "librarians.json"),
    "loans": os.path.join(DATA_DIR, "loans.json"),
    "counters": os.path.join(DATA_DIR, "counters.json"),
}


def ensure_data_directory():
    """Create the data directory if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for file_path in FILES.values():
        if not os.path.exists(file_path):
            _write_json(file_path, {} if "counters" in file_path else [])


def _read_json(file_path: str) -> Any:
    """Read and return parsed JSON from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Corrupted data file: {file_path}. Error: {e}")


def _write_json(file_path: str, data: Any):
    """Write data as formatted JSON to a file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        raise RuntimeError(f"Failed to write to file: {file_path}. Error: {e}")


# --- Books ---
def load_books() -> list:
    return _read_json(FILES["books"])


def save_books(books: list):
    _write_json(FILES["books"], books)


# --- Members ---
def load_members() -> list:
    return _read_json(FILES["members"])


def save_members(members: list):
    _write_json(FILES["members"], members)


# --- Librarians ---
def load_librarians() -> list:
    return _read_json(FILES["librarians"])


def save_librarians(librarians: list):
    _write_json(FILES["librarians"], librarians)


# --- Loans ---
def load_loans() -> list:
    return _read_json(FILES["loans"])


def save_loans(loans: list):
    _write_json(FILES["loans"], loans)


# --- ID Counters ---
def load_counters() -> dict:
    data = _read_json(FILES["counters"])
    if not isinstance(data, dict):
        return {"book": 1, "member": 1, "librarian": 1, "loan": 1}
    return data


def save_counters(counters: dict):
    _write_json(FILES["counters"], counters)


def get_next_id(entity: str) -> str:
    """Generate the next sequential ID for a given entity type."""
    counters = load_counters()
    prefix_map = {
        "book": "BK",
        "member": "MB",
        "librarian": "LB",
        "loan": "LN",
    }
    if entity not in prefix_map:
        raise ValueError(f"Unknown entity type: {entity}")

    current = counters.get(entity, 1)
    new_id = f"{prefix_map[entity]}{current:04d}"
    counters[entity] = current + 1
    save_counters(counters)
    return new_id
