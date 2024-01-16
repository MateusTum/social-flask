import os
from flask_login import login_required, current_user
from flask import Blueprint, redirect, url_for, render_template, request, jsonify
from forms import PostForm, CommentForm
from funcs import generate_unique_filename
from models import db
from models.tables import Post, Comment, User
from config import ROWS_PER_PAGE
import html
from itsdangerous import URLSafeSerializer
import secrets

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


@bp.route('/like-post', methods=['POST'])
@login_required
def like_post():
    post_id = request.args.get('post_id', 1, type=int)
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

            if len(files) >= 1:
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
    post = Post.query.filter(Post.status == 'active', Post.id == post_id).scalar()
    if post == None:
        return jsonify({'error': 'Post not found'})
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


@bp.route("/post/new-comment", methods=["POST"])
@login_required
def add_new_comment():
    def string_to_html_paragraph(input_string):
        escaped_string = html.escape(input_string)
        html_paragraph = '<p>' + escaped_string.replace('\n', '<br>') + '</p>'
        return html_paragraph

    post_id = request.args.get('post_id')
    create_comment_form = CommentForm()
    current_post = Post.query.get(post_id)
    if create_comment_form.validate_on_submit():
        new_comment = Comment(
            content=string_to_html_paragraph(create_comment_form.content.data),
        )
        db.session.add(new_comment)
        new_comment.author.append(current_user)
        new_comment.post.append(current_post)
        db.session.commit()
        return redirect(url_for("posts.show_post", post_id=post_id))


@bp.route('/delete-comment', methods=['POST'])
@login_required
def delete_comment():
    comment_id = request.args.get('comment_id')
    comment = (Comment.query
    .filter(Comment.id == comment_id)
    .filter(Comment.authors.contains(current_user)))
    if comment == None:
        error = "Comment doesnt exist or user is not the author of the comment"
    else:
        db.remove(comment)
        db.commit()
    return jsonify()

@bp.route('/get_comment_form', methods=['GET'])
@login_required
def get_comment_form():
    post_id = request.args.get('post_id')
    form = CommentForm()
    return jsonify({'form_html': render_template('comment_form.html', form=form, post_id=post_id)})

@bp.route("/load-posts", methods=['GET'])
@login_required
def load_posts():
    page = request.args.get('page', 1, type=int)
    is_user_profile = request.args.get('isUserProfile', type=bool)
    feed_pictures = request.args.get('isFeedPictures', type=bool)

    posts = (Post.query
    .order_by(Post.created_at.desc())
    .filter(Post.status == 'active')
    .paginate(page=page, per_page=ROWS_PER_PAGE))
    page_content =  render_template('more-posts.html', posts=posts)

    if is_user_profile or feed_pictures:
        profileUsername = request.args.get('profileUsername', type=str)
        user = User.query.filter_by(username=profileUsername).scalar()
        posts = (Post.query
        .order_by(Post.created_at.desc())
        .filter(Post.status == 'active', Post.authors.contains(user))
        .paginate(page=page, per_page=ROWS_PER_PAGE))
        
        page_content =  render_template('more-posts.html', posts=posts)

        if feed_pictures:
            user = User.query.filter_by(username=profileUsername).scalar()
            posts = (Post.query
            .order_by(Post.created_at.desc())
            .filter(Post.status == 'active', Post.authors.contains(user), Post.image != None)
            .paginate(page=page, per_page=ROWS_PER_PAGE))
            page_content =  render_template('feed-pictures.html', posts=posts)

    response_data = {
        'content': page_content,
        'last_page': True if page == posts.pages else False,
    }

    return jsonify(response_data)