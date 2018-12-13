# -*- coding: utf-8 -*- 
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    # 格式为mysql+pymysql://数据库用户名:密码@数据库地址:端口号/数据库的名字?数据库格式
    #如果你不打算使用mysql，使用这个连接sqlite也可以
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'appdb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'jifjaDLAJL@))()KLDJKLjkl'

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base



engine = create_engine('sqlite:///' + os.path.join(BASE_DIR,'appdb.db'),convert_unicode=True)
# metadata = MetaData()
metadata=MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))