import json

from django.db import connection

from tastypie.paginator import Paginator

class EstimatedCountPaginator(Paginator):

	def __init__(self, *args, **kwargs):
		max_estimate = kwargs.pop("max_estimate", 1000)
		super(EstimatedCountPaginator, self).__init__(*args, **kwargs)
		self.max_estimate = max_estimate
		self._count = self._estimated = None

	def get_next(self, limit, offset, count):
		# The parent method needs an int which is higher than "limit + offset"
		# to return a url. Setting it to an unreasonably large value, so that
		# the parent method will always return the url.
		if self._estimated:
			count = 2 ** 64
		return super(EstimatedCountPaginator, self).get_next(limit, offset, count)

	def get_count(self):
		"""Return an estimate of the total number of objects if the estimate is greater than 1000"""
		if self._count is None:
			estimate = self.get_estimated_count()
			if estimate < self.max_estimate:
				self._count = super(EstimatedCountPaginator, self).get_count()
				self._estimated = False
			else:
				self._count = estimate
				self._estimated = True
		
		return self._count

	def get_estimated_count(self):
		"""Get the estimated count by using the database query planner."""
		# If you do not have PostgreSQL as your DB backend, alter this method
		# accordingly.
		return self._get_postgres_estimated_count()

	def _get_postgres_estimated_count(self):

		# This method only works with postgres >= 9.0.
		# If you need postgres vesrions less than 9.0, remove "(format json)"
		# below and parse the text explain output.

		def _get_postgres_version():
			# Due to django connections being lazy, we need a cursor to make
			# sure the connection.connection attribute is not None.
			connection.cursor()
			return connection.connection.server_version
		
		try:
			if _get_postgres_version() < 90000:
				print "Postgres version too low for the EstimatedCountPaginator:",  _get_postgres_version()
				return
		except AttributeError:
			return
		
		cursor = connection.cursor()
		query = self.objects.all().query
		
		# Remove limit and offset from the query, and extract sql and params.
		query.low_mark = None
		query.high_mark = None
		query, params = self.objects.query.sql_with_params()
		
		# Fetch the estimated rowcount from EXPLAIN json output.
		query = 'explain (format json) %s' % query
		print query
		cursor.execute(query, params)
		explain = cursor.fetchone()[0]
		# Older psycopg2 versions do not convert json automatically.
		if isinstance(explain, basestring):
			explain = json.loads(explain)
		rows = explain[0]['Plan']['Plan Rows']
		return rows
		
	def page(self):
		data = super(EstimatedCountPaginator, self).page()
		data['meta']['estimated_count'] = self._estimated
		return data
