from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.models import User, Post, Tag
from app.forms import LoginForm, CreateForm


@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 10, False)

    if current_user.is_authenticated:
        return render_template(
            'index.html', title='Home', posts=posts, user=current_user
        )

    return render_template('index.html', posts=posts)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    tags = Tag.query.all()
    form = CreateForm()

    form.tags.choices = [(t.id, t.text) for t in tags]

    if form.validate_on_submit():

        new_post = Post(
            title=form.title.data, body=form.body.data, user_id=current_user.id
        )

        for tag in form.tags.data:
            t = Tag.query.filter_by(text=tag).first()
            if t is None:
                t = Tag(text=tag)

            new_post.tags.append(t)

        db.session.add(new_post)
        db.session.commit()
        flash('Post created!')

        return redirect(url_for('index'))

    return render_template('create.html', title='Create a post', form=form)


@app.route('/post/<_id>')
def post(_id):
    single_post = Post.query.filter_by(id=_id).first_or_404()
    return render_template('post.html', post=single_post)
