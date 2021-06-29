from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from django.forms.models import model_to_dict


from .utils import create_test_dataset


class TestAdminMixin:
	'''A mixin of useful methods for testing the admin site'''
	
	# Load the dataset manager group with the permissions to edit DataLocation, Dataset, Keyword, Tag
	fixtures = ['dataset_manager_group.json']
	
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.dataset_manager_group = Group.objects.get(name = 'dataset manager')
		cls.index_url = reverse('admin:index')
	
	def setUp(self):
		super().setUp()
		# Create a test dataset for the metadata model BaseMetadataTest
		# and give the permissions to it's user_group to edit BaseMetadataTest
		# and add a test user that belong to that group and to the dataset manager group
		# This is the typical configuration for a dataset manager
		self.test_dataset = create_test_dataset(characteristic_names = ['test1', 'test2'])
		self.test_dataset.user_group.permissions.add(
			Permission.objects.get(codename='view_basemetadatatest'),
			Permission.objects.get(codename='add_basemetadatatest'),
			Permission.objects.get(codename='change_basemetadatatest'),
			Permission.objects.get(codename='delete_basemetadatatest'),
		)
		self.test_user = User.objects.create_user(username='test_user', password='test', is_staff = True)
		self.test_user.groups.add(self.dataset_manager_group, self.test_dataset.user_group)
		
		# Create an other user that is a dataset manager but does not belong to any dataset user_group
		# to test visibility and edit permissions
		self.other_user = User.objects.create_user(username='other_user', password='test', is_staff = True)
		self.other_user.groups.add(self.dataset_manager_group)
		
		# Create an other dataset for which no user belong to it's user_group
		# to test visbility and edit permissions
		self.other_dataset = create_test_dataset(name = 'other dataset', user_group_name = 'other group', metadata_model = None)
		
		# Create a super user to test that he can do anything
		self.super_user = User.objects.create_user(username='super_user', password='test', is_staff = True, is_superuser = True)
	
	def get_list_url(self, model):
		'''Return the admin site URL for the list view of the model'''
		return reverse('admin:{meta.app_label}_{meta.model_name}_changelist'.format(meta=model._meta))
	
	def get_add_url(self, model):
		'''Return the admin site URL for the add view of the model'''
		return reverse('admin:{meta.app_label}_{meta.model_name}_add'.format(meta=model._meta))
	
	def get_change_url(self, instance):
		'''Return the admin site URL for the change view of the instance'''
		return reverse('admin:{meta.app_label}_{meta.model_name}_change'.format(meta=instance._meta), args=(instance.pk,))
	
	def get_delete_url(self, instance):
		'''Return the admin site URL for the delete view of the instance'''
		return reverse('admin:{meta.app_label}_{meta.model_name}_delete'.format(meta=instance._meta), args=(instance.pk,))
	
	def assertHttpOK(self, resp, msg = None):
		'''Ensures the response has an HTTP status code of 200'''
		return self.assertEqual(resp.status_code, 200, msg=msg)
	
	def assertHttpForbidden(self, resp, msg = None):
		'''Ensures the response has an HTTP status code of 403'''
		return self.assertEqual(resp.status_code, 403, msg=msg)
	
	def assertInHtmlResponse(self, response, *fragments, msg = None):
		'''Ensures the response is an HTML response that contains the fragments'''
		self.assertHttpOK(response, msg=msg)
		self.assertTrue(response['Content-Type'].startswith('text/html'), msg=msg)
		html = response.content.decode()
		for fragment in fragments:
			with self.subTest(fragment = fragment):
				self.assertIn(fragment, html, msg=msg)
	
	def assertNotInHtmlResponse(self, response, *fragments, msg = None):
		'''Ensures the response is an HTML response that does not contain the fragments'''
		self.assertHttpOK(response, msg=msg)
		self.assertTrue(response['Content-Type'].startswith('text/html'), msg=msg)
		html = response.content.decode()
		for fragment in fragments:
			with self.subTest(fragment = fragment):
				self.assertNotIn(fragment, html, msg=msg)
	
	def assertObjectUpdated(self, instance, *updated_attributes, msg = None):
		'''Ensures the instance attributes have been updated but not the others'''
		value_before = model_to_dict(instance)
		instance.refresh_from_db()
		value_after = model_to_dict(instance)
		
		for attribute in value_before.keys():
			with self.subTest(attribute = attribute):
				if attribute in updated_attributes:
					self.assertNotEqual(value_before[attribute], value_after[attribute], msg = msg)
				else:
					self.assertEqual(value_before[attribute], value_after[attribute], msg = msg)
