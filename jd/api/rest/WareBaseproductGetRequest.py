from jd.api.base import RestApi

class WareBaseproductGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.ids = None
			self.base = None

		def getapiname(self):
			return 'jingdong.ware.baseproduct.get'




