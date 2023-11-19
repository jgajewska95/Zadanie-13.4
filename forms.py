from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors', render_kw={'disabled':''})
    genre = StringField('Genre', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    publication_year = StringField('Publication Year', validators=[DataRequired()])

    def __init__(self, book=None, **kwargs):
        super().__init__(**kwargs)
        if book is not None:
            self.title.data = book.title
            self.genre.data = book.genre
            self.publisher.data = book.publisher
            self.publication_year.data = book.publication_year
            self.authors.data = ""
            for author in book.authors:
                self.authors.data += author.first_name + " " + author.last_name + ", "


class AuthorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
