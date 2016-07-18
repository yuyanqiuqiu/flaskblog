# -*- coding: utf-8 -*- 
from flask import Blueprint

# Blueprint的构造参数包含两个,第一个是蓝图的名称
# 第二个是所在包或者模块,默认__name__即可
main = Blueprint('main',__name__)


# 注意，这些模块在 app/main/__init__.py 脚本的末尾导入，
# 这是为了避免循环导入依赖，因为在
# views.py 和 errors.py 中还要导入蓝本 main
from . import views, errors