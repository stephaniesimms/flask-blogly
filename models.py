"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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

    @classmethod
    def add_user(cls, first_name, last_name, image_url):
        """Create a new user record"""

        user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def delete_user(cls, id):
        """Delete a user from database"""
        user = User.query.get(id)

        db.session.delete(user)
        db.session.commit()