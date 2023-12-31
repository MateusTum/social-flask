import os
from flask_login import login_required, current_user
from flask import Blueprint, redirect, url_for, render_template, request, jsonify
from forms import PostForm, CommentForm
from funcs import generate_unique_filename
from models import db
from models.tables import Post, Comment

bp = Blueprint('posts', __name__)


@bp.route("/delete-post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        if current_user in post.authors:
            post.status = 'deleted'
            db.session.commit()
            return redirect(url_for('home.home'))
        else:
            return jsonify({'error': 'Forbidden'}), 403
    else:
        return jsonify({'error': 'Post not found'}), 404


@bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user in post.authors:
        form = PostForm(title=post.title, content=post.content)
        if form.validate_on_submit() and request.method == 'POST':
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            return redirect(url_for('posts.show_post', post_id=post_id))
        return render_template('edit-post.html', form=form)
    else:
        return jsonify({'error': 'Forbidden'}), 403


@bp.route('/like-post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if post:
        if post not in current_user.likes:
            current_user.likes.append(post)
            db.session.commit()
            liked = True
        else:
            current_user.likes.remove(post)
            db.session.commit()
            liked = False
        return jsonify({'likes': post.get_post_likes(), 'liked': liked})
    else:
        return jsonify({'error': 'Post not found'}), 404


@bp.route("/new-post", methods=["GET", "POST"])
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
        return redirect(url_for("home.home"))

    return render_template("new-post.html", create_post_form=create_post_form)


@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@bp.route('/examples')
@login_required
def examples():
    return render_template("examples.html")


@bp.route('/share-post/<int:post_id>', methods=['POST'])
@login_required
def share_post(post_id):
    # post = Post.query.get(post_id)

    return jsonify({'error': 'In progress'})


@bp.route("/post/<int:post_id>/new-comment", methods=["GET", "POST"])
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
        return redirect(url_for("home.home"))
    return render_template("new-comment.html", create_comment_form=create_comment_form)
