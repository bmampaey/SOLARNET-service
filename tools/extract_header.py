from sunpy.net import vso
import pyfits
from datetime import datetime, timedelta
client = vso.VSOClient()
qr = client.query_legacy(tstart='2014/09/01', tend='2014/09/02', instrument='Chrotel')
hdus = pyfits.open(z.fileid, mode='denywrite')
header = pyfits.header.Header
header.fromstring(h.header.tostring())

from chrotel.models import *
base_url = 'http://sdac.virtualsolar.org/cgi-bin/get/{provider}/{fileid}'
url = base_url.format(provider=record.provider, fileid=record.fileid)

start = datetime(2014, 1, 1)
end = datetime(2015, 1, 1)
increment = timedelta(days = 1)
instrument='Chrotel'
while start <= end:
	qr = client.query_legacy(start, min(start + increment, end), instrument=instrument)
	if qr.num_records() > 0:
		for record in qr:
			hdus = pyfits.open(record.fileid)
			meta_data = MetaData.objects.create(id = record.time.start, fitsheader = hdus[0].header.tostring())
			DataLocation.objects.create(meta_data = meta_data, url = base_url.format(provider=record.provider, fileid=record.fileid), file_size = record.size, thumbnail = record.extra.thumbnail.lowres)

