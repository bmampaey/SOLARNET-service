from django.db import models
from django.contrib.auth.models import User
from djorm_pgarray.fields import BigIntegerArrayField
from dataset.models import Dataset

class UserDataSelection(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	name = models.CharField(help_text="Name of the request", max_length = 80, null=False, blank=False)
	requested = models.DateTimeField(help_text = "Date of request.", null=False, blank=False, auto_now_add=True)
	
	class Meta:
		ordering = ["requested"]
		get_latest_by = "requested"
		unique_together = (("user", "name"),)
		db_table = "user_data_selection"
		
	def __unicode__(self):
		return u"%s by %s on %s" % (self.name, self.user.username, self.requested)
	
	@property
	def number_items(self):
		return sum(data_selection.number_items for data_selection in self.data_selections.all())
	
	@property
	def dataset_names(self):
		return self.data_selections.values_list("dataset__name", flat=True).distinct()
	

class DataSelection(models.Model):
	user_data_selection = models.ForeignKey(UserDataSelection, related_name = "data_selections", on_delete=models.CASCADE) # If the UserDataSelection is deleted, delete also the DataSelection
	#TODO change to dataset
	dataset = models.ForeignKey(Dataset, help_text="The dataset for the selection", db_column="dataset_name", related_name = "data_selections", on_delete=models.DO_NOTHING) # If the DataSet is deleted, don't delete the data selections
	query_string = models.TextField(help_text="Query string for the data selection", max_length=2000, null=True, blank=True)
	all_selected = models.BooleanField(help_text="Wheter all data was selected", null=False, blank=False, default=False)
	data_ids = BigIntegerArrayField(help_text = "List of data ids to include or exclude (if all_selected is true)")
	item_count = models.IntegerField(help_text="Number of items in the selection", null=True, blank=True)

	class Meta:
		db_table = "data_selection"
		
	def __unicode__(self):
		return u"%s for %s" % (self.dataset_name, self.user_data_selection)
	
	@property
	def number_items(self):
		if self.item_count is None:
		
			# If all is selected we exclude the data_ids 
			if self.all_selected:
				# Make up the selection criteria from the cleaned data
				cleaned_data = self.dataset.search_data_form.get_cleaned_data(QueryDict(self.query_string))
				selection_criteria = self.dataset.search_data_form.get_selection_criteria(cleaned_data)
				self.item_count = self.dataset.meta_data_model.objects.filter(**selection_criteria).exclude(id__in=self.data_ids).distict().count()
	
			else:
				self.item_count = len(self.data_ids)
			
			self.save()
		
		return self.item_count
