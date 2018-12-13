#从app模块中即从__init__.py中导入创建的app应用
# -*- coding: utf-8 -*- 
from app import app,db
from flask import jsonify,Flask,render_template,request,Blueprint,flash,redirect,url_for,flash,get_flashed_messages
from app.forms import LoginForm,ResetPass,CustomerForm,SearchForm
from flask_login import logout_user,login_user,current_user,login_required
from .models import User,AllProject,Customer,SaleCustomerInfo,Log,Comment,ReadComment,Old_Active
from . import loginmanager
from sqlalchemy import and_,or_
import datetime
import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_paginate import Pagination, get_page_parameter
from config import db_session


user = Blueprint('user',__name__)
#建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。


@loginmanager.user_loader
def load_user(id):
	return User.query.get(int(id))


@user.route('/')
def login_index():
	if current_user.is_authenticated:
		return redirect(url_for('user.saleman_index',city='全部'))
	else:
		form = LoginForm()
		return render_template('login_bak.html', form=form)
	# return '1111111111'




@user.route('/index/')
def user_index():
	if current_user.is_authenticated:
		return redirect(url_for('user.saleman_index',city='全部'))
	else:
		return redirect(url_for('user.login_index'))



@user.route('/online/<city>/')
@login_required
def saleman_index(city):

	username=current_user.username
	user = User.query.filter_by(username = username).first()
	school = user.school.split(',')
	if '1' in user.flag:
		if city == '全部':
			if len(school)==1:
				res_sql = "SELECT sale_name,genre,count(*) FROM customer aa inner join [user] bb on aa.sale_name=bb.username where school in ('{}') GROUP BY sale_name,genre".format(school[0])
				res = get_res(res_sql)
				d = to_dict(res.fetchall())
				cj_sql = "SELECT sale_name,project,count(*) FROM customer aa inner join [user] bb on aa.sale_name=bb.username WHERE genre='已成交' and school in ('{}') GROUP BY sale_name,project".format(school[0])
				res_cj = get_res(cj_sql)
				count = d_add(d,res_cj.fetchall())
			else:
				cj_sql ="SELECT sale_name,project,count(*) FROM customer aa inner join [user] bb on aa.sale_name=bb.username WHERE genre='已成交' and school in {} GROUP BY sale_name,project".format(tuple(school))
				res_sql = "SELECT sale_name,genre,count(*) FROM customer aa inner join [user] bb on aa.sale_name=bb.username where school in {} GROUP BY sale_name,genre".format(tuple(school))
				res = get_res(res_sql)
				d = to_dict(res.fetchall())
				res_cj = get_res(cj_sql)
				count = d_add(d,res_cj.fetchall())
			# count=to_dict(res.fetchall(),res_cj.fetchall())
		else:
			res_sql = "SELECT sale_name,genre,count(*) from customer  where sale_name in (SELECT username FROM [user] where school like '%{}%') GROUP BY sale_name,genre".format(city)
			cj_sql ="SELECT sale_name,project,count(*) from customer  where genre='已成交' and sale_name in (SELECT username FROM [user] where school like '%{}%')  GROUP BY sale_name,project".format(city)
			res = get_res(res_sql)
			d = to_dict(res.fetchall())
			res_cj = get_res(cj_sql)
			count = d_add(d,res_cj.fetchall())
	else:
		res_sql =  "SELECT sale_name,genre,count(*) from customer where sale_name='{}' GROUP BY sale_name,genre".format(username) 
		cj_sql ="SELECT sale_name,project,count(*) from customer  where sale_name='{}' and genre='已成交' GROUP BY sale_name,project".format(username)
		res = get_res(res_sql)
		d = to_dict(res.fetchall())
		res_cj = get_res(cj_sql)
		count = d_add(d,res_cj.fetchall())
	return render_template('index.html',saleman = user,username = username,count = count,school=school,city=city)

def get_res(sql):
	s = db_session()
	res = s.execute(sql)
	s.close
	return res

def to_dict(res):
	name = set([i[0] for i in res])
	d={}
	for i in name:
		d[i]=['','','','','','','','','','','','','','']
	for i in res:
		name = i[0]
		if i[1]=='已成交':
			d[name][0]=i[2]
		elif d[name][0]=='':
			d[name][0]=0
			cj = 0
		if i[1]=='A类':
			d[name][1]=i[2]
		elif d[name][1]=='':
			d[name][1]=0
		if i[1]=='B类':
			d[name][2]=i[2]
		elif d[name][2]=='':
			d[name][2]=0
		if i[1]=='C类':
			d[name][3]=i[2]
		elif d[name][3]=='':
			d[name][3]=0
		if i[1]=='放弃':
			d[name][4]=i[2]
		elif d[name][4]=='':
			d[name][4]=0
		all_count = d[name][0]+d[name][1]+d[name][2]+d[name][3]+d[name][4]
		d[name][5]=all_count
		if '' not in d[name][0:6]:
			user = User.query.filter_by(username=name).first()
			d[name][6] = user.school
	return d
def d_add(d,res_cj):
	for i in res_cj:
		name = i[0]
		if '一建' in i[1]:
			try:
				d[name][7]=i[2]
			except:
				d[name][7]=0
		elif d[name][7]=='':
			d[name][7]=0
		if '二建' in i[1]:
			try:
				d[name][8]=i[2]
			except:
				d[name][8]=0
		elif d[name][8]=='':
			d[name][8]=0
		if '消防' in i[1]:
			try:
				d[name][9]=i[2]
			except:
				d[name][9]=0
		elif d[name][9]=='':
			d[name][9]=0
		if '监理' in i[1]:
			try:
				d[name][10]=i[2]
			except:
				d[name][10]=0
		elif d[name][10]=='':
			d[name][10]=0
		if '安全' in i[1]:
			try:
				d[name][11]=i[2]
			except:
				d[name][11]=0
		elif d[name][11]=='':
			d[name][11]=0
		if '造价' in i[1]:
			try:
				d[name][12]=i[2]
			except:
				d[name][12]=0
		elif d[name][12]=='':
			d[name][12]=0
		if '学历' in i[1]:
			try:
				d[name][13]=i[2]
			except:
				d[name][13]=0
		elif d[name][13]=='':
			d[name][13]=0
	for key,value in d.items():
		if d[key][0] == 0.0:
			for i in range(7,14):
				d[key][i]=0
	return d

@user.route('/sort/<d>/<index>/<city>/')
@login_required
def dict_sort(d,index,city):
	d = eval(d)
	index = int(index)
	username=current_user.username
	user = User.query.filter_by(username = username).first()
	school = user.school.split(',')
	items=d.items()
	backitems=[[v[1][index],v[0]] for v in items] 
	backitems.sort(reverse=True) 
	d_sort = [ backitems[i][1] for i in range(0,len(backitems))]
	count={}
	for i in d_sort:
		count[i]=d[i]
	return render_template('index.html',saleman = user,username = username,count = count,school=school,city=city)





@user.route('/login/',methods=['post'])
def saleman_login():
	form=LoginForm()
	saleman=User.query.filter_by(username=form.username.data).first()
	if form.validate_on_submit():
		if saleman.username == 'admin' and check_password_hash(saleman.password_hash,form.password.data):
			login_user(saleman,True)
			return redirect(url_for('admin.admin_index'))
		if saleman is not None and (check_password_hash(saleman.password_hash,form.password.data)):
			login_user(saleman,True)
			if form.password.data=='000000' and (check_password_hash(saleman.password_hash,form.password.data)):
				flash('密码为初始密码，请修改')
				return redirect(url_for('user.saleman_reset'))
			return redirect(url_for('user.saleman_index',city='全部'))
			
		else:
			flash('用户名或密码错误，请重新输入')
			return redirect(url_for('user.login_index'))
			


@user.route('/logout/')
def saleman_logout():
	logout_user()
	return redirect(url_for('user.login_index'))



@user.route('/reset/')
@login_required
def saleman_reset():
	username = current_user.username
	form = ResetPass()
	return render_template('reset.html',form = form, username = username)


@user.route('/psw/',methods=['post'])
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
			return redirect(url_for('user.saleman_reset'))
	else:
		flash('旧密码输入错误，请联系管理员')
		return redirect(url_for('user.saleman_reset'))



@user.route('/add_cus_form/')
@login_required
def add_cus_form():
	username = current_user.username
	sale = User.query.filter_by(username = username).first()
	flag = sale.flag.split(',')
	if '0' not in flag:
		return '权限不足'
	form = CustomerForm()
	# form.project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
	return render_template('add_cus_form.html',form = form,username = current_user.username)


@user.route('/add_cus/',methods = ['post'])
@login_required
def add_cus():
	form = CustomerForm()
	username = current_user.username
	customer = Customer()
	customer.c_name = form.name.data
	customer.phone = form.phone.data
	if len(customer.phone)!=11:
		flash('手机号不足11位')
		return redirect(url_for('user.add_cus_form'))
	if len(request.form.getlist('project'))==0:
		flash('项目不能为空')
		return redirect(url_for('user.add_cus_form'))
	if request.form.get('genre')==None:
		flash('类型不能为空')
		return redirect(url_for('user.add_cus_form'))
	if form.price_banci.data=='':
		flash('价格班次不能为空')
		return redirect(url_for('user.add_cus_form'))
	search_p = {
				'phone':form.phone.data,
				'date_time':str(datetime.date.today())
	}
	if Customer.query.filter_by(**search_p).count():
		flash('客户今日已入库')
		return redirect(url_for('user.add_cus_form'))
	project_l = request.form.getlist('project')
	project = '，'.join(project_l)
	customer.project = project	
	customer.genre = request.form.get('genre')
	customer.sale_name = current_user.username
	customer.date_time = str(datetime.date.today())
	customer.price_banci = form.price_banci.data
	customer.readed = False
	db.session.add(customer)
	db.session.commit()
	search_all = {'c_name':form.name.data,
				'phone':form.phone.data,
				'project':project,
				'genre':request.form.get('genre'),
				'sale_name':current_user.username,
				'date_time':str(datetime.date.today())
				}

	search_d = dict((key,value)for key,value in search_all.items() if value!='')
	cus = Customer.query.filter_by(**search_d).first()
	return redirect(url_for('user.one_info',id = cus.id))

@user.route('/one_info/<id>')
@login_required
def one_info(id):
	form = CustomerForm()
	form.project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
	customer = Customer.query.filter_by(id = id).first()
	form.project.data = customer.project
	form.c_type.data = customer.genre
	sale_cus_info = SaleCustomerInfo.query.filter_by(c_name_id=id)
	search_d={}
	return render_template('one_info.html',customer = customer,form = form,sale_cus_info = sale_cus_info,username = current_user.username,search_d = search_d)





@user.route('/search/',methods=['post','get'])
@login_required
def seacher():
	username = current_user.username
	sale = User.query.filter_by(username = username).first()
	flag = sale.flag.split(',')
	if '0' not in flag:
		return '权限不足'
	form = SearchForm()
	form.c_project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
	if request.form.get('time'):
		date = request.form.get('time')
	else:
		date = ''
	search_all = {
				'c_name':form.c_name.data,
				'phone':form.c_phone.data,
				'project':form.c_project.data,
				'genre':form.c_type.data,
				'date_time':date,
				}

	# search_d = dict((key,value)for key,value in search_all.items() if value!='')
	return redirect(url_for('user.get_page',search_d=search_all))


@user.route('/page/<search_d>/')
@login_required
def get_page(search_d):
	form = SearchForm()
	form.c_project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
	search_d = eval(search_d)
	if search_d['genre']=='':
		search_d['genre']="A类,B类,C类"
	all_search_cus = Customer.query.order_by(Customer.pink_time.desc()).filter(
				Customer.c_name.like('%'+search_d['c_name']+'%') if search_d['c_name'] is not '' else "",
				Customer.phone.like('%'+search_d['phone'].strip()+'%') if search_d['phone'] is not '' else "",
				Customer.project.like('%'+search_d['project']+'%') if search_d['project'] is not '' else "",
				Customer.genre.in_(search_d['genre'].split(',')) if search_d['genre'] is not '' else "",
				Customer.date_time.like('%'+search_d['date_time']+'%') if search_d['date_time'] is not '' else "",
				Customer.sale_name==current_user.username
				)
	per_page = 10
	page = request.args.get(get_page_parameter(), type=int, default=1)
	start = (page-1)*per_page
	end = start+per_page
	search_cus = all_search_cus.slice(start,end)
	biaoji_l = []
	for search in search_cus:
		comments = Comment.query.filter_by(c_name_id=search.id)
		if comments.first():
			for comment in comments:
				if ReadComment.query.filter_by(user=current_user.username,comment_id = comment.id).first() == None:
					biaoji = '未读'
					break
				else:
					biaoji = '已读'
			biaoji_l.append(biaoji)
		else:
			biaoji = '无评价'
			biaoji_l.append(biaoji)
	time_l,school_l,time_zj = last_time(search_cus)
	pagination = Pagination(bs_version=3,page=page, total=all_search_cus.count())
	return render_template('search.html',search_cus = search_cus,form = form,username=current_user.username,search_d = search_d,pagination = pagination,biaoji_l = biaoji_l,time_l = time_l)


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
	return time_l,school_l,time_zj



@user.route('/reset_cus/<id>/<search_d>/')
@login_required
def reset_cus(id,search_d):
	form = SearchForm()
	form.c_project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
	form1 = CustomerForm()
	form1.project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
	customer = Customer.query.filter_by(id = id).first()
	form1.project.data = customer.project
	form1.c_type.data = customer.genre
	sale_cus_info = SaleCustomerInfo.query.order_by(SaleCustomerInfo.id.desc()).filter_by(c_name_id = id)
	search_d = eval(search_d)
	search_cus = Customer.query.filter_by(**search_d)
	return render_template('reset_cus.html',customer = customer,form = form,sale_cus_info = sale_cus_info,username = current_user.username,form1=form1,search_cus = search_cus,search_d = search_d)


@user.route('/open/<id>/')
@login_required
def open(id):
	customer = Customer.query.filter_by(id = id).first()
	if customer.sale_name==current_user.username:
		form = SearchForm()
		form.c_project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
		form1 = CustomerForm()
		form1.project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
		form1.project.data = customer.project
		form1.c_type.data = customer.genre
		sale_cus_info = SaleCustomerInfo.query.order_by(SaleCustomerInfo.id.desc()).filter_by(c_name_id = id)
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
		return render_template('sale_open.html',customer = customer,form = form,sale_cus_info = sale_cus_info,username = current_user.username,form1=form1,comments = comments,old_act=old_act)
	else:
		return '这不是您的客户呦'


@user.route('/save_reset_cus_1/<id>/<search_d>/',methods=['post'])
@login_required
def save_reset_cus_1(id,search_d):
	form = CustomerForm()
	customer = Customer.query.filter_by(id = id).first()
	customer.genre = form.c_type.data
	customer.price_banci = form.price_banci.data
	db.session.add(customer)
	db.session.commit()
	return redirect(url_for('user.reset_cus',id = id,search_d=search_d))




@user.route('/save_reset_cus/<id>/',methods=['post'])
@login_required
def save_reset_cus(id):
	form = CustomerForm()
	customer = Customer.query.filter_by(id = id).first()
	c_type = form.c_type.data
	price_banci = form.price_banci.data
	customer.c_name = form.name.data
	if customer.genre!=c_type or customer.price_banci!=price_banci:
		old = Old_Active(cus_id=customer.id,old_genre=customer.genre,old_banci=customer.price_banci)
		customer.genre = c_type
		customer.price_banci = price_banci
		db.session.add(old)
	db.session.commit()
	return redirect(url_for('user.open',id = id))



@user.route('/save_cus_info_1/<id>/<search_d>/',methods=['post'])
@login_required
def save_cus_info_1(id,search_d):
	sale_cus_info = SaleCustomerInfo()
	sale_cus_info.c_name_id = id
	sale_cus_info.dongtai = request.form.get('sale_dongtai')
	sale_cus_info.next_phone = request.form.get('sale_nextphone')
	sale_cus_info.sale_name = current_user.username
	sale_cus_info.date_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	cus = Customer.query.filter_by(id = id).first()
	cus.sale_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	cus.readed = False
	db.session.add(sale_cus_info)
	db.session.commit()
	return redirect(url_for('user.reset_cus',id = id,search_d=search_d))



@user.route('/save_cus_info/<id>/',methods=['post'])
@login_required
def save_cus_info(id): 	
	sale_cus_info = SaleCustomerInfo()
	sale_cus_info.c_name_id = id
	sale_cus_info.dongtai = request.form.get('sale_dongtai')
	sale_cus_info.next_phone = request.form.get('sale_nextphone')
	sale_cus_info.sale_name = current_user.username
	sale_cus_info.date_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	cus = Customer.query.filter_by(id = id).first()
	cus.sale_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	cus.readed = False
	db.session.add(sale_cus_info)
	db.session.commit()
	return redirect(url_for('user.open',id = id))



@user.route('/search_index/')
@login_required
def search_index():
	username = current_user.username
	sale = User.query.filter_by(username = username).first()
	flag = sale.flag.split(',')
	if '0' not in flag:
		return '权限不足'
	form = SearchForm()
	form.c_project.choices = [('','')]+[(a.project,a.project) for a in AllProject.query.all()]
	return render_template('sale_search.html',form = form,username = current_user.username)



@user.route('/log_record/<id>')
@login_required
def log_record(id):
	cus =Customer.query.filter_by(id=int(id)).first()
	phone = cus.phone
	log = Log()
	log.sale_name = current_user.username
	log.phone = phone
	log.date_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	db.session.add(log)
	db.session.commit()
	return jsonify(phone=phone)