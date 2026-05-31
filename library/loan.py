# loan.py - Loan entity class
# Tracks book borrowing transactions including fines

from datetime import datetime, timedelta


class Loan:
    """Represents a single borrow transaction between a member and a book."""

    LOAN_PERIOD_DAYS = 14       # Default loan period
    FINE_PER_DAY = 5.0          # Fine in PKR per overdue day

    STATUS_ACTIVE = "Active"
    STATUS_RETURNED = "Returned"
    STATUS_OVERDUE = "Overdue"

    def __init__(self, loan_id: str, member_id: str, book_id: str,
                 book_title: str, member_name: str):
        self._loan_id = loan_id
        self._member_id = member_id
        self._book_id = book_id
        self._book_title = book_title
        self._member_name = member_name

        self._borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._due_date = (datetime.now() + timedelta(days=self.LOAN_PERIOD_DAYS)).strftime("%Y-%m-%d")
        self._return_date = None
        self._status = self.STATUS_ACTIVE
        self._fine_amount = 0.0

    # --- Properties ---
    @property
    def loan_id(self):
        return self._loan_id

    @property
    def member_id(self):
        return self._member_id

    @property
    def book_id(self):
        return self._book_id

    @property
    def book_title(self):
        return self._book_title

    @property
    def member_name(self):
        return self._member_name

    @property
    def borrow_date(self):
        return self._borrow_date

    @property
    def due_date(self):
        return self._due_date

    @property
    def return_date(self):
        return self._return_date

    @property
    def status(self):
        return self._status

    @property
    def fine_amount(self):
        return self._fine_amount

    def is_overdue(self) -> bool:
        """Check if the loan is past its due date."""
        if self._status == self.STATUS_RETURNED:
            return False
        due = datetime.strptime(self._due_date, "%Y-%m-%d")
        return datetime.now() > due

    def calculate_fine(self) -> float:
        """Calculate the fine based on overdue days."""
        if self._status == self.STATUS_RETURNED and self._fine_amount > 0:
            return self._fine_amount
        if not self.is_overdue():
            return 0.0
        due = datetime.strptime(self._due_date, "%Y-%m-%d")
        overdue_days = (datetime.now() - due).days
        return round(overdue_days * self.FINE_PER_DAY, 2)

    def process_return(self):
        """Mark the loan as returned and finalize the fine."""
        if self._status == self.STATUS_RETURNED:
            raise ValueError(f"Loan {self._loan_id} is already returned.")
        self._return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._fine_amount = self.calculate_fine()
        self._status = self.STATUS_RETURNED

    def get_status(self) -> str:
        """Get the current live status of the loan."""
        if self._status == self.STATUS_RETURNED:
            return self.STATUS_RETURNED
        if self.is_overdue():
            return self.STATUS_OVERDUE
        return self.STATUS_ACTIVE

    def days_remaining(self) -> int:
        """Days left before the loan is due (negative if overdue)."""
        due = datetime.strptime(self._due_date, "%Y-%m-%d")
        return (due - datetime.now()).days

    def to_dict(self) -> dict:
        """Serialize loan to dictionary for file storage."""
        return {
            "loan_id": self._loan_id,
            "member_id": self._member_id,
            "book_id": self._book_id,
            "book_title": self._book_title,
            "member_name": self._member_name,
            "borrow_date": self._borrow_date,
            "due_date": self._due_date,
            "return_date": self._return_date,
            "status": self._status,
            "fine_amount": self._fine_amount,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Loan":
        """Deserialize a Loan object from a dictionary."""
        obj = cls(
            loan_id=data["loan_id"],
            member_id=data["member_id"],
            book_id=data["book_id"],
            book_title=data.get("book_title", "Unknown"),
            member_name=data.get("member_name", "Unknown"),
        )
        obj._borrow_date = data.get("borrow_date", obj._borrow_date)
        obj._due_date = data.get("due_date", obj._due_date)
        obj._return_date = data.get("return_date")
        obj._status = data.get("status", cls.STATUS_ACTIVE)
        obj._fine_amount = data.get("fine_amount", 0.0)
        return obj

    def display_info(self) -> str:
        live_status = self.get_status()
        fine_str = f"Fine: PKR {self.calculate_fine():.2f}" if live_status == self.STATUS_OVERDUE else ""
        return (
            f"Loan [{self._loan_id}] | Book: '{self._book_title}' | "
            f"Member: {self._member_name} | Borrowed: {self._borrow_date[:10]} | "
            f"Due: {self._due_date} | Status: {live_status} {fine_str}"
        )

    def __str__(self):
        return self.display_info()

    def __repr__(self):
        return f"Loan(id={self._loan_id}, book={self._book_id}, member={self._member_id}, status={self._status})"
