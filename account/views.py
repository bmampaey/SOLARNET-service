from django.shortcuts import render
from django.views.generic.edit import FormView

from account.forms import LoginForm

class Login(FormView):
	'''Login view that authenticate and login user by email. If user does not exists, create it.'''
	template_name = 'wizard/login.html'
	form_class = LoginForm
	#TODO replace by url resolver
	success_url = '/'
	
	def form_valid(self, form):
		username, password = form.cleaned_data["email"].split("@", 1)
		
		user = authenticate(username=username, password=password)
		if user is None:
			# Register the user
			User.objects.create_user(username, email=form.cleaned_data["email"], password=password)
			user = authenticate(username=username, password=password)
		if user.is_active:
			user_login(self.request, user)
		
		return super(Login, self).form_valid(form)
