"""Blogly application."""


from flask import Flask, request, render_template, flash, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

app = Flask(__name__)
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
    user_info = User.query.get(user_id)
    return render_template('user_info.html', user=user_info)