# _*_ coding:utf-8 _*_ 
#!/usr/bin/python
# Filename:views.py

from flask import render_template, redirect, request, flash, url_for, abort

from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm

from flask_login import login_user, logout_user,login_required

@auth.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			#login_user 是flask-login的方法，将当前用户标记为登陆用户
			login_user(user,form.remember_me.data) 
			next = request.args.get('next')
			if not next_is_valid(next):
				return flask.abort(400)
			return redirect(next or url_for('main.index'))
		flash(u'密码错误')
	return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash(u'成功退出系统')
	return redirect(url_for('main.index'))


@auth.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,
					email = form.email.data,
					password = form.password.data
				)
		db.session.add(user)
		flash(u'注册成功')
		return redirect(url_for('auth.login'))

	return render_template('auth/register.html',form=form)