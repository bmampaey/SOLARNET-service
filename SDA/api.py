from tastypie.api import Api

from dataset.resources import DataSetResource
import eit.resources 

v1_api = Api(api_name='v1')
v1_api.register(DataSetResource())
v1_api.register(eit.resources.MetaDataResource())

