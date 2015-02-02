#!/usr/bin/python

import sys, os
import logging
import argparse
import pyfits
import slumber
import urlparse, urllib
from datetime import datetime, date, time
from dateutil.parser import parse as parse_date

SERVER_ADDRESS = "http://solarnet.oma.be/api"

# This method has to be overriden
def make_id(meta_data):
	return long(parse_date(meta_data['date_obs']).strftime("%Y%m%d%H%M%S"))


def get_meta_data(filepath, fields, keywords, hdu = 0):
	"""Return the meta-data found in a fits file header"""
	
	meta_data = dict()
	
	hdus = pyfits.open(filepath)
	header = hdus[hdu].header
	
	for field, attributes in fields.iteritems():
		if field in("id", "tags") or attributes["readonly"]:
			continue
		
		try:
			keyword = keywords[field]
		except Exception, why:
			logging.error("No keyword for field %s. Skipping.", field)
			continue
		try:
			value = header[keyword]
		except Exception, why:
			logging.error("No meta-data for keyword %s (field %s). Skipping.", keyword, field)
			continue
		if not attributes['type'].startswith(type(value).__name__):
			logging.warning("Type mismatch between meta-data %s and expected type %s for keyword %s (field %s)", type(value), attributes['type'], keyword, field)
			try:
				value = convert(value, attributes['type'])
				logging.info("Value succesfuly converted to %s: %r", attributes['type'], value)
			except Exception:
				logging.error("Could not convert meta-data %s to expected type %s for keyword %s (field %s). Skipping.", value, attributes['type'], keyword, field)
				continue
		meta_data[field] = value
	
	return meta_data

def convert(value, python_type):
	if python_type == "bool":
		return bool(value)
	elif python_type == "float":
		return float(value)
	elif python_type == "int":
		return int(value)
	elif python_type == "long":
		return long(value)
	elif python_type == "datetime":
		return parse_date(value).isoformat()
	elif python_type == "str":
		if isinstance(value, (datetime, date, time)):
			return value.isoformat()
		else:
			return str(value)
	else:
		raise Exception("Unknown type %s" % python_type)

def get_keywords(dataset, api = slumber.API(SERVER_ADDRESS)):

	return keywords

# Start point of the script
if __name__ == "__main__":
	
	# Get the arguments
	parser = argparse.ArgumentParser(description='Extract meta-data from fits files and upload them to the SDA.')
	parser.add_argument('--debug', '-d', default=False, action='store_true', help='Set the logging level to debug')
	parser.add_argument('--hdu', '-u', default=0, type=int, help='The number of the HDU. Typically 0, but can be 1 for tile compressed images.')
	parser.add_argument('--tags', '-t', default = [], nargs='*', help='Tags to be associated with the file.')
	parser.add_argument('dataset', help='The dataset id.')
	parser.add_argument('base_url', help='The base of the url to acces the file.')
	parser.add_argument('username', help='Your SDA username')
	parser.add_argument('password', help='Your SDA password')
	parser.add_argument('filepath', nargs='+', help='The relative path to one or more fits files. Be carrefull, the final url will be base_url + filepath')
	
	args = parser.parse_args()
	if args.debug:
		logging.basicConfig(level = logging.DEBUG, format='%(levelname)-8s: %(message)s')
	else:
		logging.basicConfig(level = logging.INFO, format='%(levelname)-8s: %(message)s')
	
	API = slumber.API(SERVER_ADDRESS, auth = (args.username, args.password))
	
	# Get or create the Tag ressource
	tag_api = API.v1(args.dataset + "_tag")
	
	tags = list()
	for tag_name in args.tags:
		try: # Try to get the tag ressource
			tag_objects = tag_api.get(name=tag_name)['objects']
		except Exception, why:
			logging.critical("Error getting tag %s: %s", tag_name, why)
			sys.exit(1)
		
		if tag_objects:
			tag = tag_objects[0]
		else: # The tag does not exists, let's try to create it
			try:
				tag = tag_api.post({"name": tag_name})
			except Exception, why:
				logging.critical("Tag %s does not exist and could not be created: %s", tag_name, why)
				sys.exit(1)
		tags.append(urllib.unquote(tag['resource_uri']))
	
	# Make a translation table field name-> keyword name
	keyword_api = API.v1(args.dataset + "_keyword")
	
	try:
		keyword_attributes = keyword_api.get(limit=0)['objects']
	except Exception, why:
		logging.critical("Could not get keywords for dataset %s: %s", args.dataset, why)
		sys.exit(1)
	else:
		logging.debug("Recieved following keywords for dataset %s:\n%s", args.dataset, keyword_attributes)
	
	keywords = dict()
	for keyword_attribute in keyword_attributes:
		keywords[keyword_attribute['db_column']] = keyword_attribute['name']
	
	# Get the schema of the meta_sata ressource to extract the fields properties
	meta_data_api = API.v1(args.dataset + "_meta_data")
	
	try:
		schema = meta_data_api.schema.get()
	except Exception, why:
		logging.critical("Could not get schema for dataset %s: %s", args.dataset, why)
		sys.exit(1)
	else:
		logging.debug("Recieved following schema for dataset %s:\n%s", args.dataset, schema)
	
	data_location_api = API.v1(args.dataset + "_data_location")
	
	# Extract the meta-data from the fits files and upload it to the server
	for filepath in args.filepath:
		logging.info("Parsing meta-data of file %s", filepath)
		try:
			meta_data = get_meta_data(filepath, schema['fields'], keywords, args.hdu)
		except Exception, why:
			logging.critical("Error parsing file %s: %s. Skipping", filepath, why)
		else:
			meta_data['id'] = make_id(meta_data)
			meta_data['tags'] = tags
			logging.info("Uploading following data:\n%s", "\n".join(["%8s = %r" % (field, value) for field,value in meta_data.iteritems()]))
			try:
				meta_data_object = meta_data_api.post(meta_data)
			except Exception, why:
				logging.critical("Could not upload meta-data to server: %s", why)
				sys.exit(1)
		
		# Upload the data_location to the server
		logging.info("Uploading data location of file %s", filepath)
		try:
			data_location_api.post({"meta_data": urllib.unquote(meta_data_object['resource_uri']), "url": urlparse.urljoin(args.base_url, filepath), "file_size": os.path.getsize(filepath)})
		except Exception, why:
			logging.critical("Could not upload data location to server: %s", why)
			sys.exit(1)
