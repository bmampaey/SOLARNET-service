from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group

from dataset.models import Dataset, Instrument, Telescope, Characteristic
from metadata.tests.models import BaseMetadataTest

__all__ = ['create_test_dataset', 'create_test_instrument']

def create_test_dataset(name = 'test dataset', description = 'test dataset description', contact_email = 'test_dataset_manager@test.com', archive_url = 'http://test-dataset.test.com/', metadata_model = BaseMetadataTest, instrument_name = 'test instrument', telescope_name = 'test telescope', user_group_name = 'test group', characteristic_names = []):
	'''Create a dataset for testing purpose'''
	if metadata_model is None:
		metadata_content_type = None
	else:
		metadata_content_type = ContentType.objects.get_for_model(metadata_model, for_concrete_model = False)
	
	telescope, trash = Telescope.objects.get_or_create(name = telescope_name)
	
	instrument, trash = Instrument.objects.get_or_create(name = instrument_name, defaults = {'telescope': telescope})
	
	user_group, trash = Group.objects.get_or_create(name = user_group_name)
	
	characteristics = [Characteristic.objects.get_or_create(name = name)[0] for name in characteristic_names]
	
	dataset = Dataset.objects.create(
		name = name,
		description = description,
		contact_email = contact_email,
		archive_url = archive_url,
		metadata_content_type = metadata_content_type,
		telescope = telescope,
		instrument = instrument,
		user_group = user_group,
	)
	
	dataset.characteristics.set(characteristics)
	
	return dataset

def create_test_instrument(instrument_name, telescope_name = 'test telescope'):
	'''Create an instrument for testing purpose'''
	
	telescope, trash = Telescope.objects.get_or_create(name = telescope_name)
	
	return Instrument.objects.create(name = instrument_name, telescope = telescope)
