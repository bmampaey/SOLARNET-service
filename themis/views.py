from collections import OrderedDict

from common.views import BaseSearchDataForm, BaseSearchDataResults, BaseDownloadData
from themis.forms import SearchData
from themis.models import MetaData, DataLocation

class SearchDataForm(BaseSearchDataForm):
	dataset_id = "themis"
	search_form_class = SearchData

class SearchDataResults(BaseSearchDataResults):
	dataset_id = "themis"
	model = MetaData
	search_form_class = SearchData
	table_columns = OrderedDict([("date_obs", "Date Observation"), ("wavelnth", "Wavelength")])

class DownloadData(BaseDownloadData):
	data_location_model = DataLocation

