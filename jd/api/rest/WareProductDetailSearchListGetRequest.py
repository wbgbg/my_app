from jd.api.base import RestApi

class WareProductDetailSearchListGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.skuId = None
			self.isLoadWareScore = None
			self.client = None

		def getapiname(self):
			return 'jingdong.ware.product.detail.search.list.get'




