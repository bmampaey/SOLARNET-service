from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetaDataResource_for

from aia_lev1.models import Keyword, DataLocation, MetaData, Tag

TagResource = TagResource_for("aia_lev1", Tag)
KeywordResource = KeywordResource_for("aia_lev1", Keyword)
DataLocationResource = DataLocationResource_for("aia_lev1", DataLocation)
MetaDataResource = MetaDataResource_for("aia_lev1", MetaData, TagResource)
