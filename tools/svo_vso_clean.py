# coding: utf-8

base_url = 'http://sdac.virtualsolar.org/cgi-bin/get/{provider}/{fileid}'
import requests
import pyfits
import StringIO

from sunpy.net.vso import VSOClient

client = VSOClient()
records = client.query_legacy('2009/01/01', '2010/01/01',  instrument='TRACE')
record = records[0]
url = base_url.format(provider=record.provider, fileid=record.fileid)
response = requests.get(url, headers = {'Range': 'Bytes=0-2879'})
if response.status_code == 206:
	f = StringIO.StringIO(response.content)
elif response.status_code == 200:
	f = StringIO.StringIO(response.content)
	print "Warning the whole file has been downloaded"
else:
	print "Error, could not download the file", response.status_code

hdus = pyfits.open(f)
