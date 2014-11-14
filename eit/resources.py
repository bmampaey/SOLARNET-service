from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetaDataResource_for

from eit.models import Keyword, DataLocation, MetaData, Tag

TagResource = TagResource_for("eit", Tag)
KeywordResource = KeywordResource_for("eit", Keyword)
DataLocationResource = DataLocationResource_for("eit", DataLocation)
MetaDataResource = MetaDataResource_for("eit", MetaData, TagResource)
