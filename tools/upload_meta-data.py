import slumber
import dateutil.parser
from datetime import datetime


class DataSet:
	def __init__(data_set_api, data_set_name = ""):
		self.data_set_api = data_set_api
		self.data_set_name = data_set_name
		self.keywords = self.data_set_api.keyword.get(limit=0)

class SDA:
	def __init__(url = "http://db1.sdod.oma.be:8080/api/v1/", auth = None):
		self.api = slumber.API(url, auth)
	
	def data_set(data_set_name):
		return DataSet(getattr(self.api, data_set_name), data_set_name)



dataset = SDA.data_set("eit")



