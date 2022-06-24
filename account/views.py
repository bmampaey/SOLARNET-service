from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

__all__ = ['LoginView',' LogoutView',' PasswordChangeView',' PasswordChangeDoneView',' PasswordResetView',' PasswordResetDoneView',' PasswordResetConfirmView', 'PasswordResetCompleteView', 'AccountUpdateView', 'AccountDeleteView']

extra_context = {
	'site_url' : '/',
	'site_header' : 'SOLARNET Virtual Observatory',
	'site_title' : 'SVO',
	'has_permission': True,
	'is_popup': False,
	'is_nav_sidebar_enabled': False,
}

class LoginView(auth_views.LoginView):
	extra_context = extra_context
	template_name = 'account/login.html'
	
	def get_success_url(self):
		url = self.get_redirect_url()
		return url or reverse_lazy('account:account_update')


class LogoutView(auth_views.LogoutView):
	extra_context = extra_context
	next_page = reverse_lazy('account:login')

class PasswordChangeView(auth_views.PasswordChangeView):
	extra_context = extra_context
	template_name = 'account/password_change.html'
	success_url = reverse_lazy('account:password_change_done')

class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
	extra_context = extra_context
	template_name = 'account/password_change_done.html'

class PasswordResetView(auth_views.PasswordResetView):
	extra_context = extra_context
	template_name = 'account/password_reset.html'
	email_template_name = 'account/password_reset_email.html'
	success_url = reverse_lazy('account:password_reset_done')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
	extra_context = extra_context
	template_name = 'account/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
	extra_context = extra_context
	template_name = 'account/password_reset_confirm.html'
	success_url = reverse_lazy('account:password_reset_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
	extra_context = extra_context
	template_name = 'account/password_reset_complete.html'
	success_url = reverse_lazy('account:password_reset_complete')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['login_url'] = reverse_lazy('account:login')
		return context

class AccountUpdateView(LoginRequiredMixin, UpdateView):
	extra_context = {**extra_context, 'title': 'Account' }
	template_name = 'account/account_update.html'
	login_url = reverse_lazy('account:login')
	fields = ['first_name', 'last_name']
	success_url = reverse_lazy('account:account_update')
	
	def get_object(self, queryset=None):
		return self.request.user

class AccountDeleteView(LoginRequiredMixin, DeleteView):
	extra_context = {**extra_context, 'title': 'Account' }
	template_name = 'account/account_delete.html'
	login_url = reverse_lazy('account:login')
	success_url = '/'
	
	def get_object(self, queryset=None):
		return self.request.user
