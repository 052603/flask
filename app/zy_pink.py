# -*- coding: utf-8 -*- 
from app import app,db
from flask import Flask,render_template,request,Blueprint,flash,redirect,url_for,flash,get_flashed_messages
from app.forms import LoginForm,ResetPass,CustomerForm,SearchForm,PinkSearchForm,CfPinkSearchForm,ZyPinkSearchForm
from flask_login import logout_user,login_user,current_user,login_required
from .models import User,AllProject,Customer,SaleCustomerInfo,Comment,ReadComment
from . import loginmanager
from sqlalchemy import and_,or_
import time
import json
from flask_paginate import Pagination, get_page_parameter
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from datetime import timedelta
import sys
sys.setrecursionlimit(1000000)



zy_pink = Blueprint('zy_pink',__name__)




@zy_pink.route('/zhuanyi/')
@login_required
def zhuanyi():
	
	username = current_user.username
	pink = User.query.filter_by(username = username).first()
	flag = pink.flag.split(',')
	if 'zy' not in flag:
		return '权限不足'
	if (pink.school == '' and pink.group == ''):
		sales = User.query.filter(User.flag.contains('0'))
	elif (pink.group == '' and pink.school !=''):
		school = pink.school.split(',')
		sales = User.query.filter(User.flag.contains('0'),User.school.in_(school))
	elif (pink.group != '' and pink.school != ''):
		school = pink.school.split(',')
		sales = User.query.filter(User.flag.contains('0'),User.school.in_(school),User.group == pink.group)
	form = ZyPinkSearchForm()
	school = pink.school.split(',')
	form.school.choices = [('','')]+[(a,a) for a in school]
	form.c_project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
	form.sale_name.choices = [('','')]+[(a.username,a.username) for a in sales]
	return render_template('zy_pink_index.html',form = form,username = username)




@zy_pink.route('/pink_search/',methods=['post'])
@login_required
def pink_search():
	form = ZyPinkSearchForm()
	pink = User.query.filter_by(username = current_user.username).first()
	if (pink.school == '' and pink.group == ''):
		sales = User.query.filter(User.flag.contains('0'))
	elif (pink.group == '' and pink.school !=''):
		school = pink.school.split(',')
		sales = User.query.filter(User.flag.contains('0'),User.school.in_(school))
	elif (pink.group != '' and pink.school != ''):
		school = pink.school.split(',')
		sales = User.query.filter(User.flag.contains('0'),User.school.in_(school),User.group == pink.group)
	school = pink.school.split(',')
	form.school.choices = [('','')]+[(a,a) for a in school]
	form.c_project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
	form.sale_name.choices = [('','')]+[(a.username,a.username) for a in sales]
	if request.form.get('time'):
		date = request.form.get('time')
	else:
		date = ""
	search_sale_all = {'sale_name':[form.sale_name.data.strip()],
				'c_name':form.c_name.data.strip(),
				'phone':form.c_phone.data.strip(),
				'project':form.c_project.data.strip(),
				'genre':form.c_type.data.strip(),
				'date_time':date.strip(),
				'school':form.school.data.strip()
				}
	
	if form.sale_name.data:
		choices_name = form.sale_name.data.strip()
	else:
		choices_name = 'no_choice'
	return redirect(url_for('zy_pink.get_page',search_d=search_sale_all,choices_name=choices_name))



@zy_pink.route('/page/<search_d>/<choices_name>')
@login_required
def get_page(search_d,choices_name):
	form = ZyPinkSearchForm()
	pink = User.query.filter_by(username = current_user.username).first()
	if (pink.school == '' and pink.group == ''):
		sales = User.query.filter(User.flag.contains('0'))
	elif (pink.group == '' and pink.school !=''):
		school = pink.school.split(',')
		sales = User.query.filter(User.flag.contains('0'),User.school.in_(school))
	elif (pink.group != '' and pink.school != ''):
		school = pink.school.split(',')
		sales = User.query.filter(User.flag.contains('0'),User.school.in_(school),User.group == pink.group)
	school = pink.school.split(',')
	form.school.choices = [('','')]+[(a,a) for a in school]
	form.c_project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
	form.sale_name.choices = [('','')]+[(a.username,a.username) for a in sales]
	search_d = eval(search_d)
	if search_d['genre']=='':
		search_d['genre']="已成交,A类,B类,C类,放弃"
	sale_name_l=[]
	if search_d['sale_name']==['']:
		if search_d['school']!='':
			for a in sales:
				if a.school==search_d['school']:
					sale_name_l.append(a.username)
		else:
			for a in sales:
				sale_name_l.append(a.username)

		search_d['sale_name'] = sale_name_l
	else:
		for a in sales:
				sale_name_l.append(a.username)
	all_search_cus = Customer.query.order_by(Customer.id.desc()).filter(Customer.sale_name.in_(search_d['sale_name']) if search_d['sale_name'] is not '' else "",
				Customer.c_name.like('%'+search_d['c_name']+'%') if search_d['c_name'] is not '' else "",
				Customer.phone.like('%'+search_d['phone']+'%') if search_d['phone'] is not '' else "",
				Customer.project.like('%'+search_d['project']+'%') if search_d['project'] is not '' else "",
				Customer.genre.in_(search_d['genre'].split(',')) if search_d['genre'] is not '' else "",
				Customer.date_time.like('%'+search_d['date_time']+'%') if search_d['date_time'] is not '' else "")
	per_page = 10
	page = request.args.get(get_page_parameter(), type=int, default=1)
	start = (page-1)*per_page
	end = start+per_page
	search_res = all_search_cus.slice(start,end)
	
	time_l,time_ruku,school_l = last_time(search_res)
	pagination = Pagination(bs_version=3,page=page, total=all_search_cus.count())
	return render_template('zy_pink_search.html',school_l=school_l,search_res = search_res,form = form,username=current_user.username,search_d = search_d,pagination = pagination,time_l = time_l,time_ruku=time_ruku,sale_name_l=sale_name_l,choices_name=choices_name)


def last_time(search_res):
	time_l = []
	time_ruku = []
	school_l = []
	for i in search_res:
		info_l = SaleCustomerInfo.query.order_by(SaleCustomerInfo.id.desc()).filter_by(c_name_id=i.id).first()
		info_ruku = SaleCustomerInfo.query.order_by(SaleCustomerInfo.id).filter_by(c_name_id=i.id).first()
		sale = User.query.filter_by(username = i.sale_name).first()
		school_l.append(sale.school)
		try:
			time_l.append(info_l.date_time)
		except:
			time_l.append('')
		try:
			time_ruku.append(info_ruku.date_time)
		except:
			time_ruku.append('')

		
	return time_l,time_ruku,school_l# print(info_l.id)


@zy_pink.route('/cus_move/<choices_name>/<search_d>/',methods=['post','get'])
@login_required
def cus_move(choices_name,search_d):
	if choices_name!='no_choice':
		xz = request.form.get('xz')
		print(xz)
		if xz==None:
			cuss = request.form.getlist('select')
			for id in cuss:
				cus = Customer.query.filter_by(id=id).first()
				cus.sale_name = request.form.get('sale')
				db.session.commit()
		else:
			cuss = Customer.query.filter_by(sale_name=choices_name)
			for cus in cuss:
				cus.sale_name = request.form.get('sale')
				db.session.commit()
	else:
		cuss = request.form.getlist('select')
		for id in cuss:
			cus = Customer.query.filter_by(id=id).first()
			cus.sale_name = request.form.get('sale')
			db.session.commit()
	# else:
	# 	cuss = Customer.query.filter_by(sale_name=)
	return redirect(url_for('zy_pink.get_page',search_d=search_d,choices_name=choices_name))