from common.resources import KeywordResource_for, DataLocationResource_for, MetaDataResource_for

from swap.models import Keyword, DataLocation, MetaData

KeywordResource = KeywordResource_for("swap", Keyword)
DataLocationResource = DataLocationResource_for("swap", DataLocation)
MetaDataResource = MetaDataResource_for("swap", MetaData)
