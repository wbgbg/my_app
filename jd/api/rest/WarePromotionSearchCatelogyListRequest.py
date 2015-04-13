from jd.api.base import RestApi

class WarePromotionSearchCatelogyListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.catelogyId = None
			self.page = None
			self.pageSize = None
			self.client = None

		def getapiname(self):
			return 'jingdong.ware.promotion.search.catelogy.list'




