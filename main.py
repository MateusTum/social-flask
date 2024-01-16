from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from config import SECRET_KEY, DATABASE_URI, DEBUG, HOST
from models.tables import *
from routes import (
    cover,
    home,
    authentication,
    admin,
    posts,
    users,
    community
)

app = Flask(__name__)
ckeditor = CKEditor()
Bootstrap5(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

db.init_app(app)
ckeditor.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session().get(User, int(user_id))


app.register_blueprint(cover.bp)
app.register_blueprint(home.bp, url_prefix='/home')
app.register_blueprint(authentication.bp, url_prefix='/auth')
app.register_blueprint(admin.bp, url_prefix='/admin')
app.register_blueprint(community.bp, url_prefix='/communities')
app.register_blueprint(users.bp, url_prefix='/user')
app.register_blueprint(posts.bp, url_prefix='/posts')


if __name__ == "__main__":
    app.run(host=HOST, debug=DEBUG)
