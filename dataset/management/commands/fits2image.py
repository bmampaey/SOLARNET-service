# -*- coding: utf-8 -*-
import sys, os
import argparse
import logging
from datetime import timedelta, datetime

from django.core.management.base import BaseCommand, CommandError
import numpy, pyfits
from skimage import io, exposure
from ..logger import Logger

class Command(BaseCommand):
	help = 'Generate a preview image from a fits file, rescaling intensities between a lower and upper percentile'
	
	def add_arguments(self, parser):
		parser.add_argument('--debug', '-d', default=False, action='store_true', help='Set the logging level to debug')
		parser.add_argument('--outdir', '-o', default='.', help='Directory where to write the results.')
		parser.add_argument('--extension', '-e', default='jpg', help='Extension type of the result image.')
		parser.add_argument('--HDU', '-H', default=0, type=int, help='The HDU number of the image')
		parser.add_argument('--lower_percentile', '-l', default=2, type=int, help='The lower percentile to cut the image')
		parser.add_argument('--upper_percentile', '-u', default=98, type=int, help='The upper percentile to cut the image')
		parser.add_argument('filenames', nargs='+', help='The paths of the input files.')
		
	def handle(self, **options):
		
		log = Logger(self, debug=options['debug'])
		
		for filename in options['filenames']:
			log.info('Converting file %s', filename)
			fits = pyfits.open(filename)
			img = fits[options['HDU']].data
			while img.ndim > 2:
				img = img[0]
			lower_percentile, upper_percentile = numpy.percentile(img, (options['lower_percentile'], options['upper_percentile']))
			img_rescale = exposure.rescale_intensity(img, in_range=(lower_percentile, upper_percentile))
			outfilename, trash = os.path.splitext(os.path.basename(filename))
			outfilename = os.path.join(options['outdir'], outfilename + '.' + options['extension'])
			io.imsave(outfilename, img_rescale)
			log.info('Wrote file %s', outfilename)

