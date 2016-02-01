#!/usr/bin/python
import sys, os
import logging
import argparse
from datetime import datetime
import pandas


def get_field(db_column, python_type):
	if python_type == 'int':
		return db_column + " = models.IntegerField(blank=True, null=True)"
	elif python_type == 'float':
		return db_column + " = models.FloatField(blank=True, null=True)"
	elif python_type == 'str':
		return db_column + " = models.TextField(blank=True, null=True)"
	elif python_type == 'datetime':
		return db_column + " = models.DateTimeField(blank=True, null=True)"
	elif python_type == 'bool':
		return db_column + " = models.NullBooleanField(blank=True, null=True)"
	else:
		return "#UNKNOW TYPE "+ db_column + " = models.??????Field(blank=True, null=True)"

# Start point of the script
if __name__ == "__main__":
	
	# Get the arguments
	parser = argparse.ArgumentParser(description='Generate the model for a dataset.')
	parser.add_argument('--debug', '-d', default=False, action='store_true', help='Set the logging level to debug')
	parser.add_argument('filename', help='The path to a csv file as generated by the extract_keywords script')
	
	args = parser.parse_args()
	if args.debug:
		logging.basicConfig(level = logging.DEBUG, format='%(levelname)-8s: %(message)s')
	else:
		logging.basicConfig(level = logging.INFO, format='%(levelname)-8s: %(message)s')
	
	csv = pandas.read_csv(args.filename, skipinitialspace = True)
	
	print "class Metada(BaseMetada):"
	
	for index, row in csv.iterrows():
		logging.debug("filed definition for row %s", row)
		print "\t" + get_field(row['db_column'], row['python_type'])
	
	print "\t"
	print "\tclass Meta(BaseMetada.Meta):"
	print "\t\tpass"