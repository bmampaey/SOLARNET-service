#!/usr/bin/python

import sys, os
import logging
import argparse
import re
from datetime import datetime
from collections import defaultdict
import csv
import pyfits

attribute_names = ["db_column", "name", "python_type", "unit", "description"]

def get_keywords(filename, hdu = 0, excluded_keywords = []):
	"""Return the list of the keyword attributes found in a fits file"""
	try:
		hdus = pyfits.open(filename)
		header = hdus[hdu].header.cards
	except Exception, why:
		logging.error("Could not open file %s: %s. Skipping", filename, why)
		return None
	keywords = list()
	
	for card in header:
		try:
			keyword = card.keyword
			value = card.value
			comment = card.comment
		except Exception, why:
			logging.error("Could not parse card %s: %s. Skipping.", card, why)
			continue
		if keyword.lower() in excluded_keywords:
			logging.info("Skipping excluded keyword %s", keyword)
			continue
		else:
			db_column = get_column_name(keyword)
		
		python_type = value_type(value)
		unit, description = extract_unit(comment)
		attributes = dict(zip(attribute_names, [db_column, keyword, python_type, unit, description]))
		logging.debug("Adding keyword %s with following attributes %s", keyword, attributes)
		keywords.append(attributes)
	
	return keywords

def get_column_name(key):
	"""Replace all weird char into the key by undescore"""
	return re.sub("\W", "_", key.strip()).lower()

iso8601 = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})([T ](?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})([,.](?P<mic>\d+))?)?((?P<tzZulu>Z)|[+-](?P<tzhour>\d{2}):?(?P<tzmin>\d{2}))?$")
def value_type(value):
	"""Try to guess the type of a value"""
	if isinstance(value, float):
		return "float"
	elif isinstance(value, (int, long)):
		return "int"
	elif isinstance(value, datetime):
		return "datetime"
	elif isinstance(value, str):
		if iso8601.match(value):
			return "datetime"
		else:
			return "str"
	else:
		logging.warning("Unexpected data type for value %s: %s", value, type(value))
		return type(value)

unit_pattern =  re.compile(r"\s*(\[\s*(?P<unit>[^\]]*)\s*\])?(?P<comment>.*)\s*")
def extract_unit(comment):
	"""Extract the unit part of a fits comment if any"""
	try:
		parts = unit_pattern.match(comment).groupdict()
	except Exception:
		logging.warning("Could not parse unit and comment from string %s. Using string as comment.", comment)
		return "", comment.strip()
	else:
		return parts["unit"].strip() if parts["unit"] is not None else "", parts["comment"].strip()
		
	
# Start point of the script
if __name__ == "__main__":
	
	# Get the arguments
	parser = argparse.ArgumentParser(description='Extract keyword attributes from fits files and upload them to the SDA.')
	parser.add_argument('--debug', '-d', default=False, action='store_true', help='Set the logging level to debug')
	parser.add_argument('--exclude', '-E', default = ["DATASUM", "CHECKSUM", "SIMPLE", "BITPIX"], nargs='*', help='Keywords to exclude')
	parser.add_argument('--hdu', '-u', default=0, type=int, help='The number of the HDU. Typically 0, but can be 1 for tile compressed images.')
	parser.add_argument('--dataset', '-D', required=True, help='The dataset id. Required.')
	parser.add_argument('filename', nargs='+', help='The path to one or more fits files')
	
	args = parser.parse_args()
	if args.debug:
		logging.basicConfig(level = logging.DEBUG, format='%(levelname)-8s: %(message)s')
	else:
		logging.basicConfig(level = logging.INFO, format='%(levelname)-8s: %(message)s')
	
	csv_filename = args.dataset + "_keywords.xls"
	try:
		csv_file = open(csv_filename, "w")
	except IOError, why:
		print "Could not create the file", csv_filename, ":", str(why)
		sys.exit(1)
	
	excluded_keywords = [keyword.lower() for keyword in args.exclude]
	
	all_keywords = defaultdict(lambda : defaultdict(set))
	
	for filename in args.filename:
		logging.info("Getting keywords for file %s", filename)
		keywords = get_keywords(filename, args.hdu, excluded_keywords)
		for attributes in keywords:
			for name, value in attributes.iteritems():
				all_keywords[attributes["db_column"]][name].add(value)
	
	for db_column, attributes in all_keywords.iteritems():
		for name, values in attributes.iteritems():
			values.discard("")
			if len(values) > 1:
				print "Attribute", name, "for db_column", db_column, "has more than one value:"
				for i, value in enumerate(values):
					print "\t", value
				new_value = raw_input("Please enter the correct value:")
				attributes[name] = new_value
			elif len(values) == 1:
				attributes[name] = values.pop()
			else:
				attributes[name] = None
			logging.debug("Final value for %s attribute %s: %s", db_column, name, attributes[name])
	
	logging.debug("Writting keywords attributes to file %s", csv_filename)
	
	writer = csv.DictWriter(csv_file, attribute_names, quoting=csv.QUOTE_NONNUMERIC)
	writer.writeheader()
	print "%8s, %8s, %8s, %10s, %70s" % tuple(attribute_names)
	for attributes in all_keywords.itervalues():
		writer.writerow(attributes)
		print "%8s, %8s, %8s, %10s, %70s" % tuple(attributes[name] for name in attribute_names)
	
	csv_file.close()
	
	print "The information above was written to the file", csv_filename, "please review it and send it to the SDA adminsitrator"

#	response = raw_input("Do you agree [Y/N]:")
#	while response not in ["Y", "N"]:
#		response = raw_input("Please answer Y or N:")
#	
#	if response == "Y":
#		pass
#	else:
#		pass
#	
#	


