from rest_framework import routers

#DRF url router
router = routers.DefaultRouter()

import dataset.views
router.register(r'telescope', dataset.views.TelescopeViewSet)
router.register(r'instrument', dataset.views.InstrumentViewSet)
router.register(r'data_location', dataset.views.DataLocationViewSet)
router.register(r'dataset', dataset.views.DatasetViewSet)
router.register(r'characteristic', dataset.views.CharacteristicViewSet)
router.register(r'keyword', dataset.views.KeywordViewSet)
router.register(r'tag', dataset.views.TagViewSet)

import chrotel.views
router.register(r'chrotel', chrotel.views.MetadataViewSet, base_name = 'chrotel')

import xrt.views
router.register(r'xrt', xrt.views.MetadataViewSet)