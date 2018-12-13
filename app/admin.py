# -*- coding: utf-8 -*- 
from app import app
from app import db 
from .models import User
from flask import request,Flask,render_template,request,Blueprint,redirect,url_for
from flask_login import logout_user,login_user,current_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash


admin = Blueprint('admin',__name__)





@admin.route('/')
@login_required
def admin_index():
	t = User.query.filter(User.id>1)
	return render_template('admin.html',t = t)
	# print(t[0].username)


@admin.route('/add',methods = ['post'])
@login_required
def admin_add():
	username = request.form.get('username')
	flag = request.form.getlist('flag')
	flag = ','.join(flag)
	print(flag)
	p_hash = generate_password_hash('000000')
	school = request.form.get('school')
	group = request.form.get('group')
	user = User(username = username,password_hash=p_hash,flag=flag,school = school,group=group)
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('admin.admin_index'))
	


@admin.route('/delete/<id>')
@login_required
def admin_delete(id):
	user = User.query.filter_by(id = id).first()
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('admin.admin_index'))
	# return username


@admin.route('/reset_psw/<id>')
@login_required
def admin_reset_psw(id):
	user = User.query.filter_by(id = id).first()
	user.password_hash = generate_password_hash('000000')
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('admin.admin_index'))

@admin.route('/reset_position/<id>')
@login_required
def admin_reset_position(id):
	user = User.query.filter_by(id = id).first()
	if user.flag==True:
		user.flag=False
	else:
		user.flag=True
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('admin.admin_index'))