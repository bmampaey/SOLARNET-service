from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetaDataResource_for

from themis.models import Keyword, DataLocation, MetaData, Tag

TagResource = TagResource_for("themis", Tag)
KeywordResource = KeywordResource_for("themis", Keyword)
DataLocationResource = DataLocationResource_for("themis", DataLocation)
MetaDataResource = MetaDataResource_for("themis", MetaData, TagResource)
