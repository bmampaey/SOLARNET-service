from api import svo_api
from metadata.resources import TagResource, AiaLevel1Resource, ChromisResource, ChrotelResource, CrispResource, EitLevel0Resource, GrisLevel1Resource, HmiMagnetogramResource, IbisResource, RosaResource, SwapLevel1Resource, ThemisResource, XrtResource

# Register the metadata resources
svo_api.register(TagResource())
svo_api.register(AiaLevel1Resource())
svo_api.register(ChromisResource())
svo_api.register(ChrotelResource())
svo_api.register(CrispResource())
svo_api.register(EitLevel0Resource())
svo_api.register(GrisLevel1Resource())
svo_api.register(HmiMagnetogramResource())
svo_api.register(IbisResource())
svo_api.register(RosaResource())
svo_api.register(SwapLevel1Resource())
svo_api.register(ThemisResource())
svo_api.register(XrtResource())