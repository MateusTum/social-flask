from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
from models import db
from models.tables import User, Profile

bp = Blueprint('authentication', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    def check_if_email_already_exists():
        email_to_register = request.form.get('email')
        email_query = User.query.filter(User.email == email_to_register)
        email_query_result = email_query.scalar()
        return email_query_result

    def check_if_username_already_exists():
        username_to_register = request.form.get('username')
        username_query = User.query.filter(User.username == username_to_register)
        username_query_result = username_query.scalar()
        return username_query_result

    def get_hashed_password():
        crude_password = request.form.get('password')
        hashed_password = generate_password_hash(crude_password, method='pbkdf2:sha256', salt_length=8)
        return hashed_password

    register_form = RegisterForm()

    if request.method == 'POST' and register_form.validate_on_submit:
        if check_if_email_already_exists():
            flash('Email already in use')
            return redirect(url_for('authentication.login'))
        if check_if_username_already_exists():
            flash('Username already in use')
            return redirect(url_for('authentication.login'))
        else:
            new_user = User(
                first_name=request.form.get('first_name'),  # type: ignore
                last_name=request.form.get('last_name'),  # type: ignore
                username=request.form.get('username'),  # type: ignore
                email=request.form.get('email'),  # type: ignore
                password=get_hashed_password(),  # type: ignore
                role="user",  # type: ignore
                status="active",  # type: ignore
            )
            db.session.add(new_user)
            new_user_profile = Profile()
            new_user.profile = new_user_profile
            db.session.add(new_user_profile)
            db.session.commit()
            return redirect(url_for('authentication.login'))
    return render_template("register.html", register_form=register_form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit:
        typed_username = request.form.get('username')
        typed_password = request.form.get('password')
        user = db.session.query(User).filter(User.username == typed_username).scalar()
        if not user:
            flash('User doesnt exist in database')
            return redirect(url_for('authentication.login'))
        elif check_password_hash(pwhash=user.password, password=typed_password):
            login_user(user)
            return redirect(url_for('home.home'))
    else:
        return render_template("login.html", login_form=login_form, current_user=current_user)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('cover.cover'))
