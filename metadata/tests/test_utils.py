from django.test import TestCase
from django.db.models.query import QuerySet, EmptyQuerySet
from django.contrib.auth.models import User, Group

from metadata.utils import get_metadata_queryset
from dataset.tests.utils import create_test_dataset


class TestGetMetadataQueryset(TestCase):
	'''Test the get_metadata_queryset function'''
	
	def setUp(self):
		# Create test data
		self.test_user = User.objects.create_user(username='test@test.com', email='test@test.com', password='test', first_name='test', last_name='test')
		self.test_dataset = create_test_dataset()
		self.test_metadata1 = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata1')
		self.test_metadata2 = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata2')
	
	def test_resource_not_registered(self):
		'''Test that if the specified metadata_model does not have a registered resource, the return value is an EmptyQuerySet'''
		
		queryset = get_metadata_queryset(Group, query_string= '', user = self.test_user)
		self.assertIsInstance(queryset, EmptyQuerySet)
	
	def test_no_user(self):
		'''Test that if no user is specified, the return value is a valid QuerySet'''
		
		queryset = get_metadata_queryset(self.test_dataset.metadata_model, query_string= '')
		self.assertIsInstance(queryset, QuerySet)
		self.assertQuerysetEqual(queryset, [self.test_metadata1, self.test_metadata2], ordered=False)
	
	def test_no_query_string(self):
		'''Test that if no query_string is specified, the return value is the QuerySet of all metadata'''
		
		queryset = get_metadata_queryset(self.test_dataset.metadata_model, user = self.test_user)
		self.assertIsInstance(queryset, QuerySet)
		self.assertQuerysetEqual(queryset, self.test_dataset.metadata_model.objects.all(), ordered=False)
	
	def test_query_string(self):
		'''Test that if a query_string is specified, the return value is a valid QuerySet corresponding to the query string'''
		
		msg = 'When a query string with correct filters is specified, the return value is the QuerySet corresponding to the query string'
		queryset = get_metadata_queryset(self.test_dataset.metadata_model, query_string = 'oid=test_metadata1')
		self.assertIsInstance(queryset, QuerySet, msg=msg)
		self.assertQuerysetEqual(queryset, [self.test_metadata1], ordered=False)
		
		msg = 'When a query string with incorrect filters is specified, the return value is the QuerySet corresponding to the query string'
		queryset = get_metadata_queryset(self.test_dataset.metadata_model, query_string = 'oid=test_metadata1&characteristic__in=irrelevant')
		self.assertIsInstance(queryset, QuerySet, msg=msg)
		self.assertQuerysetEqual(queryset, [self.test_metadata1], ordered=False)
