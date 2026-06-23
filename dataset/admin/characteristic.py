from dataset.models import Characteristic
from project import admin


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
	"""Admin class for the Characteristic model"""

	pass
