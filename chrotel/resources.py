from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetadaResource_for

from chrotel.models import Keyword, DataLocation, Metada, Tag

TagResource = TagResource_for("chrotel", Tag)
KeywordResource = KeywordResource_for("chrotel", Keyword)
DataLocationResource = DataLocationResource_for("chrotel", DataLocation)
MetadaResource = MetadaResource_for("chrotel", Metada, TagResource)
