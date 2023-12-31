import os
from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from forms import CommunityForm
from funcs import generate_unique_filename
from models import db
from models.tables import Community

bp = Blueprint('community', __name__)


@bp.route('/create-community', methods=['GET', 'POST'])
@login_required
def create_community():
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


@bp.route('/', methods=['GET'])
@login_required
def show_communities():
    communities = Community.query.order_by(Community.created_at.desc())

    return render_template('communities.html', communities=communities)


@bp.route('/<community_name>', methods=['GET'])
@login_required
def show_community(community_name):
    community = Community.query.filter_by(name=community_name).scalar()

    return render_template('community.html', community=community)
