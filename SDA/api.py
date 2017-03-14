from tastypie.api import Api

class MyApi(Api):
	'''Specialized api that set the api on the ressource on registration'''
	def register(self, resource, canonical=True):
		super(MyApi, self).register(resource, canonical)
		resource._meta.api = self

api = MyApi(api_name='v1')


import dataset.resources
api.register(dataset.resources.DatasetResource())
api.register(dataset.resources.CharacteristicResource())
api.register(dataset.resources.TelescopeResource())
api.register(dataset.resources.InstrumentResource())
api.register(dataset.resources.KeywordResource())
api.register(dataset.resources.DataLocationResource())

import metadata.resources
api.register(metadata.resources.TagResource())
api.register(metadata.resources.AiaLev1Resource())
api.register(metadata.resources.ChrotelResource())
api.register(metadata.resources.EitResource())
api.register(metadata.resources.HmiMagnetogramResource())
api.register(metadata.resources.SwapLev1Resource())
api.register(metadata.resources.ThemisResource())
api.register(metadata.resources.XrtResource())
api.register(metadata.resources.IbisResource())

import web_account.resources
api.register(web_account.resources.UserResource())

import data_selection.resources
api.register(data_selection.resources.DataSelectionGroupResource())
api.register(data_selection.resources.DataSelectionResource())

