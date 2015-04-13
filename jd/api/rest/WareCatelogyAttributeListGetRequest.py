from jd.api.base import RestApi

class WareCatelogyAttributeListGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.newVersion = None
			self.catelogyId = None
			self.client = None

		def getapiname(self):
			return 'jingdong.ware.catelogy.attribute.list.get'




