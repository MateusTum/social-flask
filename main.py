# from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5

# from flask_ckeditor import CKEditor
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
def cover():
    return render_template("cover.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    return render_template("register.html", register_form=register_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    return render_template("login.html", login_form=login_form)


if __name__ == "__main__":
    app.run(debug=True)
