from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from . import admin_blueprint
from .forms import LoginForm, CreateForm
from app import db
from app.models import User, Post, Tag
from app.utils import title_to_url


@admin_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog.index'))


@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin.login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('blog.index')

        return redirect(next_page)

    return render_template('admin/login.html', title='Sign In', form=form)


@admin_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateForm()

    tags = Tag.query.all()
    form.tags.choices = [(t.id, t.text) for t in tags]

    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data
        post.body = form.body.data
        post.user_id = current_user.id
        post.url = title_to_url(form.title.data)

        tags = []
        for tag in form.tags.data:
            t = Tag.query.filter_by(text=tag).first()
            if t is None:
                t = Tag(text=tag)
            tags.append(t)

        post.tags = tags

        db.session.add(post)
        db.session.commit()
        flash('Post created!')

        return redirect(url_for('blog.index'))

    return render_template(
        'admin/create.html', title='Create post', form=form
    )


@admin_blueprint.route('/update/<post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):
    existing = Post.query.filter_by(id=post_id).first_or_404()
    form = CreateForm(obj=existing)

    tags = Tag.query.all()
    form.tags.choices = [(t.id, t.text) for t in tags]

    if form.validate_on_submit():
        post = Post.query.filter_by(id=post_id).first_or_404()

        post.title = form.title.data
        post.body = form.body.data
        post.user_id = current_user.id
        post.url = title_to_url(form.title.data)

        tags = []
        for tag in form.tags.data:
            try:
                t = Tag.query.filter_by(id=int(tag)).first()
            except ValueError:
                t = Tag.query.filter_by(text=tag).first()
                if t is None:
                    t = Tag(text=tag)
            tags.append(t)

        post.tags = tags

        db.session.commit()
        flash('Post updated!')

        return redirect(url_for('blog.index'))

    return render_template(
        'admin/update.html', title='Update post', form=form
    )


@admin_blueprint.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted!')
    return redirect(url_for('blog.index'))
