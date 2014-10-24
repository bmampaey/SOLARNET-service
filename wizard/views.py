import logging
from collections import OrderedDict

from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login
from django.http import HttpResponse

from wizard.forms import Login
from wizard.models import UserDataSelection, DataSelection


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
		import pdb; pdb.set_trace()
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


class UserDataSelectionCreate(CreateView):
	model = UserDataSelection
#	http_method_names = ['post']
#	fields = ["dataset_name", "query_string", "all_selected", "data_ids"]
#	success_url = '/success/'
	success_message = "%(name)s was saved successfully"

class DataSelectionCreate(CreateView):
	model = DataSelection
#	http_method_names = ['post']
	success_url = '/success/'
	success_message = "%(name)s was saved successfully"

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