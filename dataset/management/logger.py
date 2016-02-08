class Logger:
	'''Easy logging for command'''
	
	def __init__(self, command, debug = False):
		self.stdout = command.stdout
		self.style = command.style
		# If not debug we replace the debug method with a void method
		if not debug:
			self.debug = lambda *args: None
	
	def debug(self, msg, *args):
		self.stdout.write(self.style.NOTICE(msg % args))
	
	def info(self, msg, *args):
		self.stdout.write(self.style.SUCCESS(msg % args))
	
	def warning(self, msg, *args):
		self.stdout.write(self.style.WARNING(msg % args))
	
	def error(self, msg, *args):
		self.stdout.write(self.style.ERROR(msg % args))
