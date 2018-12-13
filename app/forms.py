# -*- coding: utf-8 -*- 
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,SelectField,DateTimeField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    #DataRequired，当你在当前表格没有输入而直接到下一个表格时会提示你输入
    username = StringField('用户名',validators=[DataRequired(message='请输入名户名')])
    password = PasswordField('密码',validators=[DataRequired(message='请输入密码')])
    submit = SubmitField('登录')

    
class ResetPass(FlaskForm):
    old_psw = PasswordField('旧密码')
    new_psw = PasswordField('设置密码')
    re_psw = PasswordField('确认密码')



class CustomerForm(FlaskForm):
    name = StringField()
    phone = StringField()
    project = SelectField(u'选择项目' ,render_kw={"class": "form-control"})
    c_type = SelectField(label="类型",
            description="类型",
            choices=[('',''),("已成交", "已成交"), ("A类", "A类"), ("B类", "B类"), ("C类", "C类"),("放弃", "放弃")],
            render_kw={"class": "form-control"})
    price_banci = StringField()



class SearchForm(FlaskForm):
    c_name = StringField()
    c_phone = StringField()
    c_project = SelectField(u'选择项目',render_kw={"class": "form-control"})
    c_type = SelectField(label="类型",
            description="类型",
            choices=[('',''), ("A类", "A类"), ("B类", "B类"), ("C类", "C类")],
            render_kw={"class": "form-control"})


class PinkSearchForm(FlaskForm):
    sale_name = SelectField(u'业务姓名')
    c_name = StringField()
    c_phone = StringField()
    school = SelectField()
    c_project = SelectField(u'选择项目')
    c_type = SelectField(label="类型",
            description="类型",
            choices=[('',''), ("A类", "A类"), ("B类", "B类"), ("C类", "C类")],
            )
    c_readed = SelectField(label="是否查看",
            description="是否查看",
            choices=[('',''),("已回复", "已回复"), ("未回复", "未回复")],
           )
class CfPinkSearchForm(FlaskForm):
    sale_name = SelectField(u'业务姓名')
    c_name = StringField()
    c_phone = StringField()
    school = SelectField()
    c_project = SelectField(u'选择项目')
    c_type = SelectField(label="类型",
            description="类型",
            choices=[('',''),("已成交", "已成交"),("放弃", "放弃")],
            )
    c_readed = SelectField(label="是否查看",
            description="是否查看",
            choices=[('',''),("已回复", "已回复"), ("未回复", "未回复")],
           )


class ZyPinkSearchForm(FlaskForm):
    sale_name = SelectField(u'业务姓名')
    c_name = StringField()
    c_phone = StringField()
    school = SelectField()
    c_project = SelectField(u'选择项目')
    c_type = SelectField(label="类型",
            description="类型",
            choices=[('',''),("已成交", "已成交"), ("A类", "A类"), ("B类", "B类"), ("C类", "C类"),("放弃", "放弃")],
            )