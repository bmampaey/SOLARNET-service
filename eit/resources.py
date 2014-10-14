from common.resources import KeywordResource_for, DataLocationResource_for, MetaDataResource_for

from eit.models import Keyword, DataLocation, MetaData

KeywordResource = KeywordResource_for("eit", Keyword)
DataLocationResource = DataLocationResource_for("eit", DataLocation)
MetaDataResource = MetaDataResource_for("eit", MetaData)
