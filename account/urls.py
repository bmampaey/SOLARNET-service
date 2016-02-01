from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login
from account.views import UserHistoryView
from account.forms import LoginForm

urlpatterns = [
	url(r'login$', login, {'template_name': 'account/login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'logout$',logout_then_login, name='logout'),
	url(r'user_history$', UserHistoryView.as_view(), name='user_history'),
]
