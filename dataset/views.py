from django.views.generic import RedirectView, View
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from PIL import Image
from astropy.io import fits
import requests
import numpy


from dataset.models import Dataset

__all__ = ['DataView', 'ThumbnailView', 'Image2ThumbnailView', 'Fits2ThumbnailView']

# TODO allow to download by oid or using filter (see django_filter), if there is more than one gives back the first one
# TODO should we check online flag ?
class DataView(RedirectView):
	'''View to download the data by looking up the metadata resource name and oid'''
	http_method_names = ['get', 'head']
	
	def get_redirect_url(self, dataset_name, metadata_oid):
		dataset = get_object_or_404(Dataset, name=dataset_name)
		metadata = get_object_or_404(dataset.metadata_model, oid=metadata_oid)
		return metadata.data_location.file_url


class ThumbnailView(RedirectView):
	'''View to download the thumbnail by looking up the metadata resource name and metadata oid'''
	http_method_names = ['get', 'head']
	
	def get_redirect_url(self, dataset_name, metadata_oid):
		dataset = get_object_or_404(Dataset, name=dataset_name)
		metadata = get_object_or_404(dataset.metadata_model, oid=metadata_oid)
		return metadata.data_location.thumbnail_url


class Image2ThumbnailView(View):
	'''View to convert an image to a thumbnail'''
	
	def get(self, request, *args, **kwargs):
		'''Return a response with the thumbnail'''
		try:
			image = Image.open(requests.get(request.GET['url'], stream=True).raw)
			image.thumbnail((512,512))
			thumbnail = ContentFile(b'', name='thumbnail.jpg')
			image.save(thumbnail, format='jpeg')
			thumbnail.seek(0)
		except Exception as why:
			raise Http404 from why
		return FileResponse(thumbnail)


class Fits2ThumbnailView(View):
	'''View to convert a FITS file to a thumbnail'''
	
	def get(self, request, *args, **kwargs):
		'''Return a response with the thumbnail'''
		try:
			# Read the  image data from the FITS file (astropy.io.fits.open accepts an URL)
			fits_file = fits.open(request.GET['url'])
			hdu = fits_file[int(request.GET.get('hdu', 0))]
			data = hdu.data
			# Remove the percentiles
			min_percentile, max_percentile = numpy.percentile(data, [float(request.GET.get('min_percentile', 0)), float(request.GET.get('max_percentile', 100))])
			data[data < min_percentile] = min_percentile
			data[data > max_percentile] = max_percentile
			# Rescale the data to the 0..255 range
			scaled_data = ((data - min_percentile) * (255. / (max_percentile - min_percentile))).round()
			# Create a thumbnail from the rescaled data
			image = Image.fromarray(scaled_data.astype('uint8'))
			image.thumbnail((512,512))
			# Write the thumbnail to the in memory file
			thumbnail = ContentFile(b'', name='thumbnail.jpg')
			image.save(thumbnail, format='jpeg')
		except Exception as why:
			raise Http404 from why
		else:
			# The file must be rewinded before sending it
			thumbnail.seek(0)
			return FileResponse(thumbnail)
