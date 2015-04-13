#!/usr/bin/env python
import os
from flask import Flask,abort,request,jsonify,g,url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CZH IS DIAO BAO LE'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/yugi/db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db=SQLAlchemy(app)
auth=HTTPBasicAuth()
#@app.route('/API/v0.1/users',methods=['POST'])
#def new_user():
#	return "POST"

user_jdproducts= db.Table('user_jdproducts',
	db.Column('User_id',db.Integer,db.ForeignKey('users.id')),
	db.Column('JDProduct_id',db.Integer,db.ForeignKey('jdproducts.id')))

class User(db.Model):
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
		self.password_hash = pwd_context.encrypt(password)
	def verify_password(self,password):
		return pwd_context.verify(password,self.password_hash)
	def generate_auth_token(self,expiration=600):
		s=Serializer(app.config['SECRET_KEY'], expires_in=expiration) 
		return s.dumps({'id':self.id})
	
	@staticmethod
	def verify_auth_token(token):
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
	user = User.verify_auth_token(username_or_token)
	if not user:
		user = User.query.filter_by(username=username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user			
	return True

class JDProduct(db.Model):
	__tablename__='jdproducts'
	id = db.Column(db.Integer,primary_key=True)
	hkd = db.Column(db.String(10))
	price = db.Column(db.String(10))
	mark = db.Column(db.String(10))

@app.route('/api/favorite/add',methods=['POST'])
@auth.login_required
def add_favorite():
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
	user = g.user
	respon ={}
	for product in user.jdproducts:
		respon[product.hkd]=product.price
	return(jsonify(respon),200,())
		
	

@app.route('/api/fetch',methods=['POST','GET'])
def fetch_product():
	for now_product in JDProduct.query.all():
		pass#use JD API to refresh the price		


@app.route('/api/users',methods=['POST'])	
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		abort(400)
	if User.query.filter_by(username=username).first() is not None:
		abort(400)
	user = User(username=username)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	return (jsonify({'username': user.username}), 201 ,{'Location':url_for('get_user',id=user.id,_external=True)})

@app.route('/api/users/<int:id>')	
def get_user(id):
	user = User.query.get(id)
	if not user:
		abort(400)
	return jsonify({'username':user.username})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token(600)
	return jsonify({'token':token.decode('ascii'),'duration':600})

@app.route('/api/resource')
@auth.login_required
def get_resource():
	return jsonify({'data':'Hello, %s!' %g.user.username})

@app.route('/')
def hello_world():
	return 'Hello World!'
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
	app.run(debug=True)
	
