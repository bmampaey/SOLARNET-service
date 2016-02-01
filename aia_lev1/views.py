from collections import OrderedDict

from common.views import BaseSearchDataForm, BaseSearchDataResults, BaseDownloadData
from aia_lev1.forms import SearchData
from aia_lev1.models import Metada, DataLocation

class SearchDataForm(BaseSearchDataForm):
	dataset_id = "aia_lev1"
	search_form_class = SearchData

class SearchDataResults(BaseSearchDataResults):
	dataset_id = "aia_lev1"
	model = Metada
	search_form_class = SearchData
	table_columns = OrderedDict([("date_obs", "Date Observation"), ("wavelnth", "Wavelength"), ("quality", "Quality")])

class DownloadData(BaseDownloadData):
	data_location_model = DataLocation

