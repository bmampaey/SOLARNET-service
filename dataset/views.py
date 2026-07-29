import numpy
import requests
from astropy.io import fits
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView, View
from PIL import Image, ImageOps

from dataset.models import Dataset

__all__ = ['DataView', 'ThumbnailView', 'Image2ThumbnailView', 'Fits2ThumbnailView']


# TODO allow to download by oid or using filter (see django_filter), if there is more than one gives back the first one
# TODO should we check online flag ?
class DataView(RedirectView):
	"""View to download the data by looking up the metadata resource name and oid"""

	http_method_names = ['get', 'head']

	def get_redirect_url(self, dataset_name, metadata_oid):
		dataset = get_object_or_404(Dataset, name=dataset_name)
		metadata = get_object_or_404(dataset.metadata_model, oid=metadata_oid)
		return metadata.data_location.file_url


class ThumbnailView(RedirectView):
	"""View to download the thumbnail by looking up the metadata resource name and metadata oid"""

	http_method_names = ['get', 'head']

	def get_redirect_url(self, dataset_name, metadata_oid):
		dataset = get_object_or_404(Dataset, name=dataset_name)
		metadata = get_object_or_404(dataset.metadata_model, oid=metadata_oid)
		return metadata.data_location.thumbnail_url


class Image2ThumbnailView(View):
	"""View to convert an image to a thumbnail"""

	def get(self, request, *args, **kwargs):
		"""Return a response with the thumbnail"""
		try:
			image = Image.open(requests.get(request.GET['url'], stream=True).raw)
			image.thumbnail((512, 512))
			thumbnail = ContentFile(b'', name='thumbnail.jpg')
			image.save(thumbnail, format='jpeg')
			thumbnail.seek(0)
		except Exception as why:
			raise Http404 from why
		return FileResponse(thumbnail)


class Fits2ThumbnailView(View):
	"""View to convert a FITS file to a thumbnail"""

	def get(self, request, *args, **kwargs):
		"""Return a response with the thumbnail"""
		try:
			# Read the  image data from the FITS file (astropy.io.fits.open accepts an URL)
			fits_file = fits.open(request.GET['url'])
			hdu = fits_file[int(request.GET.get('hdu', 0))]
			# Convert the data to a PIL image
			data = numpy.nan_to_num(hdu.data, nan=0.0, posinf=0.0, neginf=0.0)
			data_min, data_max = data.min(), data.max()
			data = (data - data_min) / (data_max - data_min) * 255.0
			image = Image.fromarray(data.astype('uint8'))

			# Use PIL to adjust the contrast
			# Remove the percentiles
			cutoff = (float(request.GET.get('min_percentile', 0)), 100 - float(request.GET.get('max_percentile', 100)))
			image = ImageOps.autocontrast(image, cutoff=cutoff)
			# Histo Equalize
			if request.GET.get('histo_equalize', False):
				image = ImageOps.equalize(image)
			image.thumbnail((512, 512))

			# Write the thumbnail to the in memory file
			thumbnail = ContentFile(b'', name='thumbnail.jpg')
			image.save(thumbnail, format='jpeg')
		except Exception as why:
			raise Http404 from why
		else:
			# The file must be rewinded before sending it
			thumbnail.seek(0)
			return FileResponse(thumbnail)
