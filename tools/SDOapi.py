import slumber
import dateutil.parser
from datetime import datetime

class Time:
	def __init__(self, *args, **kwargs):
		
		attrs = ["year", "month", "day", "hour", "minute", "second"]
		# First case, we get a string
		if len(args) == 1 and isinstance(args[0], basestring):
			time = Time.from_string(args[0])
			for attr in attrs:
				setattr(self, attr, getattr(time, attr)) 
		# Second case we get value for the fields indenpendently
		else:
			for attr, arg in zip(attrs, args):
				if arg is None:
					setattr(self, attr, None)
				elif isinstance(arg, int) or (attr == "second" and isinstance(arg, float)):
					setattr(self, attr, arg)
				else:
					raise TypeError("Wrong type of argument for attribute %s" % attr)
			
			for attr, arg in kwargs.iteritems():
				if hasattr(self, attr):
					raise ValueError("Duplicate value for attribute %s" % attr)
				elif arg is None:
					setattr(self, attr, None)
				elif isinstance(arg, int) or (attr == "second" and isinstance(arg, float)):
					setattr(self, attr, arg)
				else:
					raise TypeError("Wrong type of argument for attribute %s" % attr)
		
		# Set remaining attributes to None
		for attr in attrs:
			if not hasattr(self, attr):
				setattr(self, attr, None)
		
		# Make some verifications
		if self.year is not None and self.year <= 0:
			raise ValueError("Wrong value %s for attribute year" % self.year)
		if self.month is not None and not 1 <= self.month <= 12:
			raise ValueError("Wrong value %s for attribute month" % self.month)
		if self.day is not None and not 1 <= self.day <= 31:
			raise ValueError("Wrong value %s for attribute day" % self.day)
		if self.hour is not None and not 0 <= self.hour <= 23:
			raise ValueError("Wrong value %s for attribute hour" % self.hour)
		if self.minute is not None and not 0 <= self.minute <= 59:
			raise ValueError("Wrong value %s for attribute minute" % self.minute)
		if self.second is not None and not 0 <= self.second <= 59:
			raise ValueError("Wrong value %s for attribute second" % self.second)

	@classmethod
	def from_string(cls, time_string):
		# dateutil parser fills the unknow values from the default
		# We use this to know wich field was set
		one = dateutil.parser.parse(time_string, default = datetime(1,1,1,1,1,1,1))
		two = dateutil.parser.parse(time_string, default = datetime(2,2,2,2,2,2,2))
		time = cls()
		for attr in ["year", "month", "day", "hour", "minute", "second", "microsecond"]:
			if getattr(one, attr) == 1:
				if getattr(two, attr) == 2:
					# The attribute was not set
					setattr(time, attr, None)
				else:
					setattr(time, attr, 1)
			else:
				setattr(time, attr, getattr(two, attr)) 
		
		# Add microseconds to seconds
		if time.microsecond is not None:
			if time.second is None:
				time.second = time.microsecond/1000000.0
			else:
				time.second += time.microsecond/1000000.0
			time.microsecond = None
		
		return time
	
	def __str__(self):
		
		return ", ".join(["%s: %s" % (attr,  getattr(self, attr)) for attr in ["year", "month", "day", "hour", "minute", "second"]])
	
	def __repr__(self):
		
		return "Time(%s)" % str(self)


class DataSet:
	def __init__(dataset, dataset_name = ""):
		self.dataset = dataset
		self.dataset_name = dataset_name
		self._keywords = None
	
	@static
	def string_filter(keyword, range):
		filters = dict()
		if not isinstance(range, (tuple, list)):
			filters[keyword+"__iexact"] = range
		elif len(range) == 1:
			filters[keyword+"__icontains"] = range[0]
		elif len(range) == 2:
			if range[0] is not None:
				filters[keyword+"__istartswith"] = range[0]  
			if range[1] is not None:
				filters[keyword+"__iendswith"] = range[1]
		elif len(range) == 3:
			if range[0] is not None:
				filters[keyword+"__istartswith"] = range[0]
			if range[1] is not None:
				filters[keyword+"__icontains"] = range[1]
			if range[2] is not None:
				filters[keyword+"__iendswith"] = range[2]
		else:
			raise Exception("Bad range type or size for keyword %s: %s", (keyword, range))
	
	@static
	def numeric_filter(keyword, range):
		filters = dict()
		if not isinstance(range, (tuple, list)):
			filters[keyword+"__exact"] = range
		elif len(range) == 1:
			filters[keyword+"__exact"] = range[0]
		elif len(range) == 2:
			if range[0] is not None:
				filters[keyword+"__gte"] = range[0]  
			if range[1] is not None:
				filters[keyword+"__lt"] = range[1]
		else:
			raise Exception("Bad range type or size for keyword %s: %s", (keyword, range))

	@static
	def time_filter(keyword, range):
		filters = dict()
		if not isinstance(range, (tuple, list)):
			if isinstance(range, date):
				filters[keyword+"__gte"] = range  
				filters[keyword+"__lt"] = range + timedelta(days=1)
			filters[keyword+"__exact"] = range
		elif len(range) == 1:
			filters[keyword+"__exact"] = range[0]
		elif len(range) == 2:
			if range[0] is not None:
				filters[keyword+"__gte"] = range[0]  
			if range[1] is not None:
				filters[keyword+"__lt"] = range[1]
		else:
			raise Exception("Bad range type or size for keyword %s: %s", (keyword, range))

	def filter(self, **kwargs):
		for keyword, range in kwargs.iteritems():
			filters = dict()
			if keyword not in self.seywords:
				raise Exception("Unknown keyword %s for dataset %s" % (keyword, self.dataset_name))
			if self.keywords[keyword] type is string:
				filters.update(Dataset.string_filter(keyword, range))
			else:
				filters.update(Dataset.numeric_filter(keyword, range))
		
		return self.dataset.get(**filters)
						
	def get(self, recnum)
  
	@property
	def keywords(self)
		if self._keywords is None:
			
		return self._keywords


class SDO:
	def __init__(url = "http://db1.sdodb.oma.be/DRMS/api/v1/", auth = None):
		self.api = slumber.API(url, auth=auth)
	
	def all(self):
		return self.api.data_series.get()
	
	def filter(self, **kwargs):
		return
		
	def get(dataset_name)
		return DataSet(self.api



datasets = SDA.datasets(start_date = None, end_date = None, euv = true)
datasets[“aia.lev1”].keywords()
datasets[“aia.lev1”].filter(date_obs="2014-05-01"
