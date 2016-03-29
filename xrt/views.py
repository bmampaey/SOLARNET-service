from collections import OrderedDict

from common.views import BaseSearchDataForm, BaseSearchDataResults, BaseDownloadData
from xrt.forms import SearchData
from xrt.models import MetaData, DataLocation

class SearchDataForm(BaseSearchDataForm):
	dataset_id = "xrt"
	search_form_class = SearchData

class SearchDataResults(BaseSearchDataResults):
	dataset_id = "xrt"
	model = MetaData
	search_form_class = SearchData
	table_columns = OrderedDict([("date_obs", "Date Observation"), ("noaa_num", "NOAA A.R. number"), ('target', 'Observation Region')])

class DownloadData(BaseDownloadData):
	data_location_model = DataLocation

