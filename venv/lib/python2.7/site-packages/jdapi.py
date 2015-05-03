# -*- coding: utf-8 -*-
import urllib
import time
import json

ukd=raw_input()
apipath="https://api.jd.com/routerjson?v=2.0&"
method="method=jingdong.ware.price.get&"
app_key="app_key=84F0963912EA9D56CD29E8EB3E774A2B&"
sku_id="360buy_param_json={%22sku_id%22:%22"+ukd+"%22}&"
now=time.localtime()
timestamp="timestamp="+time.strftime("%Y-%m-%d %X",now)
url=apipath+method+app_key+sku_id+timestamp
print url
f = urllib.urlopen(url)
#print f.read(),f.getcode()
#req = json.loads(f.read())
st=f.read()
js=json.loads(st)
print js
print js[u"jingdong_ware_price_get_responce"][u"price_changes"][0][u"price"]
