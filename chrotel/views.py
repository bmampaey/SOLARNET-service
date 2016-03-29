from collections import OrderedDict

from common.views import BaseSearchDataForm, BaseSearchDataResults, BaseDownloadData
from chrotel.forms import SearchData
from chrotel.models import MetaData, DataLocation

class SearchDataForm(BaseSearchDataForm):
	dataset_id = "chrotel"
	search_form_class = SearchData

class SearchDataResults(BaseSearchDataResults):
	dataset_id = "chrotel"
	model = MetaData
	search_form_class = SearchData
	table_columns = OrderedDict([("date_obs", "Date Observation"), ("wavelnth", "Wavelength")])

class DownloadData(BaseDownloadData):
	data_location_model = DataLocation

