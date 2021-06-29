__all__ = ['Logger']

class Logger:
	'''
	Easy logging for command
	verbosity 0 means only error messages are displayed
	verbosity 1 means only error + warning messages are displayed
	verbosity 2 means only error + warning + info messages are displayed
	verbosity 3 and above means error + warning + info + debug messages are displayed
	'''
	
	def __init__(self, command, verbosity = 1):
		self.stdout = command.stderr
		self.style = command.style
		self.verbosity = verbosity
	
	def debug(self, msg, *args):
		if self.verbosity > 2:
			# The default coloring for stderr is ERROR, so override it to no color for debug
			self.stdout.write('[DEBUG] ' + msg % args, lambda x: x)
	
	def info(self, msg, *args):
		if self.verbosity > 1:
			self.stdout.write('[INFO] ' + msg % args, self.style.SUCCESS)
	
	def warning(self, msg, *args):
		if self.verbosity > 0:
			self.stdout.write('[WARNING] ' + msg % args, self.style.WARNING)
	
	def error(self, msg, *args):
		self.stdout.write('[ERROR] ' + msg % args, self.style.ERROR)
