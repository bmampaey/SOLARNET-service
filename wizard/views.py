import logging
from collections import OrderedDict

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login
from django.http import HttpResponse, JsonResponse


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
	success_url = '/welcome/'
	
	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		username, password = form.cleaned_data["email"].split("@", 1)
		#import pdb; pdb.set_trace()
		user = authenticate(username=username, password=password)
		if user is None:
			# Register the user
			User.objects.create_user(username, email=form.cleaned_data["email"], password=password)
			user = authenticate(username=username, password=password)
		if user.is_active:
			user_login(self.request, user)
			return HttpResponse(user.username)
		else:
			return HttpResponse("Your account is disabled. Please contact the website administrator", content_type="text/plain", status=401)

# NOT USEFUL
class UserDataSelectionCreate(CreateView):
	model = UserDataSelection
#	http_method_names = ['post']
#	fields = ["name"]
#	success_url = '/success/'
	success_message = "%(name)s was saved successfully"

class DataSelectionCreate(AjaxableResponseMixin, CreateView):
	model = DataSelection
	form_class = DataSelectionCreateForm
#	http_method_names = ['post']
	success_url = '/success/'
	success_message = "%(name)s was saved successfully"
	
	def get_form(self, form_class):
		if self.request.GET:
			return form_class(self.request.user, self.request.GET)
		else:
			return form_class(self.request.user)
	
	
	def form_valid(self, form):
		import pdb; pdb.set_trace()
		form.instance.user_data_selection = UserDataSelection.objects.get_or_create(user=self.request.user, name=form.cleaned_data["user_data_selection_name"])[0]
		form.instance.dataset = Dataset.objects.get(name=form.cleaned_data["dataset_name"])
		#If all is selected we exclude the data_ids 
# 			if self.all_selected:
# 				# Make up the selection criteria from the cleaned data
# 				cleaned_data = self.dataset.search_data_form.get_cleaned_data(QueryDict(self.query_string))
# 				selection_criteria = self.dataset.search_data_form.get_selection_criteria(cleaned_data)
# 				self.item_count = self.dataset.meta_data_model.objects.filter(**selection_criteria).exclude(id__in=self.data_ids).distict().count()

		return super(DataSelectionCreate, self).form_valid(form)


class UserDataSelectionList(ListView):
	model = UserDataSelection
	table_columns = OrderedDict([('name', 'Name'), ('requested', 'Date of creation')])
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
