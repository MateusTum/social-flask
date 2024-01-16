from flask_login import login_required
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)
from config import ROWS_PER_PAGE
from models.tables import Post, User

bp = Blueprint('home', __name__)


@bp.route('/', methods=['GET'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = (Post.query
    .order_by(Post.created_at.desc())
    .filter(Post.status == 'active')
    .paginate(page=page, per_page=ROWS_PER_PAGE))

    return render_template("home.html", posts=posts)
