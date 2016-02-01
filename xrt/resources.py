from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetadaResource_for

from xrt.models import Keyword, DataLocation, Metada, Tag

TagResource = TagResource_for("xrt", Tag)
KeywordResource = KeywordResource_for("xrt", Keyword)
DataLocationResource = DataLocationResource_for("xrt", DataLocation)
MetadaResource = MetadaResource_for("xrt", Metada, TagResource)
