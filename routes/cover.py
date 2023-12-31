from flask import Blueprint, render_template

bp = Blueprint('cover', __name__)


@bp.route('/')
def cover():
    return render_template("cover.html")
