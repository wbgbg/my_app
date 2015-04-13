from jd.api.base import RestApi
class UmpToolsGetRequest(RestApi):
	def __init__(self,domain='gw.api.360buy.net',port=80):
		RestApi.__init__(self,domain, port)
		self.cid = None
		self.value_id = None
		self.source = None
		self.ip = None

	def getapiname(self):
		return 'jingdong.ecc.categoryattrvalue.get'