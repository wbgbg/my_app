from jd.api.base import RestApi

class WareProductStockListGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.skuId = None
			self.provinceId = None
			self.client = None

		def getapiname(self):
			return 'jingdong.ware.product.stock.list.get'




