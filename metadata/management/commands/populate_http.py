from importlib import import_module
import requests
from lxml import html
from fnmatch import fnmatch
from urlparse import urlparse
import logging

from django.core.management.base import BaseCommand, CommandError
from metadata.models import Tag
from ..logger import Logger

def skip_link(base_url, element, attribute, link, excludes=[], same_netloc = True, text_links_only = True):
	'''Check if a link should be skipped'''
	if attribute.lower() != 'href':
		return 'Not href'
	
	if text_links_only and not element.text:
		return 'Not text link'
	
	base_url_parts = urlparse(base_url)
	
	
	if same_netloc and link_parts.netloc != base_url_parts.netloc:
		return 'Different netloc'
	
	if excludes and any(fnmatch(link_parts.path, pattern) for pattern in excludes):
		return 'Match exclude'
	
	return False

def match_any(url, patterns):
	path = urlparse(url).path
	return patterns and any(fnmatch(path, pattern) for pattern in patterns)

def get_links(base_url, max_depth=None, matches = [], excludes = [], auth=None, log=logging):
	'''Get all the links on a website'''
	
	netloc = urlparse(base_url).netloc
	
	uninspected_urls = [(base_url, 0)]
	
	# Always yield back the base_url
	yield base_url
	
	inspected_urls = []
	
	while uninspected_urls:
		url, depth = uninspected_urls.pop()
		
		# If needed, we inspect the url to find more links
		if max_depth is not None and depth >= max_depth:
			log.debug('Skipping %s : depth %s >= max depth', url, depth)
		elif url in inspected_urls:
			log.debug('Skipping %s : Already inspected', url)
		elif match_any(url, excludes):
			log.debug('Skipping %s : Match exclude', url)
			inspected_urls.append(url)
			log.info('Inspecting %s with depth %s', url, depth)
			
			try:
				response = requests.get(url, auth=auth)
				doc = html.fromstring(response.text)
				doc.make_links_absolute(response.url)
				
				for element, attribute, link, pos in doc.iterlinks():
					log.debug('Yielding %s', link)
						yield link
					skip = skip_link(base_url, element, attribute, link, excludes = excludes)
					if skip:
						log.debug('Skipping %s : %s', link, skip)
					else:
						log.debug('Added %s for later inspection', link)
						urls.append((link, depth+1))
			
			except Exception, why:
				log.error('Critical error while getting url: %s', why)

class Command(BaseCommand):
	help = 'Populate the Metadata and DataLocation for a dataset from Fits files on an HTTP server'
	
	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The id of the dataset')
		parser.add_argument('url', help='URL of the webserver')
		parser.add_argument('--match', '-m', nargs='+', help='Patterns of the fits files, e.g. "*.fits"')
		parser.add_argument('--exclude', '-e', nargs='*', help='Patterns of files to exclude, e.g. "*.png" or "*/bad_directory/*"')
		parser.add_argument('--max_depth', type=int, help='The maximum depth recursion')
		parser.add_argument('--update', default = False, action='store_true', help='Update metadata even if already present in DB')
		parser.add_argument('--tags', default = [], nargs='*', help='A list of tag names to set to the metadata')
		parser.add_argument('--debug', default = False, action='store_true', help='Show debugging info')
	
	def handle(self, **options):
		
		log = Logger(self, debug=options['debug'])
		
		#TODO test the script
		import pdb; pdb.set_trace()
		#raise CommandError('Untested script')
		
		# Import the record classes for the dataset
		try:
			records = import_module('metadata.management.records.' + options['dataset'])
			Record = records.Record
		except (ImportError, AttributeError):
			raise CommandError('No RecordFromFitsFile class for dataset %s' % options['dataset'])
		
		tags = list()
		for tag_name in options['tags']:
			tag, created = Tag.objects.get_or_create(name=tag_name)
			if created:
				log.info('Created Tag %s', tag_name)
			tags.append(tag)
		
		# Populate the dataset
		for file_url in get_links(options['url'], max_depth=options['max_depth'], auth=Record.auth, excludes=options['exclude'] + options['match'], log=log):
			if any(fnmatch(file_url, pattern) for pattern in options['match']):
				log.info('Found fits file at %s', file_url)
#				try:
#					record = Record(file_url, log=log)
#					record.create(tags=tags, update=options['update'])
#				except Exception, why:
#					log.error('Error creating record for "%s": %s', file_url, why)
			else:
				log.debug('Skipping file at %s', file_url)

