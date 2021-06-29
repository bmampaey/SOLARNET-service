from django.test import TransactionTestCase
from django.db import connection


from metadata.models import Tag
from dataset.tests.utils import create_test_dataset

# Use a TransactionTestCase instead of a TestCase to allow vacuuming the table between tests
class TestBaseMetadataModel(TransactionTestCase):
	'''Test the BaseMetadata model'''
	
	def setUp(self):
		# Create test data
		self.test_dataset = create_test_dataset()
		self.test_tag1 = Tag.objects.create(name = 'test tag1')
		self.test_tag2 = Tag.objects.create(name = 'test tag2')
		self.test_tag3 = Tag.objects.create(name = 'test tag3')
	
	def vacuum_table(self):
		'''Run a full vacuum on the table to make the estimated_count more precise, requires to use a TransactionTestCase'''
		
		with connection.cursor() as cursor:
			cursor.execute('VACUUM FULL ANALYZE %s' % self.test_dataset.metadata_model._meta.db_table)
	
	def test_tags_names_property(self):
		'''Test the tags_names property of the model'''
		
		msg = 'When a metadata instance has no tag associated, the tags_names property must return an empty queryset'
		test_metadata0 = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata0')
		self.assertCountEqual(test_metadata0.tags_names, [], msg=msg)
		
		msg = 'When a metadata instance has 1 tag associated, the tags_names property must return the queryset with that tag only'
		test_metadata1 = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata1')
		test_metadata1.tags.add(self.test_tag1)
		self.assertCountEqual(test_metadata1.tags_names, [self.test_tag1.name], msg=msg)
		
		msg = 'When a metadata instance has 2 or more tags associated, the tags_names property must return the queryset with the related tags'
		test_metadata2 = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata2')
		test_metadata2.tags.add(self.test_tag1, self.test_tag2)
		self.assertCountEqual(test_metadata2.tags_names, [self.test_tag1.name, self.test_tag2.name], msg=msg)
	
	def test_estimated_count(self):
		'''Test the estimated_count of the queryset of the model'''
		
		msg = 'When a metadata model has no instance, the estimated_count for the whole model must be 0'
		self.assertEqual(self.test_dataset.metadata_model.objects.estimated_count(), 0, msg=msg)
		
		msg = 'When a metadata model has 1 instance, the estimated_count for the whole model must be 1'
		test_metadata = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata')
		self.vacuum_table()
		self.assertEqual(self.test_dataset.metadata_model.objects.estimated_count(), 1, msg=msg)
		
		msg = 'When a metadata model has more than 1000 instances, the estimated_count for the whole model must be arger than 1000'
		for i in range(1000): self.test_dataset.metadata_model.objects.create(oid = 'test_metadata%s' % i)
		self.vacuum_table()
		self.assertGreaterEqual(self.test_dataset.metadata_model.objects.estimated_count(), 1001, msg=msg)
		
		msg = 'When a metadata model is filtered on the oid, and the number of returned instance is larger than 1000, the estimated_count must be larger than 1000'
		queryset = self.test_dataset.metadata_model.objects.filter(oid__isnull=False)
		self.assertGreaterEqual(queryset.count(), 1000, msg=msg)
		self.assertGreaterEqual(queryset.estimated_count(), 1000, msg=msg)
		
		msg = 'When a metadata model is filtered on the oid, and the number of returned instance is smaller than 1000, the estimated_count must be equal to the count'
		queryset = self.test_dataset.metadata_model.objects.filter(oid__endswith='11')
		self.assertLess(queryset.count(), 1000, msg=msg)
		self.assertEqual(queryset.estimated_count(), queryset.count(), msg=msg)
		
		self.test_tag1.tests_basemetadatatest.add(*self.test_dataset.metadata_model.objects.all())
		self.test_tag2.tests_basemetadatatest.add(test_metadata)
		
		msg = 'When a metadata model is filtered on the tags, and the number of returned instance is larger than 1000, the estimated_count must be larger than 1000'
		queryset = self.test_dataset.metadata_model.objects.filter(tags__in=[self.test_tag1])
		self.assertGreaterEqual(queryset.count(), 1000, msg=msg)
		self.assertGreaterEqual(queryset.estimated_count(), 1000, msg=msg)
		
		msg = 'When a metadata model is filtered on the tags, and the number of returned instance is smaller than 1000, the estimated_count must be equal to the count'
		queryset = self.test_dataset.metadata_model.objects.filter(tags__in=[self.test_tag2])
		self.assertLess(queryset.count(), 1000, msg=msg)
		self.assertEqual(queryset.estimated_count(), queryset.count(), msg=msg)
