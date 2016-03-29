# coding: utf-8

import requests
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits', stream=True)
r.raw
for l in r.raw: print l
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits')
r.raw
for l in r.raw: print len(l)
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits', stream=True, headers = {'Range': 'bytes=0-2879'})
r.status_code
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits', stream=True)
r.status_code
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits', stream=True, headers = {'Range': 'Bytes=0-2879'})
r.status_code
for l in r.raw: print len(l)
for l in r.raw: print l
r.data
r.text
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits', stream=True, headers = {'Range': 'Bytes=0-2879'})
for l in r.raw: print l
r.content
import urllib
get_ipython().magic(u'pinfo urllib.urlretrieve')
urllib.urlretrieve('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits')
get_ipython().magic(u'ls /var/folders/gg/jnq02knj2jldf6jhtqxz6w6w0000gn/T/tmpKB7J66.fits')
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits', stream=True, headers = {'Range': 'Bytes=0-2879'})
with open('output.fits', 'wb') as handle:
 for block in r.iter_content(1024):
   handle.write(block)
import pyfits
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits', stream=True, headers = {'Range': 'Bytes=0-2879'})
h = pyfits.open(r.raw)
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits', stream=True, headers = {'Range': 'Bytes=0-2879'})
import StringIO
f = StringIO.StringIO(r.content)
f.read()
f
f.read()
get_ipython().magic(u'pinfo f.seek')
f.seek(0)
get_ipython().magic(u'pinfo f.seek')
f.read()
f.seek(0)
f = StringIO.StringIO(f)
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits', headers = {'Range': 'Bytes=0-2879'})
f = StringIO.StringIO(r.content)
h = pyfits.open(f)
h
f.seek(0,2)
f.read()
f.write('END')
f.seaak(0)
f.seek(0)
f.read()
f.seek(0)
h = pyfits.open(f)
h
get_ipython().magic(u'history ')
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits', headers = {'Range': 'Bytes=0-5759'})
f = StringIO.StringIO(r.content)
h = pyfits.open(f)
f.seek(0)
a = f.read()
a
r = requests.get('http://sdo5.nascom.nasa.gov/data/aia/synoptic/2015/09/08/H1900/AIA20150908_195400_1600.fits', headers = {'Range': 'Bytes=0-5759'})
r.text
len(a)
r.headers
import zipfile
f.seek(0)
z = zipfile.ZipFile(f)
zipfile.is_zipfile('output.fits')
get_ipython().magic(u'history ')
h = pyfits.open(f, ignore_missing_end = True)
h = pyfits.open(f, ignore_missing_end = True, mode = 'update')
h
q
r.apparent_encoding
r.encoding
r.headers
import zlib
zlib.decompress(a)
a
zlib.decompress(a)
z = zlib.decompressobj()
z.decompress(a)
import sunpy
sunpy.vso.client
from sunpy.net.vso import VSOClient
client = VSOClient()
get_ipython().magic(u'pinfo client.query_legacy')
client.query_legacy(instrument='TRACE')
client.query_legacy('1-1-2010', '1-1-2011',  instrument='TRACE')
client.query_legacy('1/1/2010', '1/1/2011',  instrument='TRACE')
client.query_legacy('2009/01/01', '2010/01/01',  instrument='TRACE')
trace = Out[92]
trace[0]
aia = client.query_legacy('2015/09/08', '2015/09/09', wave = '171'  instrument='AIA')
aia = client.query_legacy('2015/09/08', '2015/09/09', wave = '171' , instrument='AIA')
aia
aia = client.query_legacy('2015/09/08 19:54', '2015/09/09 19:55', wave = '171' , instrument='AIA')
aia
aia[0]
trace[0]
f = pyfits.open('Downloads/tri20090101.0000.fits')
f
hdus = f
for h in hdus:
 print h.header
get_ipython().magic(u'history ')
get_ipython().magic(u'save svo_vso.py')
get_ipython().magic(u'save svo_vso.py 0-108')
