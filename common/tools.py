import requests
import StringIO
import pyfits
import zlib

def get_fits_header(url, min_size = 2880, zipped = False, file_start = 0):
	'''Try to extract the header from a fits file by doing a partial download of the url'''
	
	start = file_start
	end = file_start + min_size
	
	# We store the response in a pseudo file for pyfits
	fits_file = StringIO.StringIO()
	
	# If fits file is zipped, the response content must be decompressed before writing it to the pseudo file
	if zipped:
		decompressor = zlib.decompressobj(zlib.MAX_WBITS | 16)
	
	while True:
		# We download the file by chunck, by specifying the desired range in the header, both bounds are inclusive 
		response = requests.get(url, headers = {'Range': 'Bytes=%s-%s' % (start, end - 1)})
		
		if zipped:
			fits_file.write(decompressor.decompress(response.content))
		else:
			fits_file.write(response.content)
		
		# It is necessary to rewind the file for pyfits
		fits_file.seek(0)
		
		# Try to read a full header from the pseudo file, if header is partial, an IOError will be raised
		try:
			header = pyfits.Header.fromfile(fits_file)
		except IOError:
			# Header is partial, we need to read more from the file
			start += 2880
			end += 2880
		else:
			# Header is complete
			# Extract the real file size from the response header
			if 'content-range' in response.headers:
				file_size = int(response.headers['content-range'].split('/')[1])
			else:
				file_size = int(response.headers['content-length'])
			break
	
	return file_size, header

