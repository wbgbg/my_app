from jd.api.base import RestApi

class WarePacksGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.skuId = None
			self.client = None

		def getapiname(self):
			return 'jingdong.ware.packs.get'




