# app.py - Web Entry Point for Library Management System
from flask import Flask, render_template, request, redirect, url_for, flash
from library.manager import LibraryManager
from library.book import Book
from library.person import Member, Librarian
from library.loan import Loan
import datetime

app = Flask(__name__)
app.secret_key = "smart_library_management_system_secure_secret_key"

# Instantiate global LibraryManager
manager = LibraryManager()

# Seed demo data if system is empty
from main import seed_demo_data
seed_demo_data(manager)


# =========================================================
# DASHBOARD
# =========================================================
@app.route("/")
def index():
    stats = manager.get_statistics()
    active_loans = manager.get_active_loans()
    overdue_loans = manager.get_overdue_loans()
    return render_template(
        "dashboard.html",
        stats=stats,
        active_loans=active_loans,
        overdue_loans=overdue_loans
    )


# =========================================================
# BOOKS MANAGEMENT
# =========================================================
@app.route("/books")
def books():
    category = request.args.get("category")
    available_only = request.args.get("available_only") == "true"
    
    books_list = manager.list_books(category=category, available_only=available_only)
    categories = Book.VALID_CATEGORIES
    
    return render_template(
        "books.html",
        books=books_list,
        categories=categories,
        selected_category=category,
        available_only=available_only
    )


@app.route("/book/<book_id>")
def book_detail(book_id):
    try:
        book = manager.get_book(book_id)
        # Find active loans for this specific book
        active_loans = [l for l in manager.get_active_loans() if l.book_id == book_id]
        return render_template("book_detail.html", book=book, active_loans=active_loans)
    except KeyError as e:
        flash(str(e), "error")
        return redirect(url_for("books"))


@app.route("/book/add", methods=["GET", "POST"])
def book_add():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        isbn = request.form.get("isbn")
        category = request.form.get("category")
        try:
            total_copies = int(request.form.get("total_copies", 1))
            year = int(request.form.get("publication_year", datetime.datetime.now().year))
            
            book = manager.add_book(
                title=title,
                author=author,
                isbn=isbn,
                category=category,
                total_copies=total_copies,
                publication_year=year
            )
            flash(f"Book '{book.title}' successfully added! ID: {book.book_id}", "success")
            return redirect(url_for("books"))
        except (ValueError, RuntimeError) as e:
            flash(str(e), "error")
            return redirect(url_for("book_add"))
            
    # GET Request
    categories = Book.VALID_CATEGORIES
    current_year = datetime.datetime.now().year
    return render_template("book_form.html", book=None, categories=categories, current_year=current_year)


@app.route("/book/edit/<book_id>", methods=["GET", "POST"])
def book_edit(book_id):
    try:
        book = manager.get_book(book_id)
    except KeyError as e:
        flash(str(e), "error")
        return redirect(url_for("books"))

    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        category = request.form.get("category")
        try:
            year = int(request.form.get("publication_year", book.publication_year))
            manager.update_book(
                book_id,
                title=title,
                author=author,
                category=category,
                publication_year=year
            )
            flash(f"Book '{title}' details updated successfully!", "success")
            return redirect(url_for("book_detail", book_id=book_id))
        except (ValueError, RuntimeError) as e:
            flash(str(e), "error")
            return redirect(url_for("book_edit", book_id=book_id))
            
    # GET Request
    categories = Book.VALID_CATEGORIES
    current_year = datetime.datetime.now().year
    return render_template("book_form.html", book=book, categories=categories, current_year=current_year)


@app.route("/book/delete/<book_id>", methods=["POST"])
def book_delete(book_id):
    try:
        book = manager.remove_book(book_id)
        flash(f"Book '{book.title}' (ID: {book.book_id}) removed from database.", "success")
    except ValueError as e:
        flash(str(e), "error")
    except KeyError as e:
        flash(str(e), "error")
    return redirect(url_for("books"))


# =========================================================
# MEMBERS MANAGEMENT
# =========================================================
@app.route("/members")
def members():
    members_list = manager.list_members()
    librarians_list = manager.list_librarians()
    return render_template("members.html", members=members_list, librarians=librarians_list)


@app.route("/member/<member_id>")
def member_detail(member_id):
    try:
        member = manager.get_member(member_id)
        loans = manager.get_member_loans(member_id)
        
        active_loans = [l for l in loans if l.status == Loan.STATUS_ACTIVE]
        historical_loans = [l for l in loans if l.status == Loan.STATUS_RETURNED]
        
        return render_template(
            "member_detail.html",
            member=member,
            active_loans=active_loans,
            historical_loans=historical_loans
        )
    except KeyError as e:
        flash(str(e), "error")
        return redirect(url_for("members"))


@app.route("/member/register", methods=["GET", "POST"])
def member_register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        membership_type = request.form.get("membership_type", "Standard")
        try:
            member = manager.register_member(name, email, phone, membership_type)
            flash(f"Member '{member.name}' registered successfully! ID: {member.person_id}", "success")
            return redirect(url_for("members"))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("member_register"))
            
    return render_template("member_form.html")


@app.route("/librarian/add", methods=["GET", "POST"])
def librarian_add():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        employee_id = request.form.get("employee_id")
        department = request.form.get("department", "General")
        try:
            lib = manager.add_librarian(name, email, phone, employee_id, department)
            flash(f"Librarian '{lib.name}' added successfully! ID: {lib.person_id}", "success")
            return redirect(url_for("members"))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("librarian_add"))
            
    return render_template("librarian_form.html")


@app.route("/member/toggle/<member_id>", methods=["POST"])
def member_toggle(member_id):
    try:
        member = manager.toggle_member_status(member_id)
        status_str = "activated" if member.is_active else "suspended"
        flash(f"Member '{member.name}' accounts privileges {status_str}.", "success")
    except KeyError as e:
        flash(str(e), "error")
    
    # Try to redirect to referrer, else members
    return redirect(request.referrer or url_for("members"))


@app.route("/member/delete/<member_id>", methods=["POST"])
def member_delete(member_id):
    try:
        member = manager.remove_member(member_id)
        flash(f"Member '{member.name}' (ID: {member.person_id}) removed from database.", "success")
    except ValueError as e:
        flash(str(e), "error")
    except KeyError as e:
        flash(str(e), "error")
    return redirect(url_for("members"))


# =========================================================
# LOANS MANAGEMENT
# =========================================================
@app.route("/loans")
def loans():
    active_loans = manager.get_active_loans()
    active_members = [m for m in manager.list_members() if m.is_active]
    available_books = manager.list_books(available_only=True)
    return render_template(
        "loans.html",
        active_loans=active_loans,
        active_members=active_members,
        available_books=available_books
    )


@app.route("/loans/borrow", methods=["POST"])
def loan_borrow():
    member_id = request.form.get("member_id")
    book_id = request.form.get("book_id")
    
    if not member_id or not book_id:
        flash("Please select both a member and a book.", "error")
        return redirect(url_for("loans"))
        
    try:
        loan = manager.borrow_book(member_id, book_id)
        flash(f"Book '{loan.book_title}' successfully loaned to {loan.member_name}! Due on: {loan.due_date}", "success")
    except (KeyError, ValueError) as e:
        flash(str(e), "error")
        
    return redirect(url_for("loans"))


@app.route("/loans/return/<loan_id>", methods=["POST"])
def loan_return(loan_id):
    try:
        loan, fine = manager.return_book(loan_id)
        if fine > 0:
            flash(f"Book '{loan.book_title}' checked in successfully. Overdue fine calculated: PKR {fine:.2f}", "warning")
        else:
            flash(f"Book '{loan.book_title}' returned on time! No outstanding fines.", "success")
    except (KeyError, ValueError) as e:
        flash(str(e), "error")
        
    redirect_url = request.form.get("redirect_url")
    return redirect(redirect_url or request.referrer or url_for("loans"))


# =========================================================
# UNIFIED SEARCH
# =========================================================
@app.route("/search")
def search():
    query = request.args.get("query", "").strip()
    search_type = request.args.get("type", "books")
    results = []
    
    if query:
        try:
            if search_type == "books":
                results = manager.search_books(query)
            else:
                results = manager.search_members(query)
        except ValueError as e:
            flash(str(e), "error")
            
    return render_template(
        "search.html",
        query=query,
        search_type=search_type,
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)
