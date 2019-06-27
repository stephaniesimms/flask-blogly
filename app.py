"""Blogly application."""


from flask import Flask, request, render_template, flash, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def show_homepage():
    """redirecting to / route that dispaly all of existing users """
    return redirect("/users")

@app.route('/users')
def get_users_list():
    """ get existing users list from database and render template with the list"""
    users_list = User.query.all()
    return render_template("index.html", users=users_list)

@app.route('/user/<user_id>')
def show_user_info(user_id):
    """ Show information about the given user."""
    user_info = User.query.get(user_id)
    return render_template('user_info.html', user=user_info)

@app.route("/users/new")
def create_new_user_page():
    """Show an add form for users"""
    return render_template("create_user.html")

@app.route("/users_new", methods=["POST"])
def add_new_user():
    """Process the add form, adding a new user and going back to /users"""
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    image_url = request.form.get("image-url")

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/edit_user/<user_id>")
def show_edit_page(user_id):
    """ Show the edit page for a user"""
    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)

@app.route("/edit_user/<user_id>", methods=["POST"])
def edit_user(user_id):
    """ Process the edit form, returning the user to the /users page"""

    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    image_url = request.form.get("image-url")