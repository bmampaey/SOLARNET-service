from django.test import TransactionTestCase

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
