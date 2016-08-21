# -*- coding: utf-8 -*- 
from flask import Blueprint
from ..models import Permission

# Blueprint的构造参数包含两个,第一个是蓝图的名称
# 第二个是所在包或者模块,默认__name__即可
main = Blueprint('main',__name__)


# 将枚举类型加入模板，避免每个模板都要导入该类型
@main.app_context_processor
def insert_permission():
    return dict(Permission=Permission)


# 注意，这些模块在 app/main/__init__.py 脚本的末尾导入，
# 这是为了避免循环导入依赖，因为在
# views.py 和 errors.py 中还要导入蓝本 main
from . import views, errors