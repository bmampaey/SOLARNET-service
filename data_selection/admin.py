from django.contrib import admin

from data_selection.models import UserDataSelection, DataSelection

@admin.register(UserDataSelection)
class UserDataSelectionAdmin(admin.ModelAdmin):
	'''Admin class for the UserDataSelection model'''
	list_display = ["user", "name", "created"]
	list_filter = ["user__username"]


@admin.register(DataSelection)
class DataSelectionAdmin(admin.ModelAdmin):
	'''Admin class for the DataSelection model'''
	list_display = ["user_data_selection", "dataset", "created"]
	list_filter = ["dataset"]