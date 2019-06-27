"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

"""Default users image."""
PLACEHOLDER_IMG = "https://www.dictionary.com/e/wp-content/uploads/2018/03/Upside-Down_Face_Emoji.png"

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model to create a new user record."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.String, nullable=False, default=PLACEHOLDER_IMG)

    def __repr__(self):
        return f"< User id ='{self.id}' name='{self.first_name} {self.last_name}' >"


class Post(db.Model):
    """Model for create post """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref="posts")