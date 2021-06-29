from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from dataset.tests.utils import create_test_dataset
from metadata.tests.models import BaseMetadataTest

class TestBaseMetadataModel(TestCase):
	'''Test the Dataset model'''
	
	def test_metadata_model(self):
		'''Test the metadata_model method'''
		
		msg = 'When the metadata_content_type for a dataset is not set, the method raises a ValueError'
		test_dataset = create_test_dataset(metadata_model = None)
		with self.assertRaises(ValueError, msg=msg):
			test_dataset.metadata_model
		
		msg = 'When the metadata_content_type for a dataset is set to an existing model, the method returns the model'
		test_dataset.metadata_content_type = ContentType.objects.get_for_model(BaseMetadataTest)
		self.assertEqual(test_dataset.metadata_model, BaseMetadataTest, msg=msg)
