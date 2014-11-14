from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetaDataResource_for

from hmi_magnetogram.models import Keyword, DataLocation, MetaData, Tag

TagResource = TagResource_for("hmi_magnetogram", Tag)
KeywordResource = KeywordResource_for("hmi_magnetogram", Keyword)
DataLocationResource = DataLocationResource_for("hmi_magnetogram", DataLocation)
MetaDataResource = MetaDataResource_for("hmi_magnetogram", MetaData, TagResource)
