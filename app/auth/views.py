# _*_ coding:utf-8 _*_ 
# !/usr/bin/python
# Filename:views.py

from flask import render_template, redirect, request, flash, url_for, abort

from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm,ChangePasswordForm
from ..email import send_email

from flask_login import login_user, logout_user,login_required, current_user

@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed	\
			and request.endpoint[:5] != 'auth.'	\
			and request.endpoint != 'static':
			return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			#login_user 是flask-login的方法，将当前用户标记为登陆用户
			login_user(user,form.remember_me.data)
			next = request.args.get('next')
			# if not next_is_valid(next):
				# return flask.abort(400)
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
					email=form.email.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()

		send_email(user.email, u'确认您的账户信息','/auth/email/confirm',
					user=user, token=token)

		flash(u'系统已经发送一封确认邮件到您的邮箱，请登录邮箱确认')
		return redirect(url_for('main.index'))

	return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash(u'账户确认成功')
	else:
		flash(u'链接错误或确认已过时')
	return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email,'Confirm your account',
				'auth/email/confirm',user=current_user,token=token)
	flash(u'已经发送一封邮件到您的邮箱，请登录邮箱进行确认')
	return redirect(url_for('main.index'))


@auth.route('/changepassword',methods=['GET','POST'])
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		new_password = form.new_password.data
		if not current_user.verify_password(form.old_password.data):
			flash(u'旧密码不匹配')
		else:
			current_user.password = new_password
			db.session.add(current_user)
			flash(u'修改密码成功')
			return redirect(url_for('main.index'))

	return render_template('auth/change_password.html',form=form)