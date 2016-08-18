# -*- coding: utf-8 -*- 

from ..models import Role, User

from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, \
    BooleanField, SelectField
from wtforms.validators import Required, Length, \
    Email, Regexp, ValidationError
from flask_pagedown.fields import PageDownField


class NameForm(Form):
    name = StringField(u'用户名', validators=[Required()])
    submit = SubmitField(u'提交')


class EditProfileForm(Form):
    name = StringField(u'实际名称', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'自我介绍')
    submit = SubmitField(u'保存')


class EditProfileAdminForm(Form):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[Required(), Length(1, 64),
                                               Regexp('^[a-zA-Z][a-zA-Z0-9_.]*$', 0,
                                                      u'用户名必须以字母或下划线开头')])
    confirmed = BooleanField(u'是否激活')
    role = SelectField(u'用户角色', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'自我介绍')
    submit = SubmitField(u'保存')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册了')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.queyr.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被占用了')


class PostForm(Form):
    body = PageDownField(u'说点啥?', validators=[Required()])
    submit = SubmitField(u'发表')