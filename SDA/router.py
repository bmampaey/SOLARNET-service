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

from chrotel.views import ChrotelMetadataViewSet
router.register(r'chrotel', ChrotelMetadataViewSet, base_name='chrotel')

from xrt.views import XrtMetadataViewSet
router.register(r'xrt', XrtMetadataViewSet, base_name='xrt')