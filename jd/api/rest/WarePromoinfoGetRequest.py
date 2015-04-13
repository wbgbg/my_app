from jd.api.base import RestApi

class WarePromoinfoGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.skuIds = None
			self.webSite = None
			self.origin = None
			self.areaId = None

		def getapiname(self):
			return 'jingdong.ware.promoinfo.get'




