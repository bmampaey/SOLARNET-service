from tastypie.api import Api

v1_api = Api(api_name='v1')


import dataset.resources
v1_api.register(dataset.resources.DatasetResource())
v1_api.register(dataset.resources.CharacteristicResource())
v1_api.register(dataset.resources.TelescopeResource())
v1_api.register(dataset.resources.InstrumentResource())
v1_api.register(dataset.resources.KeywordResource())
v1_api.register(dataset.resources.TagResource())
v1_api.register(dataset.resources.DataLocationResource())

import chrotel.resources
v1_api.register(chrotel.resources.MetadataResource())

import xrt.resources
v1_api.register(xrt.resources.MetadataResource())

import eit.resources
v1_api.register(eit.resources.MetadataResource())
#
#v1_api.register(swap_lev1.resources.MetadataResource())
#
#v1_api.register(aia_lev1.resources.MetadataResource())
#
#v1_api.register(hmi_magnetogram.resources.MetadataResource())
#
#v1_api.register(themis.resources.MetadataResource())

