from dataset.models import Telescope
from project import admin


@admin.register(Telescope)
class TelescopeAdmin(admin.ModelAdmin):
	"""Admin class for the Telescope model"""

	pass
