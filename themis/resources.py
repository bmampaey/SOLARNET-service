from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetadaResource_for

from themis.models import Keyword, DataLocation, Metada, Tag

TagResource = TagResource_for("themis", Tag)
KeywordResource = KeywordResource_for("themis", Keyword)
DataLocationResource = DataLocationResource_for("themis", DataLocation)
MetadaResource = MetadaResource_for("themis", Metada, TagResource)
