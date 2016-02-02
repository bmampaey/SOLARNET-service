from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from account.models import UserProfile

class UserProfileInline(admin.StackedInline):
	model = UserProfile
	max_num = 1
	can_delete = False

# Unregister old user admin
admin.site.unregister(User)

# Register new user admin
@admin.register(User)
class UserAdmin(AuthUserAdmin):
	inlines = [UserProfileInline]
