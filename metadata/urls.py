from api import svo_api
from metadata.resources import (
	TagResource,
	AiaLevel1Resource,
	ChromisResource,
	ChrotelResource,
	CrispResource,
	EitLevel0Resource,
	EuiLevel1Resource,
	EuiLevel2Resource,
	EuviLevel0Resource,
	GrisLevel1Resource,
	HmiMagnetogramResource,
	IbisResource,
	LyraLevel2Resource,
	LyraLevel3Resource,
	RosaResource,
	SwapLevel1Resource,
	ThemisResource,
	UsetCalciumiiKLevel1Resource,
	UsetWhiteLightLevel1Resource,
	XrtResource
)

# Register the metadata resources
svo_api.register(TagResource())
svo_api.register(AiaLevel1Resource())
svo_api.register(ChromisResource())
svo_api.register(ChrotelResource())
svo_api.register(CrispResource())
svo_api.register(EitLevel0Resource())
svo_api.register(EuiLevel1Resource())
svo_api.register(EuiLevel2Resource())
svo_api.register(EuviLevel0Resource())
svo_api.register(GrisLevel1Resource())
svo_api.register(HmiMagnetogramResource())
svo_api.register(IbisResource())
svo_api.register(LyraLevel2Resource())
svo_api.register(LyraLevel3Resource())
svo_api.register(RosaResource())
svo_api.register(SwapLevel1Resource())
svo_api.register(ThemisResource())
svo_api.register(UsetCalciumiiKLevel1Resource())
svo_api.register(UsetWhiteLightLevel1Resource())
svo_api.register(XrtResource())
