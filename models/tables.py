import os
from datetime import datetime
from flask_login import UserMixin
from funcs import format_current_datetime
from models import db

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

    def get_comment_date(self):
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
