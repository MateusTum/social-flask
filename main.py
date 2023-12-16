from datetime import datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, current_user, logout_user, login_required, LoginManager
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, PostForm, CommentForm

# import os


# Flask configs
app = Flask(__name__)
# TODO: Config os.environ.get('FLASK_KEY')
app.config['SECRET_KEY'] = "bacon"
ckeditor = CKEditor()
ckeditor.init_app(app)

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)

# Bootstrap5
Bootstrap5(app)

# Database configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy()
db.init_app(app)

# ----------------------------------------------------------------------------------------------------------------------
user_post_association = db.Table('user_post_association', db.Model.metadata,
                                 db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                                 db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
                                 )

user_post_likes_association = db.Table('user_post_likes_association', db.Model.metadata,
                                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                                       db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
                                       )

post_comment_association = db.Table('post_comment_association', db.Model.metadata,
                                    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                                    db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'))
                                    )

user_comment_association = db.Table('user_comment_association', db.Model.metadata,
                                    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                                    db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'))
                                    )


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    user_posts = db.Relationship("Post", secondary=user_post_association, back_populates="post_authors")
    user_likes = db.Relationship("Post", secondary=user_post_likes_association, back_populates="post_likes")
    user_comments = db.Relationship("Comment", secondary=user_comment_association, back_populates="comment_author")

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)

    post_authors = db.Relationship("User", secondary=user_post_association, back_populates="user_posts")
    post_likes = db.Relationship("User", secondary=user_post_likes_association, back_populates="user_likes")
    post_comments = db.Relationship("Comment", secondary=post_comment_association, back_populates="comment_post")

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def get_post_likes(self):
        amount_of_likes = len(self.post_likes)
        return amount_of_likes

    def get_post_comments(self):
        amount_of_comments = len(self.post_comments)
        return amount_of_comments


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)

    comment_author = db.Relationship("User", secondary=user_comment_association, back_populates="user_comments")
    comment_post = db.Relationship("Post", secondary=post_comment_association, back_populates="post_comments")

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# ----------------------------------------------------------------------------------------------------------------------
with app.app_context():
    db.create_all()


# ----------------------------------------------------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return db.session().get(User, int(user_id))


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/')
def cover():
    return render_template("cover.html")


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/home')
@login_required
def home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("home.html", posts=posts)


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('login'))
        if check_if_username_already_exists():
            flash('Username already in use')
            return redirect(url_for('login'))
        else:
            new_user = User(
                username=request.form.get('username'),  # type: ignore
                email=request.form.get('email'),  # type: ignore
                password=get_hashed_password(),  # type: ignore
                role="user",  # type: ignore
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("register.html", register_form=register_form)


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit:
        typed_email = request.form.get('email')
        typed_password = request.form.get('password')
        user = db.session.query(User).filter(User.email == typed_email).scalar()
        if not user:
            flash('Email doesnt exist in database')
            return redirect(url_for('login'))
        elif check_password_hash(pwhash=user.password, password=typed_password):
            login_user(user)
            return redirect(url_for('home'))
    else:
        return render_template("login.html", login_form=login_form)


# ----------------------------------------------------------------------------------------------------------------------
@app.route("/new-post", methods=["GET", "POST"])
@login_required
def add_new_post():
    create_post_form = PostForm()
    if create_post_form.validate_on_submit():
        new_post = Post(
            title=create_post_form.title.data,
            content=create_post_form.content.data,
        )
        db.session.add(new_post)
        current_user.user_posts.append(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new-post.html", create_post_form=create_post_form)


# ----------------------------------------------------------------------------------------------------------------------
@app.route("/post/<int:post_id>/new-comment", methods=["GET", "POST"])
@login_required
def add_new_comment(post_id):
    create_comment_form = CommentForm()
    current_post = Post.query.get(post_id)
    if create_comment_form.validate_on_submit():
        new_comment = Comment(
            content=create_comment_form.content.data,
        )
        db.session.add(new_comment)
        new_comment.comment_author.append(current_user)
        new_comment.comment_post.append(current_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new-comment.html", create_comment_form=create_comment_form)


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/like-post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if post:
        if post in current_user.user_likes:
            current_user.user_likes.remove(post)
            db.session.commit()
            return ('like removed')
        else:
            current_user.user_likes.append(post)
            db.session.commit()
            return ('like added')
    else:
        return "404"


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('cover'))


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/examples')
@login_required
def examples():
    return render_template("examples.html")


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
