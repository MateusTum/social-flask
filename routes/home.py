from flask_login import login_required
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)
from config import ROWS_PER_PAGE
from models.tables import Post

bp = Blueprint('home', __name__)


@bp.route('/')
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
