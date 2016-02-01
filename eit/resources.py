from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetadaResource_for

from eit.models import Keyword, DataLocation, Metada, Tag

TagResource = TagResource_for("eit", Tag)
KeywordResource = KeywordResource_for("eit", Keyword)
DataLocationResource = DataLocationResource_for("eit", DataLocation)
MetadaResource = MetadaResource_for("eit", Metada, TagResource)
