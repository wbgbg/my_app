#!/usr/bin/env python
# -*- coding:utf8 -*-
#coding=utf-8
#encoding=utf-8
"""
	JDSpider/网购商品报警器 是一款用于实时获取京东商品降价信息的的客户端/服务器结构程序.其中,服务器端通过异步io高效的从京东获取实时商品价格,与数据库内存储的价格对比后反馈给客户端.
"""
__author__= 'yugi/boge wang'
__version__= '0.1'

from gevent import monkey; monkey.patch_all()
import gevent
import os,sys
import uwsgi
import time
import urllib,time,json
from uwsgidecorators import *
#import sae.const
from flask import Flask,abort,request,jsonify,g,url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired)
import smtplib
from email.mime.text import MIMEText
from email.header import Header

app = Flask(__name__)

app.config['SECRET_KEY'] = 'CZH IS DIAO BAO LE'   #密钥
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/db.sqlite'   #数据库地址
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  #request后自动提交 
#refresh_time = 60   
apipath="https://api.jd.com/routerjson?v=2.0&"
app_key="app_key=84F0963912EA9D56CD29E8EB3E774A2B&"  #拼接url请求京东API用

#class Config(object):
#
#	DEBUG = True
#	
#	SECRET_KEY = 'CZH IS DIAO BAO LE'
#
#	SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (sae.const.MYSQL_USER,
#	sae.const.MYSQL_PASS,
#	sae.const.MYSQL_HOST,
#	sae.const.MYSQL_PORT,
#	sae.const.MYSQL_DB)
#
#	SQLALCHEMY_ECHO = True
#
#class nullpool_SQLAlchemy(SQLAlchemy):
#	def apply_driver_hacks(self,app,info,options):
#		super(nullpool_SQLAlchemy,self).apply_driver_hacks(app,info,options)
#		from sqlalchemy.pool import NullPool
#		options['poolclass'] = NullPool
#		del options['pool_size']


#db=nullpool_SQLAlchemy(app)
db=SQLAlchemy(app)
auth=HTTPBasicAuth()
#@app.route('/API/v0.1/users',methods=['POST'])
#def new_user():
#	return "POST"

user_jdproducts= db.Table('user_jdproducts',
	db.Column('User_id',db.Integer,db.ForeignKey('users.id')),
	db.Column('JDProduct_id',db.Integer,db.ForeignKey('jdproducts.id')))  #账号与商品的关系表,用于完成两表间多对多关系

class User(db.Model):
	"""账号数据表类,包含主键,账号,哈希过的密码,以及连接商品用的外键"""
	__tablename__='users'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(32),index=True)
	password_hash = db.Column(db.String(64))
	jdproducts = db.relationship('JDProduct',secondary=user_jdproducts,backref=db.backref('users',lazy='dynamic'))
#	def __init__(self,id=0,username='',password='')
#		self.id=id
#		self.username=username
#		self.password=password
		
	def hash_password(self,password):
		"""哈希加密密码"""
		self.password_hash = pwd_context.encrypt(password)
	def verify_password(self,password):
		"""验证密码"""
		return pwd_context.verify(password,self.password_hash)
	def generate_auth_token(self,expiration=600):
		"""生成登录后的验证token"""
		s=Serializer(app.config['SECRET_KEY'], expires_in=expiration) 
		return s.dumps({'id':self.id})
	
	@staticmethod
	def verify_auth_token(token):
		"""验证token是否有效"""
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None
		user = User.query.get(data['id'])
		return user

@auth.verify_password
def verify_password(username_or_token,password):
	"""验证密码,调用类中的比较函数进行比较"""
	user = User.verify_auth_token(username_or_token)
	if not user:
		user = User.query.filter_by(username=username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user			
	return True

class JDProduct(db.Model):
	"""商品信息数据表,包含主键,商品编号,价格以及一个备用的列"""
	__tablename__='jdproducts'
	id = db.Column(db.Integer,primary_key=True)
	hkd = db.Column(db.String(10))
	price = db.Column(db.String(10))
	mark = db.Column(db.String(10))

@app.route('/api/favorite/add',methods=['POST'])
@auth.login_required
def add_favorite():
	"""添加收藏API"""
	user=g.user
	print user.jdproducts
	producthkd = request.json.get('hkd')
	if JDProduct.query.filter_by(hkd=producthkd).first() is None:
		product = JDProduct(hkd=producthkd)#add new product if it is not exist
		print product.hkd
		db.session.add(product)
		db.session.commit()	
	else:
		product = JDProduct.query.filter_by(hkd=producthkd).first()
		print product.hkd
	user.jdproducts.append(product)
	print user.jdproducts
#	db.session.add()
#	db.session.commit()
	return "ok"

@app.route('/api/favorite/del',methods=['POST'])
@auth.login_required
def del_favorite():	
	"""删除收藏API"""
	producthkd = request.json.get('hkd')
	if JDProduct.query.filter_by(hkd=producthkd).first() is not None:
		product = JDProduct.query.filter_by(hkd=producthkd).first()
		user=g.user
		user.jdproducts.remove(product)	
#		db.session.add(user)
#		db.session.commit()
	return "ok"

@app.route('/api/favorite',methods=['GET'])
@auth.login_required
def favorite():
	"""查询用户收藏商品API"""
	user = g.user
	respon ={}
	for product in user.jdproducts:
		respon[product.hkd]=product.price
	return(jsonify(respon),200,())

@app.route('/api/jdproducts/<hkd>',methods=['GET'])
def jdpro(hkd):
	"""查询商品价格API"""
	respon ={}
	for user in user.jdproducts:
		respon[product.hkd]=product.price
	return(jsonify(respon),200,())

@app.route('/api/jdproducts/name/<hkd>',methods=['GET'])
@auth.login_required
def product_price(hkd):
	"""向京东请求商品名称api"""
	respon = {}
	method = "method=jingdong.ware.baseproduct.get&"	
	sku_id = "360buy_param_json={%22ids%22:%22"+hkd+"%22,%22base%22:%22name%22}&"
	now=time.localtime()
	timestamp="timestamp="+time.strftime("%Y-%m-%d %X",now)
	url=apipath+method+app_key+sku_id+timestamp
	print url	
	f = urllib.urlopen(url)
	st = f.read()
	js = json.loads(st)
	print js
	name = js[u"jingdong_ware_baseproduct_get_responce"][u"product_base"][0][u"name"]
	print type(name)
	#realname=name.decode("utf-8")
	#print type(realname)
	respon[hkd] = name
	return(jsonify(respon),200,())


#timer(refresh_time)
@app.route('/api/fetch/all')
def fetch_all():
	"""对数据库中所有商品向京东请求价格,并修改数据库,发送提醒,协程实现异步io"""
	method="method=jingdong.ware.price.get&"
	i=1
	print "start working"
#	while  (JDProduct.query.get(i) is not None):
#		now_product = JDProduct.query.get(i)
#		print "working on %s" %i
#		threads = threads.append(gevent.spawn(fetch_product,now_product.hkd))
#		print "%i finished"%i
	product = JDProduct.query.all()
	ukd = [prod.hkd for prod in product]
	threads = [gevent.spawn(fetch_product,hkd) for hkd in ukd]
	gevent.joinall(threads)
	return "ok"

def three_minute_call(signum):
	"""定时任务 每10分钟执行一次fetch_all"""
	fetch_all()

uwsgi.register_signal(99,"",three_minute_call)#信号注册
uwsgi.add_timer(99,600)#定时器

@app.route('/api/sendmail')
def sendmail(hkd=0,price1=0,price2=0):
	"""demo 发送邮件提醒价格变动"""
        sender = "wbgbg123@126.com"
        receiver = "576214465@qq.com"
        subject = "the price of %s has changed from %s to %s" % (hkd,price1,price2)
        smtpserver = "smtp.126.com"
        username = "wbgbg123@126.com"
        password = "wbgbgabc"

        msg = MIMEText("",'text','utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
	print msg.as_string()
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username,password)
	print "ready to send"
        smtp.sendmail(sender,receiver,msg.as_string())
	print "finished"
        smtp.quit()
	return "ok"


@app.route('/api/fetch/<hkd>')
def fetch_product(hkd=0):
	"""向京东查询单个商品价格"""
	#for now_product in JDProduct.query.all():
	ukd="J_%s"%hkd
	method="method=jingdong.ware.price.get&"
	sku_id="360buy_param_json={%22sku_id%22:%22"+ukd+"%22}&"
	now=time.localtime()
	timestamp="timestamp="+time.strftime("%Y-%m-%d %X",now)
	url=apipath+method+app_key+sku_id+timestamp
	price = "-1.00"
	trys = 5
	while (price=="-1.00" and trys>0):
		trys = trys-1
		with gevent.Timeout(10,False) as timeout:
			f = urllib.urlopen(url)
			st = f.read()
			js = json.loads(st)
#	print "%s:%s:%s"%(url,st,js)
			price = js[u"jingdong_ware_price_get_responce"][u"price_changes"][0][u"price"]
#	fil = open("/home/nowlog",'a')
#	fil.write(price)
#	fil.close
	now_product = JDProduct.query.filter_by(hkd=hkd).first()
	if now_product is not None:
		if (now_product.price != price and not(now_product.price in ["-1.00","-1"] and price in ["-1.00","-1"])):
			print "%s price change from %s to %s" %(ukd,now_product.price,price)
			sendmail(now_product.hkd,now_product.price,price)
			now_product.price = price
			db.session.commit();	
#			tell_client(nowproduct.hkd)
#	return (jsonify({'ukd=':ukd,'price=':price}))		
	return "ok"

def tell_client(ukd):
	pass

@app.route('/api/users',methods=['POST'])	
def new_user():
	"""新用户注册api"""
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		print "no username"
		abort(400)
	if User.query.filter_by(username=username).first() is not None:
		print username
		print password
		print "no user"
		abort(400)
	user = User(username=username)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	return (jsonify({'username': user.username}), 201 ,{'Location':url_for('get_user',id=user.id,_external=True)})

@app.route('/api/users/<int:id>')	
def get_user(id):
	"""通过用户id查询用户名称api"""
	user = User.query.get(id)
	if not user:
		abort(400)
	return jsonify({'username':user.username})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
	"""返回登录token API"""
	token = g.user.generate_auth_token(600)
	return jsonify({'token':token.decode('ascii'),'duration':600})

@app.route('/api/resource')
@auth.login_required
def get_resource():
	return jsonify({'data':'Hello, %s!' %g.user.username})

@app.route('/')
def hello_world():
	return u'你好'
@app.route('/czh')
def czh():
	return 'sb!'

def __init__():
	if not os.path.exists('db.sqlite'):
		db.create_all()
#	app.run()


if __name__=='__main__':
	if not os.path.exists('db.sqlite'):
		db.create_all()
