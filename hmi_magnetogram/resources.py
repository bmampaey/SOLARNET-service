from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetadaResource_for

from hmi_magnetogram.models import Keyword, DataLocation, Metada, Tag

TagResource = TagResource_for("hmi_magnetogram", Tag)
KeywordResource = KeywordResource_for("hmi_magnetogram", Keyword)
DataLocationResource = DataLocationResource_for("hmi_magnetogram", DataLocation)
MetadaResource = MetadaResource_for("hmi_magnetogram", Metada, TagResource)
