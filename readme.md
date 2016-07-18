
**migrations文件夹是根据脚本生成的,而不是事先建立**

####env.py配置里增加如下行
render_as_batch=True, # 解决命令行执行sql更新的错误

1. python manage.py db init # 创建migration文件夹

2. python manage.py db migrate # 生成migration的sql文件

3. python hello.py db upgrade # 更新数据库