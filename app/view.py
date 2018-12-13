# -*- coding: utf-8 -*- 
from app import app
from .admin import admin
from .user import user
from .pink import pink
from .cf_pink import cf_pink
from .zy_pink import zy_pink

#这里分别给app注册了两个蓝图admin,user
#参数url_prefix='/xxx'的意思是设置request.url中的url前缀，
#即当request.url是以/admin或者/user的情况下才会通过注册的蓝图的视图方法处理请求并返回
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(pink, url_prefix='/pink')
app.register_blueprint(cf_pink, url_prefix='/cf_pink')
app.register_blueprint(zy_pink, url_prefix='/zy_pink')
