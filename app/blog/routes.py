from flask import render_template, request
from flask_login import current_user

from . import blog_blueprint
from app.models import Post


@blog_blueprint.route('/')
@blog_blueprint.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 10, False)

    if current_user.is_authenticated:
        return render_template(
            'blog/index.html', posts=posts, user=current_user
        )

    return render_template('blog/index.html', posts=posts)


@blog_blueprint.route('/post/<_id>')
def post(_id):
    single_post = Post.query.filter_by(id=_id).first_or_404()
    return render_template('blog/post.html', post=single_post)
