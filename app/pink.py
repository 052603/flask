# -*- coding: utf-8 -*- 
from app import app,db
from flask import Flask,render_template,request,Blueprint,flash,redirect,url_for,flash,get_flashed_messages
from app.forms import LoginForm,ResetPass,CustomerForm,SearchForm,PinkSearchForm
from flask_login import logout_user,login_user,current_user,login_required
from .models import Old_Active,User,AllProject,Customer,SaleCustomerInfo,Comment,ReadComment
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



pink = Blueprint('pink',__name__)


@pink.route('/pink_index/')
@login_required
def pink_index():
	username = current_user.username
	form = PinkSearchForm()
	pink = User.query.filter_by(username = username).first()
	flag = pink.flag.split(',')
	if '1' not in flag:
		return '权限不足'
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
	return render_template('pink_index.html',form = form,username = username)



@pink.route('/pink_search/',methods=['post'])
@login_required
def pink_search():
	form = PinkSearchForm()
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
	readed = form.c_readed.data
	if readed=='已回复':
		readed = True
	elif readed == '未回复':
		readed = False
	else:
		readed=''
	if request.form.get('time'):
		date = request.form.get('time')
	else:
		date = ""
	sale_name_l = []
	
	search_sale_all = {'sale_name':[form.sale_name.data.strip()],
				'c_name':form.c_name.data.strip(),
				'phone':form.c_phone.data.strip(),
				'project':form.c_project.data.strip(),
				'genre':form.c_type.data.strip(),
				'date_time':date.strip(),
				'readed':readed,
				'school':form.school.data.strip()
				}
	return redirect(url_for('pink.get_page',search_d=search_sale_all))



@pink.route('/page/<search_d>/')
@login_required
def get_page(search_d):
	form = PinkSearchForm()
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
		search_d['genre']="A类,B类,C类"
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
	all_search_cus = Customer.query.order_by(Customer.sale_time.desc()).filter(Customer.sale_name.in_(search_d['sale_name']) if search_d['sale_name'] is not '' else "",
				Customer.c_name.like('%'+search_d['c_name']+'%') if search_d['c_name'] is not '' else "",
				Customer.phone.like('%'+search_d['phone']+'%') if search_d['phone'] is not '' else "",
				Customer.project.like('%'+search_d['project']+'%') if search_d['project'] is not '' else "",
				Customer.genre.in_(search_d['genre'].split(',')) if search_d['genre'] is not '' else "",
				Customer.date_time.like('%'+search_d['date_time']+'%') if search_d['date_time'] is not '' else "",
				Customer.readed==search_d['readed'] if search_d['readed'] is not '' else "")

	
	per_page = 10
	page = request.args.get(get_page_parameter(), type=int, default=1)
	start = (page-1)*per_page
	end = start+per_page
	search_res = all_search_cus.slice(start,end)
	biaoji_l = []
	for search in search_res:
		comments = Comment.query.filter_by(c_name_id=search.id)
		if comments.first():
			for comment in comments:
				if ReadComment.query.filter_by(user=current_user.username,comment_id = comment.id).first() == None:
					biaoji = '未读'
					break
				else:
					if comment.name==current_user.username:
						biaoji = '已评价'
					else:
						biaoji ='已读'
			biaoji_l.append(biaoji)
		else:
			biaoji = '无评价'
			biaoji_l.append(biaoji)
	time_l,school_l,time_zj = last_time(search_res)
	pagination = Pagination(bs_version=3,page=page, total=all_search_cus.count())
	return render_template('pink_search.html',search_res = search_res,form = form,username=current_user.username,search_d = search_d,pagination = pagination,time_l = time_l,biaoji_l = biaoji_l,school_l=school_l,time_zj=time_zj)


def last_time(search_res):
	time_l = []
	school_l = []
	time_zj=[]
	for i in search_res:
		info_l = SaleCustomerInfo.query.order_by(SaleCustomerInfo.id.desc()).filter_by(c_name_id=i.id).first()
		info_zj = SaleCustomerInfo.query.order_by(SaleCustomerInfo.id.desc()).filter(SaleCustomerInfo.c_name_id==i.id,SaleCustomerInfo.pink!=None).first()
		sale = User.query.filter_by(username = i.sale_name).first()
		try:
			time_l.append(info_l.date_time)
		except:

			time_l.append('')
		try:
			school_l.append(sale.school)
			time_zj.append(info_zj.pink_date_time)
		except:
			time_zj.append('')
	return time_l,school_l,time_zj# print(info_l.id)






@pink.route('/replay/<id>/')
@login_required
def replay(id):
	pink = User.query.filter_by(username=current_user.username).first()
	cus = Customer.query.filter_by(id = id).first()
	sale_name = User.query.filter_by(username = cus.sale_name).first()
	if (pink.school=='') or ((sale_name.school in pink.school) and pink.group=='') or ((sale_name.school in pink.school)and pink.group ==sale_name.group):
		cus_info = SaleCustomerInfo.query.order_by(SaleCustomerInfo.id.desc()).filter_by(c_name_id = id)
		comments = Comment.query.filter_by(c_name_id = id)
		old_act = Old_Active.query.order_by(Old_Active.id.desc()).filter(Old_Active.cus_id==id)
		for comment in comments:
			if ReadComment.query.filter_by(cus_id = id,user = current_user.username,comment_id=comment.id).first()==None:
				read = ReadComment()
				read.cus_id = id
				read.user = current_user.username
				read.comment_id = comment.id
				db.session.add(read)
				db.session.commit()
				
		return render_template('replay.html',cus = cus,cus_info = cus_info,username = current_user.username,comments=comments,old_act=old_act)
	else:
		return '您不可以这样访问呦！！！'





@pink.route('/replay_info/<id>/',methods=['post'])
@login_required
def replay_info(id):
	info = request.form.get('pink_info')
	cus_info = SaleCustomerInfo.query.filter_by(id=id).first()
	cus_info.info = info
	cus_info.pink_date_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	cus_info.pink = current_user.username
	cus = Customer.query.filter_by(id=int(cus_info.c_name_id)).first()
	cus.readed = True
	cus.pink_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	cus.pink = current_user.username
	db.session.commit()
	return redirect(url_for('pink.replay',id=cus_info.c_name_id))



@pink.route('/reset/')
@login_required
def saleman_reset():
	username = current_user.username
	form = ResetPass()
	return render_template('pink_reset.html',form = form, username = username)


@pink.route('/psw/',methods=['post'])
@login_required
def psw():
	form = ResetPass()
	saleman = User.query.filter_by(username = current_user.username).first()
	if check_password_hash(saleman.password_hash,form.old_psw.data):
		if form.new_psw.data == form.re_psw.data:
			saleman.password_hash = generate_password_hash(form.new_psw.data)
			db.session.commit()
			flash('修改成功，请重修登录')
			return redirect(url_for('user.saleman_logout'))
		else:
			flash('两次密码不同，请重新输入')
			return redirect(url_for('pink.saleman_reset'))
	else:
		flash('旧密码输入错误，请联系管理员')
		return redirect(url_for('pink.saleman_reset'))

@pink.route('/comment/<info_id>/<c_id>',methods=['post'])
@login_required
def comment(info_id,c_id):
	comment = Comment()
	comment.info_id = info_id
	comment.c_name_id = c_id
	comment.comment = request.form.get('comment')
	comment.name = current_user.username
	db.session.add(comment)
	db.session.commit()
	return redirect(url_for('pink.replay',id=c_id))

