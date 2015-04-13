from jd.api.base import RestApi

class WarePromotionInfoGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.skuId = None
			self.webSite = None
			self.origin = None

		def getapiname(self):
			return 'jingdong.ware.promotionInfo.get'




