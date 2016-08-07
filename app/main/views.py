# -*- coding: utf-8 -*- 
from datetime import datetime
from flask import render_template, session, request, abort, redirect, url_for
from flask_login import login_required
# .表示同级目录下的__init__.py模块.
# .forms表示同级目录下的 forms模块
# ..models表示上级目录的models模块
# 一个点表示一级目录

from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import User, Permission
from ..decorators import permission_required, admin_required
from flask_login import current_user, flash, redirect


@main.route('/', methods=['GET', 'POST'])
def index():
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
    return render_template('main/name.html', form=form)


@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    show_user = User.query.filter_by(username=username).first()
    if show_user is None:
        abort(404)
    return render_template('main/user.html', user=show_user)


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
        edit_user.role = form.role.data
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
