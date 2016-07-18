# -*- coding: utf-8 -*- 
import os
basedir = os.path.abspath(os.path.dirname(__file__))

print basedir

class Config():
	# 生成防CSRF攻击串
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'b\x1c\x90\xe0\xa7\x847\x84'
	# 数据库提交
	SQLALCHEMY_COMMIT_TEARDOWN = True
	# 邮件相关 
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'Flasky Admin <new619@163.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
				'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')



class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI =  os.environ.get('TEST_DATABASE_URL') or \
				'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URL') or \
				'sqlite:///' + os.path.join(basedir, 'data.sqlite')



config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}