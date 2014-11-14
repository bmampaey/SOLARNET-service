from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetaDataResource_for

from swap.models import Keyword, DataLocation, MetaData, Tag

TagResource = TagResource_for("swap", Tag)
KeywordResource = KeywordResource_for("swap", Keyword)
DataLocationResource = DataLocationResource_for("swap", DataLocation)
MetaDataResource = MetaDataResource_for("swap", MetaData, TagResource)
