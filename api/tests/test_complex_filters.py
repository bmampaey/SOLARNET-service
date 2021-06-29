from django.test import SimpleTestCase
from django.db.models import Q
from tastypie.exceptions import InvalidFilterError

from api.complex_filters import get_complex_filter

class TestGetComplexFilter(SimpleTestCase):
	'''Test the get_complex_filter function'''
	
	def test_error(self):
		'''Test in case of errors'''
		msg = 'In case of an expression that does not conform, return an empty filter if ignore_bad_filters is True'
		self.assertEqual(get_complex_filter('cannot work', ignore_bad_filters = True), Q(), msg=msg)
		
		msg = 'In case of an expression that does not conform, raise a InvalidFilterError exception if ignore_bad_filters is False'
		with self.assertRaises(InvalidFilterError, msg=msg):
			get_complex_filter('cannot work', ignore_bad_filters = False)
	
	def test_empty(self):
		'''Test the empty string'''
		msg = 'An empty string must return an empty filter'
		self.assertEqual(get_complex_filter(''), Q(), msg=msg)
	
	def test_simple_expression(self):
		'''Test simple expressions'''
		
		msg = 'A simple exact lookup must return a simple exact Q filter'
		self.assertEqual(get_complex_filter('name=bob'), Q(name='bob'), msg=msg)
		
		msg = 'A simple lookup containing a digit is allowed'
		self.assertEqual(get_complex_filter('name2=bob'), Q(name2='bob'), msg=msg)
		
		msg = 'A simple contains lookup must return a simple contains Q filter'
		self.assertEqual(get_complex_filter('name__contains=bob'), Q(name__contains='bob'), msg=msg)
		
		msg = 'A simple gte lookup with a number must return a simple gte with a number Q filter'
		self.assertEqual(get_complex_filter('age__gte=18'), Q(age__gte='18'), msg=msg)
		
		msg = 'A simple in lookup must return a simple in with a list Q filter'
		self.assertEqual(get_complex_filter('name__in=bob,bobette'), Q(name__in=['bob','bobette']), msg=msg)
		
		msg = 'A simple range lookup must return a simple range with a list Q filter'
		self.assertEqual(get_complex_filter('age__range=18,65'), Q(age__range=['18', '65']), msg=msg)
		
		msg = 'A simple lookup for a value with quotes is allowed'
		self.assertEqual(get_complex_filter('name="bob mackenzie"'), Q(name='bob mackenzie'), msg=msg)
		
		msg = 'A simple isnull lookup with a "false" must return a simple isnull with False Q filter'
		self.assertEqual(get_complex_filter('name__isnull=false'), Q(name__isnull=False), msg=msg)
		
		msg = 'A simple isnull lookup with a "true" must return a simple isnull with True Q filter'
		self.assertEqual(get_complex_filter('name__isnull=true'), Q(name__isnull=True), msg=msg)
		
		msg = 'A simple exact lookup with a "none" must return a simple exact with None Q filter'
		self.assertEqual(get_complex_filter('name=none'), Q(name=None), msg=msg)
	
	def test_complex_expression(self):
		'''Test complex expressions'''
		
		msg = 'A simple expression with parenthesis must return a simple Q filter'
		self.assertEqual(get_complex_filter('(name=bob)'), Q(name='bob'), msg=msg)
		
		msg = 'A complex expression with 1 "or" must return a OR Q filter'
		self.assertEqual(get_complex_filter('name=bob or name=bobette'), Q(name='bob') | Q(name='bobette'), msg=msg)
		
		msg = 'A complex expression with 2 "or" must return a OR Q filter'
		self.assertEqual(get_complex_filter('name=bob or name=bobette or name=sidonie'), Q(name='bob') | Q(name='bobette') | Q(name='sidonie'), msg=msg)
		
		msg = 'A complex expression with 1 "and" must return a AND Q filter'
		self.assertEqual(get_complex_filter('age__gte=18 and age__lte=65'), Q(age__gte='18') & Q(age__lte='65'), msg=msg)
		
		msg = 'A complex negated expression must return a NOT Q filter'
		self.assertEqual(get_complex_filter('not name=bob'), ~Q(name='bob'), msg=msg)
		
		msg = 'In a complex expression, boolean operators take same precedence as in a Q filter'
		self.assertEqual(get_complex_filter('name=bob or age__gte=18 and age__lte=65'), Q(name='bob') | Q(age__gte='18') & Q(age__lte='65'), msg=msg)
		
		msg = 'In a complex expression, operators precedence can be forced using parenthesis'
		self.assertEqual(get_complex_filter('(name=bob or age__gte=18) and age__lte=65'), (Q(name='bob') | Q(age__gte='18')) & Q(age__lte='65'), msg=msg)
