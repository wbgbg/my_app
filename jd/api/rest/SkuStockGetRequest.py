from jd.api.base import RestApi

class SkuStockGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.sku_id = None
			self.area_id = None

		def getapiname(self):
			return 'jingdong.sku.stock.get'




