from jd.api.base import RestApi

class WareProductSearchListGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.isLoadAverageScore = None
			self.isLoadPromotion = None
			self.sort = None
			self.page = None
			self.pageSize = None
			self.keyword = None
			self.client = None

		def getapiname(self):
			return 'jingdong.ware.product.search.list.get'




