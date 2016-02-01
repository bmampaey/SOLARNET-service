from collections import OrderedDict

from common.views import BaseSearchDataForm, BaseSearchDataResults, BaseDownloadData
from swap_lev1.forms import SearchData
from swap_lev1.models import Metada, DataLocation

class SearchDataForm(BaseSearchDataForm):
	dataset_id = "swap_lev1"
	search_form_class = SearchData

class SearchDataResults(BaseSearchDataResults):
	dataset_id = "swap_lev1"
	model = Metada
	search_form_class = SearchData
	table_columns = OrderedDict([("date_obs", "Date Observation")])

class DownloadData(BaseDownloadData):
	data_location_model = DataLocation
