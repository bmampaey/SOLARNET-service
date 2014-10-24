from django.db import models
from django.contrib.auth.models import User
from djorm_pgarray.fields import BigIntegerArrayField

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
		return sum(data_selection.number_items for data_selection in seld.data_selections.all())

class DataSelection(models.Model):
	user_data_selection = models.ForeignKey(UserDataSelection, related_name = "data_selections", on_delete=models.CASCADE) # If the UserDataSelection is deleted, delete also the DataSelection
	dataset_name = models.CharField(help_text="Name of the dataset for the selection", max_length=20, null=False, blank=False)
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
		if self.item_count is not None:
			return self.item_count
		else:
			# TODO
			return None
	
