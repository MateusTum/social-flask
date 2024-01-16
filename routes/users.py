import os
from flask import Blueprint, redirect, url_for, render_template, request, jsonify
from flask_login import current_user, login_required
from forms import UserProfileForm, FollowForm
from funcs import generate_unique_filename
from config import ROWS_PER_PAGE
from models import db
from models.tables import User, Post

bp = Blueprint('users', __name__)


@bp.route('/edit-profile', methods=['GET', 'POST'])
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
                upload_path = os.path.join(f'static/uploads/{current_user.username}/pictures/profile/',
                                           user_profile_img.filename)
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
            return redirect(url_for('users.show_profile', username=user.username))
        return render_template('edit-profile.html', form=form)
    else:
        return jsonify({'error': 'Profile not found'}), 404


@bp.route('/follow/<int:user_id_to_follow>', methods=['POST'])
@login_required
def follow_user(user_id_to_follow):
    form = FollowForm(user_id=user_id_to_follow)
    user_to_follow = User.query.get_or_404(user_id_to_follow)
    if form.validate_on_submit():
        if current_user in user_to_follow.followers.all():
            current_user.followed.remove(user_to_follow)
            db.session.commit()
            return jsonify(
                {
                "message": f"You have unfollowed {user_to_follow.username}",
                "following_status": False
                }
                ), 200
        else:
            current_user.followed.append(user_to_follow)
            db.session.commit()
            return jsonify(
                {
                "message": f"You are now following {user_to_follow.username}",
                "following_status": True
                }
                ), 200

    # If form validation fails, return an error response
    return jsonify({'error': 'Invalid form data'}), 400



@bp.route('/profile/<username>', methods=['GET'])
@login_required
def show_profile(username):
    form = FollowForm(request.form)
    user = User.query.filter_by(username=username).scalar()
    followers = user.followers.all()
    following = user.followed.all()
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
        return render_template('profile.html', user=user, profile_posts=profile_posts, followers=followers,
                               following=following, form=form)
