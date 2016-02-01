from collections import OrderedDict

from common.views import BaseSearchDataForm, BaseSearchDataResults, BaseDownloadData
from chrotel.forms import SearchData
from chrotel.models import Metada, DataLocation

class SearchDataForm(BaseSearchDataForm):
	dataset_id = "chrotel"
	search_form_class = SearchData

class SearchDataResults(BaseSearchDataResults):
	dataset_id = "chrotel"
	model = Metada
	search_form_class = SearchData
	table_columns = OrderedDict([("date_obs", "Date Observation"), ("wavelnth", "Wavelength"), ("sci_obj", "Science Objectif")])

class DownloadData(BaseDownloadData):
	data_location_model = DataLocation

