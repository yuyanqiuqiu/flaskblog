# _*_ coding:utf-8 _*_ 
#!/usr/bin/python
# Filename:forms.py
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
	email = StringField(u'邮箱',validators=[Required(),Length(6,128),
											Email()])
	password = PasswordField(u'密码',validators=[Required()])
	remember_me = BooleanField(u'记住我?')
	submit = SubmitField(u'登录')


class RegistrationForm(Form):
	email = StringField(u'邮箱',validators=[Required(),Length(6,128)
											,Email()])
	username = StringField(u'用户名',validators=[Required(),Length(1,64),
							Regexp('^[A-Za-z][A-Za-z0-9._]*$',0,
								u'用户名只能是字母数字小数点和下划线')]
							)
	password = PasswordField(u'密码',validators=[Required(),
							EqualTo('password2',message=u'两次密码必须一致')])
	password2 = PasswordField(u'确认密码',validators=[Required()])

	submit = SubmitField(u'注册')


	# 自定义校验方法，格式为 vaidate_字段名，传入的参数是self及字段本身
	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError(u'该邮箱已经被注册了')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'该用户名已经被占用了')


class ChangePasswordForm(Form):
	old_password = PasswordField(u'旧密码',validators=[Required()])
	new_password = PasswordField(u'新密码',validators=[Required(),
								EqualTo('new_password2',message=u'两次密码必须保持一致')])
	new_password2 = PasswordField(u'确认密码',validators=[Required()])
	submit = SubmitField(u'保存')