from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required
from werkzeug.security import generate_password_hash
import random
import string

from models import db
from models.tables import Profile, User

bp = Blueprint('admin', __name__)


@bp.route('/generate-users', methods=['GET'])
@login_required
def generate_users():
    def generate_random_email():
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'example.com', 'domain.com'])
        return f"{username}@{domain}"

    def get_hashed_password():
        crude_password = '12345678'
        hashed_password = generate_password_hash(crude_password, method='pbkdf2:sha256', salt_length=8)
        return hashed_password

    def generate_random_data():
        usernames = [''.join(random.choices(string.ascii_lowercase, k=8)) for _ in range(20)]
        first_names = ['John', 'Jane', 'Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Henry', 'Ivy',
                       'Jack', 'Kate', 'Leo', 'Mia', 'Nick', 'Olivia', 'Peter', 'Quinn', 'Rachel']
        last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor',
                      'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez',
                      'Davis']

        users = []
        for i in range(20):
            user = User(username=usernames[i],  # type: ignore
                        first_name=random.choice(first_names),  # type: ignore
                        last_name=random.choice(last_names),  # type: ignore
                        password=get_hashed_password(),  # type: ignore
                        email=generate_random_email(),  # type: ignore
                        role='user',  # type: ignore
                        status='active')  # type: ignore
            new_user_profile = Profile()
            user.profile = new_user_profile
            user.profile.profile_image_path = '/static/assets/avatar.jpg'
            users.append(user)

        return users

    users = generate_random_data()

    db.session.add_all(users)
    db.session.commit()

    return redirect(url_for('home.home'))


@bp.route('/users', methods=['GET'])
@login_required
def show_users():
    users = User.query.order_by(User.created_at.desc())

    return render_template('users.html', users=users)
