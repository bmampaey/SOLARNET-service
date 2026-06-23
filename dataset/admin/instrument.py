from dataset.models import Instrument
from project import admin


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
	"""Admin class for the Instrument model"""

	pass
