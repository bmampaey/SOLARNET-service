from tastypie.api import Api


#import eit.resources
#import swap_lev1.resources
#import aia_lev1.resources
#import hmi_magnetogram.resources
#import themis.resources
#import wizard.resources

v1_api = Api(api_name='v1')

# TODO remove when migrating to SVO
import account.resources
v1_api.register(account.resources.UserResource())

import dataset.resources
v1_api.register(dataset.resources.DatasetResource())
v1_api.register(dataset.resources.CharacteristicResource())
v1_api.register(dataset.resources.TelescopeResource())
v1_api.register(dataset.resources.InstrumentResource())
v1_api.register(dataset.resources.KeywordResource())

import common.resources
v1_api.register(common.resources.TagResource())
v1_api.register(common.resources.DataLocationResource())

import chrotel.resources
v1_api.register(chrotel.resources.MetadaResource())

#import eit.resources
#v1_api.register(eit.resources.MetadaResource())
#
#v1_api.register(swap_lev1.resources.MetadaResource())
#
#v1_api.register(aia_lev1.resources.MetadaResource())
#
#v1_api.register(hmi_magnetogram.resources.MetadaResource())
#
#v1_api.register(themis.resources.MetadaResource())
#
#v1_api.register(wizard.resources.UserDataSelectionResource())
#v1_api.register(wizard.resources.DataSelectionResource())

#from SDA.resources import UserResource, UserProfileResource
#v1_api.register(UserResource())
#v1_api.register(UserProfileResource())
