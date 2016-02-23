from pyfits import Header
from xrt.tools.populate import field_values
from xrt.models import Metadata
fields = Metadata._meta.get_fields()


metadatas = Metadata.objects.only('fits_header').filter(wavemin__isnull=True)
packet_size = 1000


log = open('repopulate.log', 'w')
while metadatas.exists():
	print "Processing ", packet_size
	for metadata in metadatas[:packet_size]:
		log.write("%s\n" % metadata.oid)
		try:
			header = Header.fromstring(metadata.fits_header)
			values = field_values(fields, header)
			metadata.__dict__.update(values)
			metadata.save()
		except Exception, why:
			print metadata.oid, why

