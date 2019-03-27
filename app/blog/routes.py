from flask import render_template, request, redirect, url_for
from flask_login import current_user

from . import blog_blueprint
from app.models import Post


@blog_blueprint.route('/')
@blog_blueprint.route('/index')
def index():
    tag = request.args.get('tag', None, type=str)
    title = request.args.get('title', None, type=str)
    page = request.args.get('page', 1, type=int)

    if tag is not None:
        posts = Post.query.order_by(Post.timestamp.desc()).filter(Post.tags.any(text=tag)).paginate(page, 10, False)
    elif title is not None:
        posts = Post.query.order_by(Post.timestamp.desc()).filter(Post.title.ilike(title)).paginate(page, 10, False)
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 10, False)

    if current_user.is_authenticated:
        return render_template(
            'blog/index.html', posts=posts, user=current_user
        )

    return render_template('blog/index.html', posts=posts)


@blog_blueprint.route('/search', methods=['POST'])
def search():
    title = request.form.get("post_title")
    if title is None:
        return redirect(url_for('blog.index'))
    return redirect(url_for('blog.index', title=f'%{title}%'))


@blog_blueprint.route('/post/<url_title>')
def post(url_title):
    single_post = Post.query.filter_by(url=url_title).first_or_404()
    return render_template('blog/post.html', post=single_post)
