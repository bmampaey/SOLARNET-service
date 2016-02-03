class Logger:
	'''Easy logging for command'''
	
	def __init__(self, command):
		self.stdout = command.stdout
		self.style = command.style
	
	def info(self, msg, *args):
		self.stdout.write(self.style.SUCCESS(msg % args))
	
	def warning(self, msg, *args):
		self.stdout.write(self.style.WARNING(msg % args))
	
	def error(self, msg, *args):
		self.stdout.write(self.style.ERROR(msg % args))
