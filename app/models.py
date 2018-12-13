# -*- coding: utf-8 -*- 
from datetime import datetime
from app import db
from flask_login import UserMixin


class Log(db.Model):
    __tablename__='log'
    id = db.Column(db.Integer,primary_key=True)
    sale_name = db.Column(db.String())
    phone = db.Column(db.String())
    date_time = db.Column(db.String())


class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    school = db.Column(db.String())
    group = db.Column(db.String())
    username = db.Column(db.String(128),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    flag = db.Column(db.String())



class Customer(db.Model):
    """docstring for Customer"""
    __tablename__ = 'customer'
    id = db.Column(db.Integer,primary_key=True)
    c_name = db.Column(db.String())
    phone = db.Column(db.String())
    project = db.Column(db.String())
    genre = db.Column(db.String())
    sale_name = db.Column(db.String())
    price_banci = db.Column(db.String())
    date_time = db.Column(db.String())	
    readed = db.Column(db.Boolean())   
    pink = db.Column(db.String()) 
    sale_time = db.Column(db.String())
    pink_time = db.Column(db.String())
        

class SaleCustomerInfo(db.Model):
    """docstring for Kehu"""
    __tablename__ = 'salecustomerinfo'
    id = db.Column(db.Integer,primary_key=True)
    c_name_id = db.Column(db.String())
    dongtai = db.Column(db.Text())
    next_phone = db.Column(db.Text())
    info = db.Column(db.Text())
    date_time = db.Column(db.Text())
    pink_date_time = db.Column(db.Text())
    pink = db.Column(db.String())
    sale_name = db.Column(db.String())



class AllProject(db.Model):
    __tablename__ = 'all_project'
    id = db.Column(db.Integer,primary_key=True)
    project = db.Column(db.String())


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True)
    info_id = db.Column(db.Integer)
    c_name_id = db.Column(db.Integer)
    comment = db.Column(db.String())
    name = db.Column(db.String())
    date_time = db.Column(db.DateTime, default=datetime.now)


class ReadComment(db.Model):
    __tablename__ = 'readcomment'
    id = db.Column(db.Integer,primary_key=True)
    cus_id = db.Column(db.Integer)
    user = db.Column(db.String())
    comment_id = db.Column(db.Integer)


class Old_Active(db.Model):
    __tablename__ = 'old_active'
    id = db.Column(db.Integer,primary_key=True)
    cus_id = db.Column(db.Integer)
    old_genre = db.Column(db.String())
    old_banci = db.Column(db.String())
    date_time = db.Column(db.DateTime, default=datetime.now)