# URLs for allowing to reset one's password on the admin login page
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .site import site

# Do not specify an app_name, the admin login view does not support it
# Site urls must come last because it has a "catch all" that would hide the password reset views
urlpatterns = [
	path('password_reset/', PasswordResetView.as_view(template_name = 'admin/password_reset.html', email_template_name = 'admin/password_reset_email.html'), name='admin_password_reset'),
	path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('password_reset/complete/', PasswordResetCompleteView.as_view(template_name = 'admin/password_reset_complete.html'), name='password_reset_complete'),
	path('', site.urls),
]
