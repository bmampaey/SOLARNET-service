from common.resources import TagResource_for, KeywordResource_for, DataLocationResource_for, MetadaResource_for

from swap_lev1.models import Keyword, DataLocation, Metada, Tag

TagResource = TagResource_for("swap_lev1", Tag)
KeywordResource = KeywordResource_for("swap_lev1", Keyword)
DataLocationResource = DataLocationResource_for("swap_lev1", DataLocation)
MetadaResource = MetadaResource_for("swap_lev1", Metada, TagResource)
