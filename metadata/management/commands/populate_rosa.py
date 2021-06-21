import requests
from lxml import html

from django.core.management.base import BaseCommand, CommandError
from ..logger import Logger

from metadata.management.records.rosa import Record
from dataset.models import DataLocation

base_url = 'https://star.pst.qub.ac.uk/webdav/public/fchroma/2014-10-25'

def get_archive_folder(url, auth=None):
	'''Get all the archive folders url'''
	
	archive_folders = list()
	for target in Record.data_properties:
		for channel in Record.data_properties[target]['CHANNEL']:
			archive_folders.append(url + '/' + target + '/' + channel + '/')
	return archive_folders

def get_file_urls(url, auth=None):
	archive_folders = get_archive_folder(url, auth)
	file_urls = list()
	for archive_folder in archive_folders:
		response = requests.get(archive_folder, auth=auth)
		doc = html.fromstring(response.text)
		doc.make_links_absolute(archive_folder)
		
		for element, attribute, link, pos in doc.iterlinks():
			if attribute.lower() == 'href' and element.text and not element.text.lower().startswith('parent directory'):
				file_urls.append(link)
	
	return file_urls


class Command(BaseCommand):
	help = 'Populate the Metadata and DataLocation for ROSA'
	
	def add_arguments(self, parser):
		parser.add_argument('--debug', default = False, action='store_true', help='Show debugging info')
		parser.add_argument('--update', default = False, action='store_true', help='Update metadata even if already present in DB')
	
	def handle(self, **options):
		
		log = Logger(self, debug=options['debug'])
		
		# Populate the dataset
		for file_url in get_file_urls(base_url, auth=Record.auth):
			if file_url.endswith('fits'):
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
