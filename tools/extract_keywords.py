#!/usr/bin/python
import pyfits
import glob
import sys, os, os.path
import csv
from datetime import datetime
import dateutil.parser
import logging
import argparse
import re

def get_keywords(filename, hdu = 0, exclude = [], get_comment = False, get_history = False):
	
	try:
		hdus = pyfits.open(filename)
		header = hdus[hdu].header.ascard
	except Exception, why:
		logging.critical("Could not open file %s: %s.", filename, why)
		return None
	
	keywords = [["db_column", "name", "python_type", "unit", "description"]]
	comment_index = 0
	history_index = 0
	for card in header:
		try:
			key = card.key
			value = card.value
			comment = card.comment
		except Exception, why:
			logging.error("Could not parse card %s: %s. Skipping.", card, why)
			continue
		if key in exclude:
			continue
		elif key.lower() == "history":
			if not get_history:
				logging.info("Ommiting history %s", value) 
				continue
			else:
				value.strip(" \t\n-")
				if not value:
					logging.info("Ommiting empty history")
					continue	
				# history keywords are not unique
				db_column = "history_%d" % history_index
				history_index += 1
		
		elif key.lower() == "comment":
			if not get_comment:
				logging.info("Ommiting comment %s", value)
				continue
			else:
				value.strip(" \t\n-")
				if not value:
					logging.info("Ommiting empty comment")
					continue	
				# comment keywords are not unique
				db_column = "comment_%d" % comment_index
				comment_index += 1
		else:
			# Replace all weird char into the key
			db_column = column_name(key)
		
		python_type = value_type(value)
		unit, description = extract_unit(comment)
		keywords.append([db_column, key, python_type, unit, description])
	
	return keywords

def column_name(key):
	return re.sub("\W", "_", key.strip()).lower()

def value_type(value):
	if isinstance(value, float):
		return "float"
	elif isinstance(value, (int, long)):
		return "int"
	elif isinstance(value, datetime):
		return "datetime"
	elif isinstance(value, bool):
		return "bool"
	else:
		return "str"

unit_pattern =  re.compile(r"\s*(\[\s*(?P<unit>[^\]]*)\s*\])?(?P<comment>.*)\s*")
def extract_unit(comment):
	try:
		parts = unit_pattern.match(comment).groupdict()
	except Exception:
		logging.error("Could not parse unit and comment from string %s. Using string as comment.", comment)
		return "", comment.strip()
	else:
		return parts["unit"].strip() if parts["unit"] is not None else "", parts["comment"].strip()
		
	
# Start point of the script
if __name__ == "__main__":
	
	script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
	# Default name for the log file
	log_filename = os.path.join('.', script_name+'.log')
	
	# Get the arguments
	parser = argparse.ArgumentParser(description='Extract keywords from fits files.')
	parser.add_argument('--debug', '-d', default=False, action='store_true', help='set the logging level to debug for the log file')
	parser.add_argument('--comments', '-C', default=False, action='store_true', help='Extract pure comment keywords')
	parser.add_argument('--history', '-H', default=False, action='store_true', help='Extract history keywords')
	parser.add_argument('--exclude', '-E', default = ["DATASUM", "CHECKSUM", "SIMPLE", "BITPIX"], nargs='*', help='Keywords to exclude (in small caps)')
	parser.add_argument('--hdu', '-u', default=0, type=int, help='The number of the HDU. Typically 0, but can be 1 for tile compressed images.')
	parser.add_argument('--sql', '-s', default=None, help='Output as sql insert statements. Pass the table name.')
	parser.add_argument('filename', help='The path of the fits file')
	
	args = parser.parse_args()
	if args.debug:
		logging.basicConfig(level = logging.DEBUG, format='%(levelname)-8s: %(message)s')
	else:
		logging.basicConfig(level = logging.INFO, format='%(levelname)-8s: %(message)s')
	
	keywords = get_keywords(args.filename, args.hdu, args.exclude, args.comments, args.history)
	if args.sql:
		columns = ", ".join(keywords[0]) 
		for row in keywords[1:]:
			values = "','".join(row)
			print "insert into %s (%s) values ('%s');" % (args.sql, columns, values)
		
	else:	
		writer = csv.writer(sys.stdout)
		writer.writerows(keywords)
	