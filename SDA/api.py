from tastypie.api import Api

from dataset.resources import DatasetResource
import eit.resources
import swap.resources

v1_api = Api(api_name='v1')
v1_api.register(DatasetResource())
v1_api.register(eit.resources.MetaDataResource())
v1_api.register(eit.resources.DataLocationResource())
v1_api.register(eit.resources.KeywordResource())

v1_api.register(swap.resources.MetaDataResource())
v1_api.register(swap.resources.DataLocationResource())
v1_api.register(swap.resources.KeywordResource())

#from SDA.resources import UserResource, UserProfileResource
#v1_api.register(UserResource())
#v1_api.register(UserProfileResource())
