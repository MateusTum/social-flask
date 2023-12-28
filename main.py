import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify
)
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import (
    UserMixin,
    login_user,
    current_user,
    logout_user,
    login_required,
    LoginManager
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import (
    LoginForm,
    RegisterForm,
    PostForm,
    CommentForm,
    UserProfileForm,
    CommunityForm
)
from funcs import (
    generate_unique_filename,
    format_current_datetime,
    )
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import SECRET_KEY, DATABASE_URI, DEBUG, HOST
import random
import string

# Flask configs
app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="memory://",
)

app.config['SECRET_KEY'] = SECRET_KEY
ckeditor = CKEditor()
ckeditor.init_app(app)

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)

# Bootstrap5
Bootstrap5(app)

# Database configs
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy()
db.init_app(app)

ROWS_PER_PAGE = 10

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

followers = db.Table('followers', db.Model.metadata,
                     db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
                     )

user_community_association = db.Table('user_community_association', db.Model.metadata,
                                 db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                                 db.Column('community_id', db.Integer, db.ForeignKey('communities.id'))
                                 )
                                
post_community_association = db.Table('post_community_association', db.Model.metadata,
                                 db.Column('community_id', db.Integer, db.ForeignKey('communities.id')),
                                 db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
                                 )

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    # Relationship
    posts = db.Relationship("Post", secondary=user_post_association, back_populates="authors")
    likes = db.Relationship("Post", secondary=user_post_likes_association, back_populates="likes")
    comments = db.Relationship("Comment", secondary=user_comment_association, back_populates="author")
    profile = db.relationship('Profile', back_populates='user', uselist=False)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
    communities = db.Relationship("Community", secondary=user_community_association, back_populates="admins")

    # Dates
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False)

    # Relationship
    authors = db.Relationship("User", secondary=user_post_association, back_populates="posts")
    likes = db.Relationship("User", secondary=user_post_likes_association, back_populates="likes")
    comments = db.Relationship("Comment", secondary=post_comment_association, back_populates="post")

    # Dates
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Methods
    def get_post_likes(self):
        amount_of_likes = len(self.likes)
        return amount_of_likes

    def get_post_comments(self):
        amount_of_comments = len(self.comments)
        return amount_of_comments

    def get_post_images(self):
        folder_path = "./static/" + self.image
        try:
            filenames = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            return filenames
        except Exception as e:
            print(f"Error getting filenames in {folder_path}: {e}")
            return []

    def get_post_date(self):
        dt = datetime.now()
        creation_datetime = self.created_at
        time_difference = dt - creation_datetime

        if time_difference.days > 0:
            if time_difference.days == 1:
                return f"{time_difference.days} day ago"
            elif time_difference.days < 7:
                return f"{time_difference.days} days ago"
            else:
                return f"on {format_current_datetime(date=creation_datetime)}"
        elif time_difference.seconds // 3600 > 0:
            hours_ago = time_difference.seconds // 3600
            if hours_ago == 1:
                return f"{hours_ago} hour ago"
            else:
                return f"{hours_ago} hours ago"
        else:
            minutes_ago = time_difference.seconds // 60
            if minutes_ago == 1:
                return f"{minutes_ago} minute ago"
            else:
                return f"{minutes_ago} minutes ago"


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)

    # Relationship
    author = db.Relationship("User", secondary=user_comment_association, back_populates="comments")
    post = db.Relationship("Post", secondary=post_comment_association, back_populates="comments")

    # Dates
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    profile_image_path = db.Column(db.String(255))
    bio = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    street_address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    occupation = db.Column(db.String(100), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    education = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)

    # Social media profiles
    facebook_profile = db.Column(db.String(255))
    twitter_profile = db.Column(db.String(255))
    linkedin_profile = db.Column(db.String(255))

    # Interests related to the user
    interests = db.Column(db.String(255))
    hobbies = db.Column(db.String(255))

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

    # Relationship
    user = db.relationship('User', back_populates='profile')

    # Dates
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)



class Community(db.Model):
    __tablename__ = 'communities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(250))
    picture = db.Column(db.String)

    # Relationships
    admins = db.Relationship("User", secondary=user_community_association, back_populates="communities")
    posts = db.Relationship("Post", secondary=post_community_association, backref="communities_posts")

    # Dates
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
@limiter.limit("1 per second")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    load_more = request.args.get('loadMore', type=bool)
    posts = Post.query.order_by(Post.created_at.desc()).where(Post.status == 'active').paginate(page=page,
                                                                                                per_page=ROWS_PER_PAGE)
    if load_more:
        response_data = {
            'content': render_template('more-posts.html', posts=posts),
            'last_page': True if page == posts.pages else False,
        }
        return jsonify(response_data)
    elif load_more is None:
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
            return redirect(url_for('login'))
    return render_template("register.html", register_form=register_form)


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit:
        typed_username = request.form.get('username')
        typed_password = request.form.get('password')
        user = db.session.query(User).filter(User.username == typed_username).scalar()
        if not user:
            flash('User doesnt exist in database')
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
            status="active",
        )
        db.session.add(new_post)
        db.session.commit()
        if 'images' in request.files:
            files = request.files.getlist('images')

            if len(files) > 1:
                uploaded_images = create_post_form.images.data
                upload_directory = os.path.join(f'./static/uploads/{current_user.username}/posts/{new_post.id}')

                for file in uploaded_images:
                    file_extension = os.path.splitext(file.filename)[1]
                    unique_filename = f"{generate_unique_filename(file_extension=file_extension)}"
                    file.filename = unique_filename
                    upload_path = os.path.join(f'static/uploads/{current_user.username}/posts/{new_post.id}',
                                               file.filename)

                    try:
                        file.save(upload_path)
                    except FileNotFoundError:
                        os.makedirs(upload_directory, exist_ok=True)
                        file.save(upload_path)

                new_post.image = f"uploads/{current_user.username}/posts/{new_post.id}/"

        current_user.posts.append(new_post)
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
        new_comment.author.append(current_user)
        new_comment.post.append(current_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new-comment.html", create_comment_form=create_comment_form)


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/like-post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if post:
        # Toggle the like status (you can use a more sophisticated logic here)
        if post not in current_user.likes:
            current_user.likes.append(post)
            db.session.commit()
            liked = True
        else:
            current_user.likes.remove(post)
            db.session.commit()
            liked = False
        # Return the updated like count and liked status as JSON
        return jsonify({'likes': post.get_post_likes(), 'liked': liked})
    else:
        return jsonify({'error': 'Post not found'}), 404


# ----------------------------------------------------------------------------------------------------------------------
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user in post.authors:
        form = PostForm(title=post.title, content=post.content)
        if form.validate_on_submit() and request.method == 'POST':
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            return redirect(url_for('show_post', post_id=post_id))
        return render_template('edit-post.html', form=form)
    else:
        return jsonify({'error': 'Forbidden'}), 403


# ----------------------------------------------------------------------------------------------------------------------
@app.route("/delete-post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        if current_user in post.authors:
            post.status = 'deleted'
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return jsonify({'error': 'Forbidden'}), 403
    else:
        return jsonify({'error': 'Post not found'}), 404


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
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/examples')
@login_required
def examples():
    return render_template("examples.html")


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/profile/<username>', methods=['GET'])
@limiter.limit("1 per second")
@login_required
def show_profile(username):
    user = User.query.filter_by(username=username).scalar()
    page = request.args.get('page', 1, type=int)
    load_more = request.args.get('loadMore', type=bool)
    profile_posts = (Post.query
                 .join(Post.authors)
                 .filter(Post.status == 'active', User.id == user.id)
                 .order_by(Post.created_at.desc())
                 .paginate(page=page, per_page=ROWS_PER_PAGE))

    if load_more:
        response_data = {
            'content': render_template('more-posts.html', posts=profile_posts),
            'last_page': True if page == profile_posts.pages else False,
        }
        return jsonify(response_data)

    elif load_more is None:
        return render_template('profile.html', user=user, profile_posts=profile_posts)


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.filter_by(username=current_user.username).scalar()
    if user:
        form = UserProfileForm(
            bio=user.profile.bio,
            phone_number=user.profile.phone_number,
            date_of_birth=user.profile.date_of_birth,
            street_address=user.profile.street_address,
            city=user.profile.city,
            state=user.profile.state,
            postal_code=user.profile.postal_code,
            country=user.profile.country,
            gender=user.profile.gender,
            occupation=user.profile.occupation,
            company=user.profile.company,
            education=user.profile.education,
            website=user.profile.website,
            facebook_profile=user.profile.facebook_profile,
            twitter_profile=user.profile.twitter_profile,
            linkedin_profile=user.profile.linkedin_profile,
            interests=user.profile.interests,
            hobbies=user.profile.hobbies,
        )
        if form.validate_on_submit() and request.method == 'POST':
            user_profile_img = form.profile_img.data
            if user_profile_img:
                file_extension = os.path.splitext(user_profile_img.filename)[1]
                unique_filename = f"{generate_unique_filename(file_extension=file_extension)}"
                user_profile_img.filename = unique_filename
                upload_path = os.path.join(f'static/uploads/{current_user.username}/pictures/profile/', user_profile_img.filename)
                upload_directory = os.path.join(f'./static/uploads/{current_user.username}/pictures/profile')
                try:
                    user_profile_img.save(upload_path)
                except FileNotFoundError:
                    os.makedirs(upload_directory, exist_ok=True)
                    user_profile_img.save(upload_path)
                finally:
                    user.profile.profile_image_path = "/" + upload_path

            attributes_to_update = [
            'bio', 'phone_number', 'date_of_birth', 'street_address', 'city', 'state',
            'postal_code', 'country', 'gender', 'occupation', 'company', 'education',
            'website', 'facebook_profile', 'twitter_profile', 'linkedin_profile',
            'interests', 'hobbies'
            ]

            for attribute in attributes_to_update:
                setattr(user.profile, attribute, getattr(form, attribute).data)
                
            db.session.commit()
            return redirect(url_for('show_profile', username=user.username))
        return render_template('edit-profile.html', form=form)
    else:
        return jsonify({'error': 'Profile not found'}), 404


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/new-community', methods=['GET', 'POST'])
@login_required
def new_community():
    form = CommunityForm()

    if form.validate_on_submit() and request.method == 'POST':
        new_community = Community(
                name=request.form.get('name'),  # type: ignore
                description=request.form.get('description'),  # type: ignore
            )
        db.session.add(new_community)
        db.session.commit()

        community_img = form.picture.data
        if community_img:
            file_extension = os.path.splitext(community_img.filename)[1]
            unique_filename = f"{generate_unique_filename(file_extension=file_extension)}"
            community_img.filename = unique_filename
            upload_path = os.path.join(f'static/uploads/{new_community.name}/pictures/profile/', community_img.filename)
            upload_directory = os.path.join(f'./static/uploads/{new_community.name}/pictures/profile')
            try:
                community_img.save(upload_path)
            except FileNotFoundError:
                os.makedirs(upload_directory, exist_ok=True)
                community_img.save(upload_path)
            finally:
                new_community.picture = "/" + upload_path
            
        new_community.admins.append(current_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('new-community.html', form=form)

    
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/communities', methods=['GET'])
@login_required
def show_communities():
    communities = Community.query.order_by(Community.created_at.desc())

    return render_template('communities.html', communities=communities)


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/users', methods=['GET'])
@login_required
def show_users():
    users = User.query.order_by(User.created_at.desc())

    return render_template('users.html', users=users)


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/generate-users', methods=['GET'])
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
        first_names = ['John', 'Jane', 'Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack', 'Kate', 'Leo', 'Mia', 'Nick', 'Olivia', 'Peter', 'Quinn', 'Rachel']
        last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Davis']

        users = []
        for i in range(20):
            user = User(username=usernames[i],
             first_name=random.choice(first_names),
              last_name=random.choice(last_names),
               password=get_hashed_password(),
               email=generate_random_email(),
               role='user',
               status='active')
            new_user_profile = Profile()
            user.profile = new_user_profile
            user.profile.profile_image_path = '/static/assets/avatar.jpg'
            users.append(user)

        return users

    users = generate_random_data()

    db.session.add_all(users)
    db.session.commit()

    return redirect(url_for('home'))


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/share-post/<int:post_id>', methods=['POST'])
@login_required
def share_post(post_id):
    post = Post.query.get(post_id)

    return jsonify({'error': 'In progress'})


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host=HOST, debug=DEBUG)
