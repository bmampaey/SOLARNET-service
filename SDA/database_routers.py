from SDA.settings import DATABASES

class DataSetRouteur(object):
	"""
	A router to control all database operations on models of the different data set applications.
	"""
	def db_for_read(self, model, **hints):
		"""
		Redirect each dataset read to it's database.
		"""
		#import pdb; pdb.set_trace() 
		if model._meta.app_label not in DATABASES:
			return 'default'
		return model._meta.app_label
	
	def db_for_write(self, model, **hints):
		"""
		Redirect each dataset write to it's database.
		"""
		#import pdb; pdb.set_trace()
		if model._meta.app_label not in DATABASES:
			return 'default'
		return model._meta.app_label
	
	def allow_relation(self, obj1, obj2, **hints):
		"""
		Allow relations only between same dataset.
		"""
		if obj1._meta.app_label not in DATABASES or obj2._meta.app_label not in DATABASES:
			return True
		else:
			return obj1._meta.app_label == obj2._meta.app_label
	
#	def allow_migrate(self, db, model):
#		"""
#		Make sure the dataset app only appears in the corresponding database.
#		"""
#		#import pdb; pdb.set_trace() 
#		if model._meta.app_label not in DATABASES:
#			return True
#		else:
#			return db == model._meta.app_label

