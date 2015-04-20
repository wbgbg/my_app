#!/usr/bin/env python
# -*- coding:utf8 -*-
#elncoding = utf-8
from gevent import monkey; monkey.patch_all()
import os,sys
import time
import urllib,time,json
from flask import Flask,abort,request,jsonify,g,url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired)
#from uwsgidecorators import *
import gevent
apipath="https://api.jd.com/routerjson?v=2.0&"
app_key="app_key=84F0963912EA9D56CD29E8EB3E774A2B&"


def fetch_product(hkd=0):
	ukd="J_%s"%hkd
	method="method=jingdong.ware.price.get&"
	sku_id="360buy_param_json={%22sku_id%22:%22"+ukd+"%22}&"
	now=time.localtime()
	timestamp="timestamp="+time.strftime("%Y-%m-%d %X",now)
	url=apipath+method+app_key+sku_id+timestamp
	f = urllib.urlopen(url)
	st = f.read()
	js = json.loads(st)
	price = js[u"jingdong_ware_price_get_responce"][u"price_changes"][0][u"price"]
	print ukd,':',price


def fetch_all(low_b,up_b):			
	threads = []
	for i in range(low_b,up_b):
		threads = threads.append(gevent.spawn(fetch_product,i))
	gevent.joinall(threads)

if __name__=="__main__"	:
	print time.localtime()
	fetch_all(1217499,1218499)
	print time.localtime()
