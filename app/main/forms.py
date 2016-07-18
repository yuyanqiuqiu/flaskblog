# -*- coding: utf-8 -*- 

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
	name = StringField(u'用户名',validators=[Required()])
	submit = SubmitField(u'提交')