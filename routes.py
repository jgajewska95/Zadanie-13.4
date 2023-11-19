import json

from flask import request, render_template, redirect, url_for, jsonify, make_response, abort

from app import app, db_manager
from app.forms import BookForm, AuthorForm


def serialize_book(book):
    authors_result = []
    for author in book.authors:
        authors_result.append({
            'id': author.id,
            'first_name': author.first_name,
            'last_name': author.last_name
        })

    return {
        'id': book.id,
        'title': book.title,
        'genre': book.genre,
        'publisher': book.publisher,
        'publication_year': book.publication_year,
        'authors': authors_result,
    }


@app.route("/books/", methods=["GET", "POST"])
def books_all():
    form = BookForm()
    author_form = AuthorForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            db_manager.add_book(form.data)
        if author_form.validate_on_submit():
            db_manager.add_author(author_form.data)
        return redirect(url_for("books_all"))

    return render_template("books.html", form=form, author_form=author_form, books=db_manager.get_books(), error=error,
                           authors=db_manager.get_authors())


@app.route("/books/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    if request.method == "POST":
        form = BookForm()
        if form.validate_on_submit():
            db_manager.update_book(book_id, form.data)
        return redirect(url_for("books_all"))
    book = db_manager.get_book(book_id)
    authors = db_manager.get_authors()
    form = BookForm(book)
    return render_template("book_details.html", form=form, book_id=book_id, authors=authors)


@app.route("/books/<int:book_id>/<int:author_id>/", methods=["POST"])
def book_details_author(book_id, author_id):
    db_manager.add_book_author(book_id, author_id)
    return redirect(url_for(f"book_details", book_id=book_id))


@app.route("/api/v1/books/", methods=["GET"])
def api_v1_books():
    return jsonify([serialize_book(book) for book in db_manager.get_books()])


@app.route("/api/v1/books/<int:book_id>/", methods=["GET"])
def api_v1_book(book_id):
    book = db_manager.get_book(book_id)
    if book is None:
        abort(404)
    return jsonify([serialize_book(book)])


@app.route("/api/v1/books/", methods=["POST"])
def api_v1_book_new():
    db_manager.add_book(json.loads(request.data))
    return "Success"


@app.route("/api/v1/books/<int:book_id>/", methods=["DELETE"])
def api_v1_book_delete(book_id):
    result = db_manager.delete_book(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/books/<int:book_id>/", methods=["PUT"])
def update_todo(book_id):
    book = db_manager.get_book(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'genre' in data and not isinstance(data.get('genre'), str),
        'publisher' in data and not isinstance(data.get('publisher'), str),
        'publication_year' in data and not isinstance(data.get('publication_year'), str)
    ]):
        abort(400)
    book = {
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'genre': data.get('genre', book['genre']),
        'publisher': data.get('publisher', book['publisher']),
        'publication_year': data.get('publication_year', book['publication_year'])
    }
    db_manager.update_book(book_id, book)
    return jsonify({'book': book})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)
