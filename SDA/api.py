from tastypie.api import Api

from dataset.api.resources import DataSetResource

v1_api = Api(api_name='v1')
v1_api.register(DataSetResource())

