import logging
from collections import OrderedDict

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login
from django.http import JsonResponse, QueryDict

from wizard.forms import Login, DataSelectionCreateForm
from wizard.models import UserDataSelection, DataSelection
from dataset.models import Dataset

# See https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-editing/#ajax-example
class AjaxableResponseMixin(object):
	"""
	Mixin to add AJAX support to a form.
	Must be used with an object-based FormView (e.g. CreateView)
	"""
	def form_invalid(self, form):
		response = super(AjaxableResponseMixin, self).form_invalid(form)
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):
		# We make sure to call the parent's form_valid() method because
		# it might do some processing (in the case of CreateView, it will
		# call form.save() for example).
		response = super(AjaxableResponseMixin, self).form_valid(form)
		if self.request.is_ajax():
			data = {
				'pk': self.object.pk,
			}
			return JsonResponse(data)
		else:
			return response

class Wizard(TemplateView):
	template_name = 'wizard/index.html'
	
	def get_context_data(self, **kwargs):
		context = super(Wizard, self).get_context_data(**kwargs)
		return context

class LoginForm(FormView):
	template_name = 'wizard/login_form.html'
	form_class = Login
	#TODO replace by url resolver
	success_url = '/wizard/'
	
	def form_valid(self, form):
		username, password = form.cleaned_data["email"].split("@", 1)
		#import pdb; pdb.set_trace()
		user = authenticate(username=username, password=password)
		if user is None:
			# Register the user
			User.objects.create_user(username, email=form.cleaned_data["email"], password=password)
			user = authenticate(username=username, password=password)
		if user.is_active:
			user_login(self.request, user)
		
		return super(LoginForm, self).form_valid(form)


class DataSelectionCreate(AjaxableResponseMixin, CreateView):
	model = DataSelection
	form_class = DataSelectionCreateForm
	success_url = '/success/'
	success_message = "%(name)s was saved successfully"
	
	def get_form(self, form_class):
		data = self.request.GET or self.request.POST
		 #import pdb; pdb.set_trace()
		if data:
			data = data.copy()
			if "user_data_selection_name" not in data:
				dataset = Dataset.objects.get(id=data['dataset_id'])
				data["user_data_selection_name"] = dataset.name
			return form_class(data)
		else:
			return form_class()
	
	def get_context_data(self, **kwargs):
		context = super(DataSelectionCreate, self).get_context_data(**kwargs)
		context['previous_user_data_selection_names'] = UserDataSelection.objects.filter(user=self.request.user).values_list("name", flat=True)
		return context
	
	
	def form_valid(self, form):
		# TODO See if it is possible to put this in the form save method
		
		form.instance.user_data_selection = UserDataSelection.objects.get_or_create(user=self.request.user, name=form.cleaned_data["user_data_selection_name"])[0]
		form.instance.dataset = Dataset.objects.get(id=form.cleaned_data["dataset_id"])
		import pdb; pdb.set_trace()
		# If all is selected we exclude the data_ids 
		if form.cleaned_data["all_selected"]:
			# Make up the selection criteria from the cleaned data
			cleaned_data = form.instance.dataset.search_data_form.get_cleaned_data(QueryDict(form.cleaned_data["query_string"]))
			selection_criteria = form.instance.dataset.search_data_form.get_selection_criteria(cleaned_data)
			form.instance.data_ids = list(form.instance.dataset.meta_data_model.objects.order_by().filter(**selection_criteria).exclude(id__in=form.cleaned_data["selected_data_ids"]).values_list('id', flat=True).distinct())
		else:
			form.instance.data_ids = form.cleaned_data["selected_data_ids"]
		
		return super(DataSelectionCreate, self).form_valid(form)


class UserDataSelectionList(ListView):
	model = UserDataSelection
	table_columns = OrderedDict([('name', 'Name'), ('created', 'Date of creation'), ('updated', 'Last update')])
	paginate_by = None # We do not paginate
	context_object_name = 'user_data_selection_list'
	ordering = 'requested'
	template_name = 'wizard/user_data_selection_list.html'
	
	def get_queryset(self):
		# Return the data selection for the user
		return self.model.objects.filter(user=self.request.user)
	
	def get_context_data(self, **kwargs):
		context = super(UserDataSelectionList, self).get_context_data(**kwargs)
		context['table_columns'] = self.table_columns
		return context

class UserDataSelectionDetail(DetailView):
	model = UserDataSelection
	context_object_name = 'user_data_selection'
	template_name = 'wizard/user_data_selection.html'

class DataSelectionDetail(DetailView):
	model = DataSelection
	context_object_name = 'data_selection'
	template_name = 'wizard/data_selection.html'

def download_user_data_selection(request, download_user_data_selection_id):
	# Placeholder for zip file download
	pass
