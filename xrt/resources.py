from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetaDataResource_for

from xrt.models import Keyword, DataLocation, MetaData, Tag

TagResource = TagResource_for("xrt", Tag)
KeywordResource = KeywordResource_for("xrt", Keyword)
DataLocationResource = DataLocationResource_for("xrt", DataLocation)
MetaDataResource = MetaDataResource_for("xrt", MetaData, TagResource)
