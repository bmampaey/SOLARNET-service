import requests
from requests.auth import HTTPDigestAuth
from lxml import html
from fnmatch import fnmatch
from urlparse import urlparse

from django.core.management.base import BaseCommand, CommandError
from ..logger import Logger

from metadata.management.records.gris_lev1 import Record

base_url = 'http://archive.leibniz-kis.de/pub/gris/'

def get_index_links(url, auth=None):
	'''Get all the links on the index page'''
	response = requests.get(url, auth=auth)
	doc = html.fromstring(response.text)
	doc.make_links_absolute(url)
	
	index_links = list()
	for element, attribute, link, pos in doc.iterlinks():
		if attribute.lower() == 'href' and element.text:
			index_links.append(link)
	
	return index_links

def get_archive_folder(url, auth=None):
	'''Get all the archive folders url'''
	index_links = get_index_links(url, auth)
	
	archive_folders = list()
	for index_link in index_links:
		response = requests.get(index_link, auth=auth)
		doc = html.fromstring(response.text)
		doc.make_links_absolute(index_link)
		
		for element, attribute, link, pos in doc.iterlinks():
			if attribute.lower() == 'href' and element.text and element.text.lower().startswith('go to archive'):
				archive_folders.append(link + '/level1/')
	return archive_folders

def get_fits_files(url, auth=None):
	import pdb; pdb.set_trace()
	archive_folders = get_archive_folder(url, auth)
	fits_files = list()
	for archive_folder in archive_folders:
		response = requests.get(archive_folder, auth=auth)
		doc = html.fromstring(response.text)
		doc.make_links_absolute(archive_folder)
		
		for element, attribute, link, pos in doc.iterlinks():
			if attribute.lower() == 'href' and link.endswith('cc'):
				fits_files.append(link)
	
	return fits_files


class Command(BaseCommand):
	help = 'Populate the Metadata and DataLocation for GRIS'
	
	def handle(self, **options):
		
		log = Logger(self)
		
		# Populate the dataset
		for file_url in get_fits_files(base_url, auth=Record.auth):
			log.info('Found fits file at %s', file_url)
			try:
				record = Record(file_url, log=log)
				record.create()
			except Exception, why:
				log.error('Error creating record for "%s": %s', file_url, why)
