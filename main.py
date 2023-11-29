# from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5

# from flask_ckeditor import CKEditor
# from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy

# from functools import wraps
# from werkzeug.security import generate_password_hash, check_password_hash
# from forms import
# import os


# ~~~~~~~~~~~~~~~~~ GENERAL CONFIGS ~~~~~~~~~~~~~~~~~
# Flask configs
app = Flask(__name__)
# TODO: Config os.environ.get('FLASK_KEY')
app.config['SECRET_KEY'] = "bacon"

# Bootstrap5
Bootstrap5(app)

# Database configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy()
db.init_app(app)


# ~~~~~~~~~~~~~~~~~ END OF GENERAL CONFIGS ~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~ TABLES ~~~~~~~~~~~~~~~~~

# TODO: Association tables

# TODO: Government account table

# TODO: Company account table

# TODO: User account table

# TODO: Post account table

# TODO: Comment table

# TODO: Group table

# TODO: Chat table?

# ~~~~~~~~~~~~~~~~~ END OF TABLES ~~~~~~~~~~~~~~~~~

# with app.app_context():
#     db.create_all()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
