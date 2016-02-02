from django.conf.urls import url
from django.contrib.auth import views
from account.forms import LoginForm

urlpatterns = [
	url(r'login$', views.login, {'template_name': 'account/login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'logout$',views.logout_then_login, name='logout'),
]
