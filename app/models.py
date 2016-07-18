# -*- coding: utf-8 -*- 
from . import db
from werkzeug import generate_password_hash, check_password_hash


# 数据库实体
class Role(db.Model):
    """docstring for Role"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    # password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


    @property
    def password(self):
        raise AttributeError('密码不具有可读属性')
    
    @password.setter
    def password(self):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(128))
    text = db.Column(db.Text(4000))

    def __repr__(self):
        return '<Blog %r>' % self.title