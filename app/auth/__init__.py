# _*_ coding:utf-8 _*_ 
#!/usr/bin/python

from flask import Blueprint

auth = Blueprint('auth',__name__)

from . import views