import math
import sqlite3
from contextlib import closing

from flask import Flask, abort, redirect, render_template, request, url_for

from database import get_connection


app = Flask(__name__)

# LEFT JOIN giữ cả danh mục chưa có sách. COUNT(books.id) đếm 0 cho các danh mục đó.
CATEGORY_COUNTS = """
    SELECT categories.id, categories.name, categories.description,
           COUNT(books.id) AS book_count
    FROM categories
    LEFT JOIN books ON books.category_id = categories.id
    GROUP BY categories.id
    ORDER BY categories.name
"""

BOOKS_WITH_CATEGORY = """
    SELECT books.*, categories.name AS category_name
    FROM books JOIN categories ON categories.id = books.category_id
"""


@app.get("/")
def dashboard():
    with closing(get_connection()) as connection:
        total_categories = connection.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
        total_books = connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        categories = connection.execute(CATEGORY_COUNTS).fetchall()
    return render_template("dashboard.html", total_categories=total_categories,
                           total_books=total_books, categories=categories)


@app.get("/categories")
def categories():
    with closing(get_connection()) as connection:
        rows = connection.execute(CATEGORY_COUNTS).fetchall()
    return render_template("categories.html", categories=rows)


@app.get("/categories/<int:id>")
def category_detail(id):
    with closing(get_connection()) as connection:
        category = connection.execute(
            "SELECT id, name, description FROM categories WHERE id = ?", (str(id),)
        ).fetchone()
        if category is None:
            abort(404)
        books_in_category = connection.execute(
            "SELECT id, title FROM books WHERE category_id = ? ORDER BY title, id",
            (category["id"],),
        ).fetchall()
    return render_template("category_detail.html", category=category, books=books_in_category)


@app.route("/categories/add", methods=["GET", "POST"])
@app.route("/categories/<int:id>/edit", methods=["GET", "POST"])
def category_form(id=None):
    category = {"name": "", "description": ""}
    error = None
    with closing(get_connection()) as connection:
        if id is not None:
            category = connection.execute("SELECT * FROM categories WHERE id = ?", (str(id),)).fetchone()
            if category is None:
                abort(404)
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            description = request.form.get("description", "").strip()
            category = {"name": name, "description": description}
            if not name:
                error = "Vui lòng nhập tên danh mục."
            else:
                try:
                    with connection:
                        if id is None:
                            connection.execute("INSERT INTO categories (name, description) VALUES (?, ?)",
                                               (name, description))
                        else:
                            connection.execute("UPDATE categories SET name = ?, description = ? WHERE id = ?",
                                               (name, description, id))
                except sqlite3.IntegrityError:
                    error = "Tên danh mục đã tồn tại."
                else:
                    return redirect(url_for("categories"))
    return render_template("category_form.html", category=category, error=error, id=id)


@app.post("/categories/<int:id>/delete")
def delete_category(id):
    with closing(get_connection()) as connection:
        try:
            with connection:
                result = connection.execute("DELETE FROM categories WHERE id = ?", (str(id),))
                if result.rowcount == 0:
                    abort(404)
        except sqlite3.IntegrityError:
            rows = connection.execute(CATEGORY_COUNTS).fetchall()
            error = "Danh mục đang có sách. Hãy chuyển hoặc xóa các sách trong danh mục trước."
            return render_template("categories.html", categories=rows, error=error), 409
    return redirect(url_for("categories"))


@app.get("/books")
def books():
    with closing(get_connection()) as connection:
        categories = connection.execute("SELECT id, name FROM categories ORDER BY name").fetchall()
        category_id = request.args.get("category_id", type=int)
        if category_id in {category["id"] for category in categories}:
            rows = connection.execute(BOOKS_WITH_CATEGORY + " WHERE books.category_id = ? ORDER BY books.id",
                                      (category_id,)).fetchall()
        else:
            category_id = None
            rows = connection.execute(BOOKS_WITH_CATEGORY + " ORDER BY books.id").fetchall()
    return render_template("books.html", books=rows, categories=categories, category_id=category_id)


@app.get("/books/<int:id>")
def book_detail(id):
    with closing(get_connection()) as connection:
        book = connection.execute(
            BOOKS_WITH_CATEGORY + " WHERE books.id = ?", (str(id),)
        ).fetchone()
    if book is None:
        abort(404)
    return render_template("book_detail.html", book=book)


def validate_book(book, categories):
    if not book["title"]:
        return "Vui lòng nhập tên sách."
    if book["category_id"] not in {str(category["id"]) for category in categories}:
        return "Vui lòng chọn một danh mục có trong danh sách."
    try:
        price = float(book["price"])
        quantity = int(book["quantity"])
    except ValueError:
        return "Giá phải là số và số lượng phải là số nguyên."
    if not math.isfinite(price) or price < 0:
        return "Giá phải là số hữu hạn và không âm."
    if not 0 <= quantity <= 2**63 - 1:
        return "Số lượng phải nằm trong phạm vi số nguyên không âm của SQLite."
    return None


@app.route("/books/add", methods=["GET", "POST"])
@app.route("/books/<int:id>/edit", methods=["GET", "POST"])
def book_form(id=None):
    book = {"title": "", "author": "", "price": "", "quantity": 0, "category_id": ""}
    error = None
    with closing(get_connection()) as connection:
        if id is not None:
            row = connection.execute("SELECT * FROM books WHERE id = ?", (str(id),)).fetchone()
            if row is None:
                abort(404)
            book = {field: row[field] for field in book}
        categories = connection.execute("SELECT id, name FROM categories ORDER BY name").fetchall()
        if request.method == "POST" and categories:
            book = {field: request.form.get(field, "").strip() for field in book}
            error = validate_book(book, categories)
            if error is None:
                values = (book["title"], book["author"], float(book["price"]),
                          int(book["quantity"]), int(book["category_id"]))
                try:
                    with connection:
                        if id is None:
                            connection.execute("""
                                INSERT INTO books (title, author, price, quantity, category_id)
                                VALUES (?, ?, ?, ?, ?)
                            """, values)
                        else:
                            connection.execute("""
                                UPDATE books SET title = ?, author = ?, price = ?,
                                                 quantity = ?, category_id = ?
                                WHERE id = ?
                            """, (*values, id))
                except sqlite3.IntegrityError:
                    categories = connection.execute("SELECT id, name FROM categories ORDER BY name").fetchall()
                    error = "Không lưu được sách. Vui lòng kiểm tra lại danh mục."
                else:
                    return redirect(url_for("books"))
    return render_template("book_form.html", book=book, categories=categories, error=error, id=id)


@app.post("/books/<int:id>/delete")
def delete_book(id):
    with closing(get_connection()) as connection, connection:
        result = connection.execute("DELETE FROM books WHERE id = ?", (str(id),))
        if result.rowcount == 0:
            abort(404)
    return redirect(url_for("books"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
