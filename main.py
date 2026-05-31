# main.py - Application Entry Point
# Smart Library Management System

from library.manager import LibraryManager
from library import ui


def handle_books(manager: LibraryManager):
    """Book management sub-menu."""
    while True:
        ui.print_book_menu()
        choice = ui.get_input("Choice")

        if choice == "1":
            # Add Book
            ui.print_header("Add New Book")
            ui.display_categories()
            try:
                title = ui.get_input("Title")
                author = ui.get_input("Author")
                isbn = ui.get_input("ISBN")
                category = ui.get_input("Category")
                copies = ui.get_int_input("Number of Copies", 1, 100)
                year = ui.get_int_input("Publication Year", 1000, 2100)
                book = manager.add_book(title, author, isbn, category, copies, year)
                ui.print_success(f"Book added successfully! ID: {book.book_id}")
            except (ValueError, RuntimeError) as e:
                ui.print_error(str(e))

        elif choice == "2":
            # Remove Book
            ui.print_header("Remove Book")
            book_id = ui.get_input("Book ID")
            try:
                book = manager.get_book(book_id)
                ui.print_info(str(book))
                if ui.confirm("Are you sure you want to remove this book?"):
                    manager.remove_book(book_id)
                    ui.print_success("Book removed.")
            except (KeyError, ValueError) as e:
                ui.print_error(str(e))

        elif choice == "3":
            ui.display_books(manager.list_books(), "All Books")

        elif choice == "4":
            ui.display_categories()
            cat = ui.get_input("Enter category")
            books = manager.list_books(category=cat)
            ui.display_books(books, f"Books in '{cat}'")

        elif choice == "5":
            ui.display_books(manager.list_books(available_only=True), "Available Books")

        elif choice == "6":
            book_id = ui.get_input("Book ID")
            try:
                book = manager.get_book(book_id)
                ui.print_header("Book Details")
                print(f"\n  {book.display_info()}")
                print(f"\n  Added on: {book.added_at}")
            except KeyError as e:
                ui.print_error(str(e))

        elif choice == "0":
            break
        else:
            ui.print_error("Invalid choice.")

        ui.pause()


def handle_members(manager: LibraryManager):
    """Member management sub-menu."""
    while True:
        ui.print_member_menu()
        choice = ui.get_input("Choice")

        if choice == "1":
            # Register Member
            ui.print_header("Register New Member")
            try:
                name = ui.get_input("Full Name")
                email = ui.get_input("Email")
                phone = ui.get_input("Phone")
                print("  Membership types: Standard, Premium, Student")
                m_type = ui.get_input("Membership Type (default: Standard)") or "Standard"
                member = manager.register_member(name, email, phone, m_type)
                ui.print_success(f"Member registered! ID: {member.person_id}")
            except ValueError as e:
                ui.print_error(str(e))

        elif choice == "2":
            # Remove Member
            ui.print_header("Remove Member")
            member_id = ui.get_input("Member ID")
            try:
                member = manager.get_member(member_id)
                ui.print_info(str(member))
                if ui.confirm("Remove this member?"):
                    manager.remove_member(member_id)
                    ui.print_success("Member removed.")
            except (KeyError, ValueError) as e:
                ui.print_error(str(e))

        elif choice == "3":
            ui.display_members(manager.list_members(), "All Members")

        elif choice == "4":
            # Member details + loan history
            member_id = ui.get_input("Member ID")
            try:
                member = manager.get_member(member_id)
                ui.print_header("Member Details")
                print(f"\n  {member.display_info()}")
                loans = manager.get_member_loans(member_id)
                if loans:
                    print()
                    ui.display_loans(loans, f"Loans for {member.name}")
                else:
                    ui.print_info("No loan history.")
            except KeyError as e:
                ui.print_error(str(e))

        elif choice == "5":
            # Add Librarian
            ui.print_header("Add Librarian")
            try:
                name = ui.get_input("Full Name")
                email = ui.get_input("Email")
                phone = ui.get_input("Phone")
                emp_id = ui.get_input("Employee ID")
                dept = ui.get_input("Department (default: General)") or "General"
                lib = manager.add_librarian(name, email, phone, emp_id, dept)
                ui.print_success(f"Librarian added! ID: {lib.person_id}")
            except ValueError as e:
                ui.print_error(str(e))

        elif choice == "6":
            ui.display_members(manager.list_librarians(), "All Librarians")

        elif choice == "0":
            break
        else:
            ui.print_error("Invalid choice.")

        ui.pause()


def handle_loans(manager: LibraryManager):
    """Loan management sub-menu."""
    while True:
        ui.print_loan_menu()
        choice = ui.get_input("Choice")

        if choice == "1":
            # Borrow Book
            ui.print_header("Borrow Book")
            try:
                member_id = ui.get_input("Member ID")
                book_id = ui.get_input("Book ID")
                loan = manager.borrow_book(member_id, book_id)
                ui.print_success(f"Book borrowed! Loan ID: {loan.loan_id} | Due: {loan.due_date}")
            except (KeyError, ValueError) as e:
                ui.print_error(str(e))

        elif choice == "2":
            # Return Book
            ui.print_header("Return Book")
            try:
                loan_id = ui.get_input("Loan ID")
                loan, fine = manager.return_book(loan_id)
                ui.print_success(f"Book returned: '{loan.book_title}'")
                if fine > 0:
                    ui.print_warning(f"Fine due: PKR {fine:.2f}")
                else:
                    ui.print_info("No fine. Returned on time!")
            except (KeyError, ValueError) as e:
                ui.print_error(str(e))

        elif choice == "3":
            loans = manager.get_active_loans()
            ui.display_loans(loans, "Active Loans")

        elif choice == "4":
            loans = manager.get_overdue_loans()
            ui.display_loans(loans, "Overdue Loans")

        elif choice == "5":
            loan_id = ui.get_input("Loan ID")
            try:
                loan = manager.get_loan(loan_id)
                ui.print_header("Loan Details")
                print(f"\n  {loan.display_info()}")
                print(f"\n  Borrowed on : {loan.borrow_date}")
                if loan.return_date:
                    print(f"  Returned on : {loan.return_date}")
                else:
                    days = loan.days_remaining()
                    if days >= 0:
                        print(f"  Days remaining: {days}")
                    else:
                        print(f"  Overdue by: {abs(days)} day(s)")
                        print(f"  Fine: PKR {loan.calculate_fine():.2f}")
            except KeyError as e:
                ui.print_error(str(e))

        elif choice == "0":
            break
        else:
            ui.print_error("Invalid choice.")

        ui.pause()


def handle_search(manager: LibraryManager):
    """Search sub-menu."""
    while True:
        ui.print_search_menu()
        choice = ui.get_input("Choice")

        if choice == "1":
            query = ui.get_input("Search books (title / author / ISBN)")
            try:
                results = manager.search_books(query)
                ui.display_books(results, f"Search Results for '{query}'")
            except ValueError as e:
                ui.print_error(str(e))

        elif choice == "2":
            query = ui.get_input("Search members (name / email)")
            try:
                results = manager.search_members(query)
                ui.display_members(results, f"Search Results for '{query}'")
            except ValueError as e:
                ui.print_error(str(e))

        elif choice == "0":
            break
        else:
            ui.print_error("Invalid choice.")

        ui.pause()


def seed_demo_data(manager: LibraryManager):
    """Seed some demo data if the system is empty (first run)."""
    if manager.list_books():
        return  # Already has data

    print("\n  Setting up demo data for first run...")

    # Books
    books_data = [
        ("Clean Code", "Robert C. Martin", "978-0132350884", "Technology", 3, 2008),
        ("The Alchemist", "Paulo Coelho", "978-0062315007", "Fiction", 4, 1988),
        ("A Brief History of Time", "Stephen Hawking", "978-0553380163", "Science", 2, 1988),
        ("Atomic Habits", "James Clear", "978-0735211292", "Self-Help", 3, 2018),
        ("1984", "George Orwell", "978-0451524935", "Fiction", 5, 1949),
        ("Sapiens", "Yuval Noah Harari", "978-0062316097", "History", 2, 2011),
        ("Introduction to Algorithms", "Thomas Cormen", "978-0262033848", "Technology", 2, 2009),
        ("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", "Literature", 3, 1925),
    ]
    for args in books_data:
        manager.add_book(*args)

    # Members
    manager.register_member("Ali Raza", "ali.raza@gmail.com", "0300-1234567", "Student")
    manager.register_member("Sara Khan", "sara.khan@hotmail.com", "0301-9876543", "Standard")
    manager.register_member("Hamza Ahmed", "hamza.ahmed@yahoo.com", "0311-5555555", "Premium")

    # Librarian
    manager.add_librarian("Ms. Samreen", "samreen@library.pk", "0321-1111111", "EMP-001", "Management")

    print("  ✅ Demo data loaded successfully!")


def main():
    """Main application entry point."""
    manager = LibraryManager()
    seed_demo_data(manager)

    while True:
        ui.print_main_menu()
        choice = ui.get_input("Choice")

        if choice == "1":
            handle_books(manager)
        elif choice == "2":
            handle_members(manager)
        elif choice == "3":
            handle_loans(manager)
        elif choice == "4":
            stats = manager.get_statistics()
            ui.display_statistics(stats)
            ui.pause()
        elif choice == "5":
            handle_search(manager)
        elif choice == "0":
            ui.print_header("Goodbye! 👋")
            break
        else:
            ui.print_error("Invalid choice. Please select from the menu.")


if __name__ == "__main__":
    main()
