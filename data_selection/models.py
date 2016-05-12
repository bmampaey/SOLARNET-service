from __future__ import unicode_literals
import urlparse

from django.db import models
from django.http import QueryDict
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import DEFAULT_DB_ALIAS

from web_account.models import User
from dataset.models import Dataset

class UserDataSelection(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(help_text='Name of the data selection', max_length = 80, null=False, blank=False)
	created = models.DateTimeField(help_text = 'Date of creation', null=False, blank=False, auto_now_add=True)
	updated = models.DateTimeField(help_text = 'Date of last update', null=False, blank=False, auto_now=True)
	
	class Meta:
		ordering = ['-updated']
		get_latest_by = 'updated'
		unique_together = (('user', 'name'),)
		db_table = 'user_data_selection'
		
	def __unicode__(self):
		return u'%s by %s on %s' % (self.name, self.user.get_username(), self.created)
	
	@property
	def number_items(self):
		return sum(data_selection.number_items for data_selection in self.data_selections.all())

	
	@property
	def dataset_names(self):
		return self.data_selections.values_list('dataset', flat=True).distinct()
	
	@property
	def ftp_link(self):
		return urlparse.urljoin(settings.FTP_URL, 'data_selections/{self.user.email}/{self.name}/'.format(self = self))
	
	@property
	def metadata(self):
		metadata = dict()
		for data_selection in self.data_selections.filter(dataset=dataset):
			if data_selection.dataset in metadata:
				metadata[data_selection.dataset] = data_selection.metadata
			else:
				metadata[data_selection.dataset] |= data_selection.metadata
	
	@property
	def similar_metadata(self, for_dataset):
		similars = dict()
		for dataset, metadata in self.all_metadata.iteritems():
			if dataset == for_dataset:
				continue
			
		t1, t2 = dataset.metadata_model._meta.db_table, metadata.model._meta.db_table
		where_clause, params = metadata.query.get_compiler(DEFAULT_DB_ALIAS).compile(metadata.query.where)
		sql_string = 'SELECT "{t1}".* from "{t1}" JOIN "{t2}" ON "{t1}"."date_beg" <= "{t2}"."date_end" AND "{t1}"."date_end" >= "{t2}"."date_beg"'
		if where_clause:
			sql_string = (sql_string + 'WHERE {where_clause};').format(t1=t1, t2=t2, where_clause=where_clause)
		else:
			sql_string = (sql_string + ';').format(t1=t1, t2=t2)

class DataSelection(models.Model):
	user_data_selection = models.ForeignKey(UserDataSelection, related_name = 'data_selections', on_delete=models.CASCADE) # If the UserDataSelection is deleted, delete also the DataSelection
	dataset = models.ForeignKey(Dataset, related_name = 'datasets', related_query_name = 'dataset', on_delete=models.CASCADE)
	query_string = models.TextField(help_text='Query string for the data selection', max_length=2000, null=True, blank=True)
	metadata_oids = ArrayField(models.TextField('Observation ID', help_text = 'Unique identifier for the observation metadata, usually in the form YYYYMMDDHHMMSS'), help_text = 'List of metadata oids', null=True, blank=True)
	created = models.DateTimeField(help_text = 'Date of creation', null=False, blank=False, auto_now_add=True)
	number_items = models.IntegerField(help_text = 'Number of items in the data selection', null=True, blank=True)
	
	class Meta:
		db_table = 'data_selection'
		
	def __unicode__(self):
		return u'%s for %s' % (self.dataset, self.user_data_selection)
	
	def save(self, *args, **kwargs):
		self.number_items = self.metadata.count()
		super(DataSelection, self).save(*args, **kwargs)
	
	@property
	def metadata(self):
		if self.metadata_oids:
			return self.dataset.metadata_model.objects.filter(oid__in=self.metadata_oids)
		else:
			query_dict = QueryDict(self.query_string, mutable=True)
			# TODO this is probably wrong and should use the correct resource and use build_filters
			return self.dataset.metadata_model.objects.filter(**query_dict.dict())
	
	@property
	def ftp_link(self):
		return self.user_data_selection.ftp_link + '{self.dataset.name}/'.format(self = self)

