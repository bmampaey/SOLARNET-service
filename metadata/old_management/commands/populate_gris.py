import requests
from lxml import html

from django.core.management.base import BaseCommand, CommandError
from ..logger import Logger

from metadata.management.records.gris_lev1 import Record
from dataset.models import DataLocation

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

def get_file_urls(url, auth=None):
	archive_folders = get_archive_folder(url, auth)
	file_urls = list()
	for archive_folder in archive_folders:
		response = requests.get(archive_folder, auth=auth)
		doc = html.fromstring(response.text)
		doc.make_links_absolute(archive_folder)
		
		for element, attribute, link, pos in doc.iterlinks():
			if attribute.lower() == 'href' : # and not element.text.lower().startswith('parent directory'):
				file_urls.append(link)
	
	return file_urls


class Command(BaseCommand):
	help = 'Populate the Metadata and DataLocation for GRIS'
	
	def add_arguments(self, parser):
		parser.add_argument('--debug', default = False, action='store_true', help='Show debugging info')
		parser.add_argument('--update', default = False, action='store_true', help='Update metadata even if already present in DB')
	
	def handle(self, **options):
		
		log = Logger(self, debug=options['debug'])
		
		# Populate the dataset
		for file_url in get_file_urls(base_url, auth=Record.auth):
			if file_url.endswith('c') or file_url.endswith('r'):
				log.info('Found fits file at %s', file_url)
				
				if not options['update'] and DataLocation.objects.filter(file_url=file_url).exists():
					log.info('Skipping fits file at %s, already parsed', file_url)
					continue
				
				try:
					record = Record(file_url, log=log)
					record.create(update=options['update'])
				except Exception as why:
					log.error('Error creating record for "%s": %s', file_url, why)
			else:
				log.info('Skipping file at %s, not a fits file', file_url)
