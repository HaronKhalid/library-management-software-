# person.py - Base class and derived user classes
# Demonstrates: Inheritance, Polymorphism, OOP principles

from datetime import datetime


class Person:
    """Base class representing a person in the library system."""

    def __init__(self, person_id: str, name: str, email: str, phone: str):
        self._person_id = person_id
        self._name = name
        self._email = email
        self._phone = phone
        self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Getters
    @property
    def person_id(self):
        return self._person_id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

    @property
    def created_at(self):
        return self._created_at

    # Setters
    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email address.")
        self._email = value.strip()

    @phone.setter
    def phone(self, value: str):
        self._phone = value.strip()

    def get_role(self) -> str:
        """Polymorphic method - overridden by subclasses."""
        return "Person"

    def to_dict(self) -> dict:
        """Serialize object to dictionary for file storage."""
        return {
            "person_id": self._person_id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone,
            "created_at": self._created_at,
            "role": self.get_role(),
        }

    def display_info(self) -> str:
        return (
            f"[{self.get_role()}] ID: {self._person_id} | "
            f"Name: {self._name} | Email: {self._email} | Phone: {self._phone}"
        )

    def __str__(self):
        return self.display_info()

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._person_id}, name={self._name})"


class Member(Person):
    """Represents a library member who can borrow books."""

    MAX_BORROW_LIMIT = 5  # Maximum books a member can borrow at once

    def __init__(self, person_id: str, name: str, email: str, phone: str,
                 membership_type: str = "Standard"):
        super().__init__(person_id, name, email, phone)
        self._membership_type = membership_type
        self._active_loans = []       # List of active loan IDs
        self._loan_history = []       # List of all past loan IDs
        self._is_active = True

    @property
    def membership_type(self):
        return self._membership_type

    @property
    def active_loans(self):
        return self._active_loans

    @property
    def loan_history(self):
        return self._loan_history

    @property
    def is_active(self):
        return self._is_active

    def get_role(self) -> str:
        return "Member"

    def can_borrow(self) -> bool:
        """Check if member is allowed to borrow more books."""
        return self._is_active and len(self._active_loans) < self.MAX_BORROW_LIMIT

    def add_loan(self, loan_id: str):
        """Record a new active loan."""
        if loan_id not in self._active_loans:
            self._active_loans.append(loan_id)
            self._loan_history.append(loan_id)

    def remove_loan(self, loan_id: str):
        """Remove a loan from active loans on return."""
        if loan_id in self._active_loans:
            self._active_loans.remove(loan_id)

    def deactivate(self):
        self._is_active = False

    def activate(self):
        self._is_active = True

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "membership_type": self._membership_type,
            "active_loans": self._active_loans,
            "loan_history": self._loan_history,
            "is_active": self._is_active,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Member":
        """Deserialize a Member object from a dictionary."""
        obj = cls(
            person_id=data["person_id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            membership_type=data.get("membership_type", "Standard"),
        )
        obj._created_at = data.get("created_at", obj._created_at)
        obj._active_loans = data.get("active_loans", [])
        obj._loan_history = data.get("loan_history", [])
        obj._is_active = data.get("is_active", True)
        return obj

    def display_info(self) -> str:
        base = super().display_info()
        return (
            f"{base} | Membership: {self._membership_type} | "
            f"Active Loans: {len(self._active_loans)}/{self.MAX_BORROW_LIMIT} | "
            f"Status: {'Active' if self._is_active else 'Inactive'}"
        )


class Librarian(Person):
    """Represents a library staff member with admin privileges."""

    def __init__(self, person_id: str, name: str, email: str, phone: str,
                 employee_id: str, department: str = "General"):
        super().__init__(person_id, name, email, phone)
        self._employee_id = employee_id
        self._department = department

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def department(self):
        return self._department

    def get_role(self) -> str:
        return "Librarian"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "employee_id": self._employee_id,
            "department": self._department,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Librarian":
        obj = cls(
            person_id=data["person_id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            employee_id=data.get("employee_id", ""),
            department=data.get("department", "General"),
        )
        obj._created_at = data.get("created_at", obj._created_at)
        return obj

    def display_info(self) -> str:
        base = super().display_info()
        return f"{base} | Employee ID: {self._employee_id} | Dept: {self._department}"
