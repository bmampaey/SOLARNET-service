from collections import OrderedDict

from common.views import BaseSearchDataForm, BaseSearchDataResults, BaseDownloadData
from hmi_magnetogram.forms import SearchData
from hmi_magnetogram.models import Metada, DataLocation

class SearchDataForm(BaseSearchDataForm):
	dataset_id = "hmi_magnetogram"
	search_form_class = SearchData

class SearchDataResults(BaseSearchDataResults):
	dataset_id = "hmi_magnetogram"
	model = Metada
	search_form_class = SearchData
	table_columns = OrderedDict([("date_obs", "Date Observation"), ("quality", "Quality")])

class DownloadData(BaseDownloadData):
	data_location_model = DataLocation

