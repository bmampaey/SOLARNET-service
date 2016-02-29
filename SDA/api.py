from tastypie.api import Api

api = Api(api_name='v1')


import dataset.resources
api.register(dataset.resources.DatasetResource())
api.register(dataset.resources.CharacteristicResource())
api.register(dataset.resources.TelescopeResource())
api.register(dataset.resources.InstrumentResource())
api.register(dataset.resources.KeywordResource())
api.register(dataset.resources.TagResource())
api.register(dataset.resources.DataLocationResource())

import chrotel.resources
api.register(chrotel.resources.MetadataResource())

import xrt.resources
api.register(xrt.resources.MetadataResource())

import eit.resources
api.register(eit.resources.MetadataResource())

import swap_lev1.resources
api.register(swap_lev1.resources.MetadataResource())

import aia_lev1.resources
api.register(aia_lev1.resources.MetadataResource())

import hmi_magnetogram.resources
api.register(hmi_magnetogram.resources.MetadataResource())

import themis.resources
api.register(themis.resources.MetadataResource())

