from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from wizard import views

urlpatterns = patterns('',
	url(r'^$', views.Wizard.as_view(), name='index'),
	url(r'user_data_selection_create/$', login_required(views.UserDataSelectionCreate.as_view()), name='user_data_selection_create'),
	url(r'data_selection_create/$', login_required(views.DataSelectionCreate.as_view()), name='data_selection_create'),
	url(r'user_data_selection_list/$', login_required(views.UserDataSelectionList.as_view()), name='user_data_selection_list'),

#	url(r'export_data/(?P<pk>[0-9]+)/$', views.ExportDataRequestUpdate.as_view(), name='export_data_update'),
#	url(r'export_data/(?P<pk>[0-9]+)/delete/$', views.ExportDataRequestDelete.as_view(), name='export_data_delete'),
	url(r'login$', views.LoginForm.as_view(), name='login_form'),
	url(r'logout', 'django.contrib.auth.views.logout', name='logout'),
)
