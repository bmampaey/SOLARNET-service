#!/usr/bin/env python
# -*- coding: utf-8 -*-
#angstrom Å

# Common imports
import sys, os
import argparse
import logging
from datetime import timedelta, datetime

import numpy, pyfits
from skimage import io, exposure

if __name__ == "__main__":
	
	# Get the arguments
	parser = argparse.ArgumentParser(description='Describe me')
	parser.add_argument('--debug', '-d', default=False, action='store_true', help='Set the logging level to debug')
	parser.add_argument('--outdir', '-o', default='.', help='Directory where to write the results.')
	parser.add_argument('--extension', '-e', default='jpg', help='Extension type of the result image.')
	parser.add_argument('--HDU', '-H', default=0, type=int, help='The HDU number of the image')
	parser.add_argument('--lower_percentile', '-l', default=2, type=int, help='The lower percentile to cut the image')
	parser.add_argument('--upper_percentile', '-u', default=98, type=int, help='The upper percentile to cut the image')
	parser.add_argument('filenames', nargs='+', help='The paths of the input files.')
	
	args = parser.parse_args()
	
	# Setup the logging
	if args.debug:
		logging.basicConfig(level = logging.DEBUG, format='%(levelname)-8s: %(message)s')
	else:
		logging.basicConfig(level = logging.INFO, format='%(levelname)-8s: %(message)s')
	
	for filename in args.filenames:
		logging.info('Converting file %s', filename)
		fits = pyfits.open(filename)
		img = fits[args.HDU].data
		lower_percentile, upper_percentile = numpy.percentile(img, (args.lower_percentile, args.upper_percentile))
		img_rescale = exposure.rescale_intensity(img, in_range=(lower_percentile, upper_percentile))
		outfilename, trash = os.path.splitext(os.path.basename(filename))
		outfilename = args.outdir + '/' + outfilename + '.' + args.extension
		io.imsave(outfilename, img_rescale)
		logging.info('Wrote file %s', outfilename)

