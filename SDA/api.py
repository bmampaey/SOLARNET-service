from tastypie.api import Api

import dataset.resources
import themis.resources
import swap_lev1.resources
import aia_lev1.resources
import hmi_magnetogram.resources
import wizard.resources

v1_api = Api(api_name='v1')
v1_api.register(dataset.resources.DatasetResource())
v1_api.register(dataset.resources.CharacteristicResource())
v1_api.register(dataset.resources.TelescopeResource())
v1_api.register(dataset.resources.InstrumentResource())
v1_api.register(dataset.resources.TagResource())

v1_api.register(themis.resources.MetaDataResource())
v1_api.register(themis.resources.DataLocationResource())
v1_api.register(themis.resources.KeywordResource())
v1_api.register(themis.resources.TagResource())

v1_api.register(swap_lev1.resources.MetaDataResource())
v1_api.register(swap_lev1.resources.DataLocationResource())
v1_api.register(swap_lev1.resources.KeywordResource())
v1_api.register(swap_lev1.resources.TagResource())

v1_api.register(aia_lev1.resources.MetaDataResource())
v1_api.register(aia_lev1.resources.DataLocationResource())
v1_api.register(aia_lev1.resources.KeywordResource())
v1_api.register(aia_lev1.resources.TagResource())

v1_api.register(hmi_magnetogram.resources.MetaDataResource())
v1_api.register(hmi_magnetogram.resources.DataLocationResource())
v1_api.register(hmi_magnetogram.resources.KeywordResource())
v1_api.register(hmi_magnetogram.resources.TagResource())

v1_api.register(themis.resources.MetaDataResource())
v1_api.register(themis.resources.DataLocationResource())
v1_api.register(themis.resources.KeywordResource())
v1_api.register(themis.resources.TagResource())

v1_api.register(wizard.resources.UserDataSelectionResource())
v1_api.register(wizard.resources.DataSelectionResource())

#from SDA.resources import UserResource, UserProfileResource
#v1_api.register(UserResource())
#v1_api.register(UserProfileResource())
