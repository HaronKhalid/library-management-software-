# ui.py - Console UI helper
# All display formatting and menu rendering functions

from library.book import Book


DIVIDER = "=" * 65
THIN_LINE = "-" * 65


def clear_screen():
    """Print blank lines to simulate screen clear."""
    print("\n" * 2)


def print_header(title: str):
    print(f"\n{DIVIDER}")
    print(f"  {title.center(61)}")
    print(DIVIDER)


def print_success(msg: str):
    print(f"\n  ✅  {msg}")


def print_error(msg: str):
    print(f"\n  ❌  {msg}")


def print_info(msg: str):
    print(f"\n  ℹ️   {msg}")


def print_warning(msg: str):
    print(f"\n  ⚠️   {msg}")


def get_input(prompt: str) -> str:
    return input(f"  >> {prompt}: ").strip()


def get_int_input(prompt: str, min_val: int = 1, max_val: int = 9999) -> int:
    while True:
        try:
            val = int(get_input(prompt))
            if min_val <= val <= max_val:
                return val
            print_error(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print_error("Invalid input. Please enter a whole number.")


def confirm(prompt: str) -> bool:
    ans = get_input(f"{prompt} (y/n)").lower()
    return ans in ("y", "yes")


def pause():
    input(f"\n  Press Enter to continue...")


def display_books(books: list, title: str = "Books"):
    print_header(title)
    if not books:
        print_info("No books found.")
        return
    print(f"  {'ID':<8} {'Title':<28} {'Author':<20} {'Category':<12} {'Avail'}")
    print(THIN_LINE)
    for b in books:
        avail = f"{b.available_copies}/{b.total_copies}"
        print(f"  {b.book_id:<8} {b.title[:26]:<28} {b.author[:18]:<20} {b.category[:10]:<12} {avail}")
    print(THIN_LINE)
    print(f"  Total: {len(books)} book(s)")


def display_members(members: list, title: str = "Members"):
    print_header(title)
    if not members:
        print_info("No members found.")
        return
    print(f"  {'ID':<8} {'Name':<22} {'Email':<28} {'Loans':<6} {'Status'}")
    print(THIN_LINE)
    for m in members:
        status = "Active" if m.is_active else "Inactive"
        print(f"  {m.person_id:<8} {m.name[:20]:<22} {m.email[:26]:<28} {len(m.active_loans):<6} {status}")
    print(THIN_LINE)
    print(f"  Total: {len(members)} member(s)")


def display_loans(loans: list, title: str = "Loans"):
    print_header(title)
    if not loans:
        print_info("No loans found.")
        return
    print(f"  {'Loan ID':<8} {'Book':<25} {'Member':<20} {'Due':<12} {'Status'}")
    print(THIN_LINE)
    for l in loans:
        status = l.get_status()
        fine = f" (PKR {l.calculate_fine():.0f})" if l.is_overdue() else ""
        print(
            f"  {l.loan_id:<8} {l.book_title[:23]:<25} "
            f"{l.member_name[:18]:<20} {l.due_date:<12} {status}{fine}"
        )
    print(THIN_LINE)
    print(f"  Total: {len(loans)} loan(s)")


def display_statistics(stats: dict):
    print_header("Library Statistics")
    print(f"  {'📚 Total Titles':<30} {stats['total_titles']}")
    print(f"  {'📖 Total Copies':<30} {stats['total_copies']}")
    print(f"  {'✅ Available Copies':<30} {stats['available_copies']}")
    print(f"  {'📤 Borrowed Copies':<30} {stats['borrowed_copies']}")
    print(THIN_LINE)
    print(f"  {'👥 Total Members':<30} {stats['total_members']}")
    print(f"  {'✅ Active Members':<30} {stats['active_members']}")
    print(f"  {'👔 Librarians':<30} {stats['total_librarians']}")
    print(THIN_LINE)
    print(f"  {'📋 Total Loans':<30} {stats['total_loans']}")
    print(f"  {'🔄 Active Loans':<30} {stats['active_loans']}")
    print(f"  {'⚠️  Overdue Loans':<30} {stats['overdue_loans']}")
    print(f"  {'💰 Total Fines (PKR)':<30} {stats['total_fines']:.2f}")
    print(THIN_LINE)


def display_categories():
    print_info(f"Valid categories: {', '.join(Book.VALID_CATEGORIES)}")


def print_main_menu():
    print_header("📚  Library Management System")
    print("  1.  📖  Book Management")
    print("  2.  👥  Member Management")
    print("  3.  📋  Loan Management")
    print("  4.  📊  Statistics")
    print("  5.  🔍  Search")
    print("  0.  🚪  Exit")
    print(THIN_LINE)


def print_book_menu():
    print_header("Book Management")
    print("  1.  Add Book")
    print("  2.  Remove Book")
    print("  3.  List All Books")
    print("  4.  List by Category")
    print("  5.  List Available Books")
    print("  6.  View Book Details")
    print("  0.  Back")
    print(THIN_LINE)


def print_member_menu():
    print_header("Member Management")
    print("  1.  Register Member")
    print("  2.  Remove Member")
    print("  3.  List All Members")
    print("  4.  View Member Details & Loans")
    print("  5.  Add Librarian")
    print("  6.  List Librarians")
    print("  0.  Back")
    print(THIN_LINE)


def print_loan_menu():
    print_header("Loan Management")
    print("  1.  Borrow Book")
    print("  2.  Return Book")
    print("  3.  View All Active Loans")
    print("  4.  View Overdue Loans")
    print("  5.  View Loan Details")
    print("  0.  Back")
    print(THIN_LINE)


def print_search_menu():
    print_header("Search")
    print("  1.  Search Books (title / author / ISBN)")
    print("  2.  Search Members (name / email)")
    print("  0.  Back")
    print(THIN_LINE)
