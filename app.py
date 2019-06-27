"""Blogly application."""
from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post
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
    """Redirect to list of users."""
    return redirect("/users")


@app.route('/users')
def get_users_list():
    """Show list of all users."""
    users_list = User.query.order_by("id").all()
    return render_template("index.html", users=users_list)


@app.route('/users/<user_id>')
def show_user_info(user_id):
    """Show information about the given user."""
    user_info = User.query.get(user_id)
    return render_template('user_info.html', user=user_info)


@app.route("/users/new")
def create_new_user_page():
    """Show an add form for users."""
    return render_template("create_user.html")


@app.route("/users_new", methods=["POST"])
def add_new_user():
    """Process the add form, adding a new user and going back to /users."""
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    # get user image otherwise assign value as None to insert default image
    image_url = request.form.get("image-url") or None

    user = User(first_name=first_name,
                last_name=last_name,
                image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/edit_user/<user_id>")
def show_edit_page(user_id):
    """Show the edit page for a user."""
    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)


@app.route("/edit_user/<user_id>", methods=["POST"])
def edit_user(user_id):
    """Process the edit form, returning the user to the /users page."""

    user = User.query.get(user_id)
    user.first_name = request.form.get("first-name")
    user.last_name = request.form.get("last-name")
    user.image_url = request.form.get("image-url") 

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/delete_user/<user_id>", methods=["POST"])
def delete_user(user_id):
    """Delete the user and redirect to users page."""

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<user_id>/posts/new")
def show_new_post_page(user_id):
    """Show form to add a post for that user."""
    user = User.query.get(user_id)
    
    return render_template("post_add.html", user=user)


@app.route("/users/<user_id>/posts", methods=["POST"])
def add_new_post(user_id):
    """Process the new post form. Redirect to user info page."""    
    user = User.query.get(user_id)

    title = request.form.get("title")
    content = request.form.get("content")

    post = Post(title=title,
                content=content,
                user_id=user.id)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route("/posts/<post_id>")
def show_post(post_id):
    """Show a post."""

    post = Post.query.get(post_id)
    return render_template("post_info.html", post=post)


@app.route("/posts/<post_id>/edit")
def show_edit_post_page(post_id):
    """ Show form to edit a post"""
    
    post = Post.query.get(post_id)
    return render_template('post_edit.html', post=post)


@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    
    db.session.delete(post)
    db.session.commit()

    return redirect("/users")