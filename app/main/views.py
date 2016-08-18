# -*- coding: utf-8 -*-


# .表示同级目录下的__init__.py模块.
# .forms表示同级目录下的 forms模块
# ..models表示上级目录的models模块
# 一个点表示一级目录

from flask import render_template, session, request, abort, redirect, \
    url_for, current_app
from flask_login import login_required

from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, \
    PostForm
from .. import db
from ..models import User, Permission, Post, Role, Follow
from ..decorators import permission_required, admin_required
from flask_login import current_user, flash, redirect


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('main/index.html', form=form, posts=posts,pagination=pagination)


@main.route('/post/<int:id>')
def post(id):
    single_post = Post.query.get_or_404(id)
    return render_template('main/post.html', posts=[single_post])


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    single_post = Post.query.get_or_404(id)
    if current_user != single_post.author and \
        not current_user.can(Permission.ADMINSTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        single_post.body = form.body.data
        db.session.add(single_post)
        flash(u'修改成功')
        return redirect(url_for('.post', id=id))
    form.body.data = single_post.body
    return render_template('main/edit_post.html', form=form)


@main.route('/newuser', methods=['GET', 'POST'])
def new_user():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        user = User.query.filter_by(username=name).first()
        if user is None:
            user = User(username=name)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        # send_email('test@example.com','New User','new_user',new_user_name=name)
        else:
            session['known'] = True
        session['name'] = name
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('main/newuser.html', form=form)


@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    show_user = User.query.filter_by(username=username).first()
    if show_user is None:
        abort(404)
    posts = Post.query.filter_by(author_id=show_user.id).order_by(Post.timestamp.desc()).all()
    return render_template('main/user.html', user=show_user, posts=posts)


@main.route('/unfollow/<username>')
def unfollow(username):
    u = current_user.followed.filter_by(username=username)
    if u is not None:
        db.session.delete(u)
    return redirect(url_for('.user', username=username))


@main.route('/follow/<username>')
def follow(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        flash(u'未找到指定用户')
        return redirect(url_for('.index'))
    if current_user.is_following(u):
        flash(u'你已经关注他了')
        return redirect('.user', username=username)
    current_user.follow(u)
    flash(u'关注了{0}'.format(username))
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    return redirect(url_for('.user', username=username))


@main.route('/followed_by/<username>')
def followed_by(username):
    return redirect(url_for('.user', username=username))


@main.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'修改资料成功')
        return redirect(url_for('.user', username=current_user.username))

    form.name.data = current_user.name
    form.about_me.data = current_user.about_me
    form.location.data = current_user.location
    return render_template('main/edit_profile.html', form=form)


@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    edit_user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=edit_user)
    if form.validate_on_submit():
        edit_user.email = form.email.data
        edit_user.username = form.username.data
        edit_user.name = form.name.data
        edit_user.about_me = form.about_me.data
        edit_user.location = form.location.data
        # 下面的role必须赋值一个实体,如果直接赋值form.role.data会报错
        # int object has no attribute _sa_instance_state
        edit_user.role = Role.query.get(form.role.data)
        edit_user.confirm = form.confirmed.data

        db.session.add(edit_user)
        flash(u'修改用户信息成功')
        return redirect(url_for('.user', username=edit_user.username))

    form.email.data = edit_user.email
    form.username.data = edit_user.username
    form.name.data = edit_user.name
    form.location.data = edit_user.location
    form.about_me.data = edit_user.about_me
    form.role.data = edit_user.role
    form.confirmed.data = edit_user.confirm

    return render_template('main/edit_profile_admin.html', form=form)


# =========================测试部分=========================================
@main.route('/secret', methods=['GET', 'POST'])
@login_required
def secret():
    return '只有登陆用户才可以看到内容'


@main.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def for_admins_only():
    return u'超级管理员页面'


@main.route('/moderator', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return u'管理员管理评论页面'
# ===================================================================