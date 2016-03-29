from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetaDataResource_for

from chrotel.models import Keyword, DataLocation, MetaData, Tag

TagResource = TagResource_for("chrotel", Tag)
KeywordResource = KeywordResource_for("chrotel", Keyword)
DataLocationResource = DataLocationResource_for("chrotel", DataLocation)
MetaDataResource = MetaDataResource_for("chrotel", MetaData, TagResource)
