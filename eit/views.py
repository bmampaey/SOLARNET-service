from collections import OrderedDict

from common.views import BaseSearchDataForm, BaseSearchDataResults, BaseDownloadData
from eit.forms import SearchData
from eit.models import MetaData, DataLocation

class SearchDataForm(BaseSearchDataForm):
	dataset_id = "eit"
	search_form_class = SearchData

class SearchDataResults(BaseSearchDataResults):
	dataset_id = "eit"
	model = MetaData
	search_form_class = SearchData
	table_columns = OrderedDict([("date_obs", "Date Observation"), ("wavelnth", "Wavelength"), ("sci_obj", "Science Objectif")])

class DownloadData(BaseDownloadData):
	data_location_model = DataLocation

