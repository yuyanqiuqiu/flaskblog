# _*_ coding:utf-8 _*_ 
#!/usr/bin/python
# Filename:forms.py
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email


class LoginForm(Form):
	email = StringField('Email',validators=[Required(),Length(1,128),
												Email()])
	password = PasswordField('Password',validators=[Required()])
	remember_me = BooleanField('Remember Me?')
	submit = SubmitField('Log In')