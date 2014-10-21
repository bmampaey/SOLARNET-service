from collections import OrderedDict

from common.views import BaseSearchDataForm, BaseSearchDataResults, BaseDownloadData
from swap.forms import SearchData
from swap.models import MetaData, DataLocation

class SearchDataForm(BaseSearchDataForm):
	dataset_name = "swap"
	search_form_class = SearchData

class SearchDataResults(BaseSearchDataResults):
	dataset_name = "swap"
	model = MetaData
	search_form_class = SearchData
	table_columns = OrderedDict([("date_obs", "Date Observation")])

class DownloadData(BaseDownloadData):
	data_location_model = DataLocation
