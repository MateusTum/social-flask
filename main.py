from datetime import datetime

from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5

from flask_ckeditor import CKEditor
# from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy

# from functools import wraps
# from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm

# import os


# ~~~~~~~~~~~~~~~~~ GENERAL CONFIGS ~~~~~~~~~~~~~~~~~
# Flask configs
app = Flask(__name__)
# TODO: Config os.environ.get('FLASK_KEY')
app.config['SECRET_KEY'] = "bacon"
ckeditor = CKEditor()
ckeditor.init_app(app)

# Bootstrap5
Bootstrap5(app)

# Database configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy()
db.init_app(app)


# ~~~~~~~~~~~~~~~~~ END OF GENERAL CONFIGS ~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~ TABLES ~~~~~~~~~~~~~~~~~

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# ~~~~~~~~~~~~~~~~~ END OF TABLES ~~~~~~~~~~~~~~~~~


with app.app_context():
    db.create_all()


@app.route('/')
def cover():
    return render_template("cover.html")


@app.route('/home')
def home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("home.html", posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    return render_template("register.html", register_form=register_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    return render_template("login.html", login_form=login_form)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)


@app.route('/examples')
def examples():
    return render_template("examples.html")


if __name__ == "__main__":
    app.run(debug=True)
