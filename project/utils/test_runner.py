import sys
import traceback

from django.test.runner import DiscoverRunner
from HtmlTestRunner import HTMLTestRunner, result


class MyHtmlTestResult(result.HtmlTestResult):
	def _exc_info_to_string(self, err, test):
		"""Converts a sys.exc_info()-style tuple of values into a string."""
		# if six.PY3:
		#     # It works fine in python 3
		#     try:
		#         return super(_HTMLTestResult, self)._exc_info_to_string(
		#             err, test)
		#     except AttributeError:
		#         # We keep going using the legacy python <= 2 way
		#         pass

		# This comes directly from python2 unittest
		exctype, value, tb = err
		# Skip test runner traceback levels
		while tb and self._is_relevant_tb_level(tb):
			tb = tb.tb_next

		if exctype is test.failureException:
			# Skip assert*() traceback levels
			msg_lines = traceback.format_exception(exctype, value, tb)
		else:
			msg_lines = traceback.format_exception(exctype, value, tb)

		if self.buffer:
			# Only try to get sys.stderr as it might not be
			# StringIO yet, e.g. when test fails during __call__
			try:
				error = sys.stderr.getvalue()
			except AttributeError:
				error = None
			if error:
				if not error.endswith('\n'):
					error += '\n'
				msg_lines.append(error)
		# This is the extra magic to make sure all lines are str
		encoding = getattr(sys.stdout, 'encoding', 'utf-8')
		lines = []
		for line in msg_lines:
			if not isinstance(line, str):
				# utf8 shouldn't be hard-coded, but not sure f
				line = line.encode(encoding)
			lines.append(line)

		return ''.join(lines)


class MyHTMLTestRunner(HTMLTestRunner):
	def __init__(self, **kwargs):
		# Pass any required options to HTMLTestRunner
		resultclass = kwargs.pop('resultclass', None) or MyHtmlTestResult
		super().__init__(
			output='./test_reports/',
			combine_reports=True,
			report_name='code_test',
			add_timestamp=False,
			resultclass=resultclass,
			**kwargs,
		)


class HtmlTestReporter(DiscoverRunner):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Patch over the test_runner in the super class.
		html_test_runner = MyHTMLTestRunner
		self.test_runner = html_test_runner
