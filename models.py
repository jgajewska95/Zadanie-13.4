from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    authors = db.relationship("Author", lazy="dynamic", secondary="book_author", back_populates="books")

    def __str__(self):
        return f"<Book {self.title}>"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    books = db.relationship("Book", lazy="dynamic", secondary="book_author", back_populates="authors")

    def __str__(self):
        return f"<Author {self.first_name} {self.last_name}>"


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(100))
    is_rented = db.Column(db.Boolean)
    date = db.Column(db.DateTime)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))


book_author = db.Table(
    "book_author",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id")),
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"))
)
