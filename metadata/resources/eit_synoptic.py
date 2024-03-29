# Generated by command write_metadata_files version 1
from metadata.models import EitSynoptic
from .base_metadata import BaseMetadataResource

__all__ = ['EitSynopticResource']


class EitSynopticResource(BaseMetadataResource):
	'''RESTful resource for model EitSynoptic'''
	
	class Meta(BaseMetadataResource.Meta):
		abstract = False
		queryset = EitSynoptic.objects.all()
		resource_name = 'metadata_eit_synoptic'
