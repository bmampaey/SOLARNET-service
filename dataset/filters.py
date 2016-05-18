from pyparsing import infixNotation, opAssoc, Suppress, CharsNotIn, Word, alphanums, quotedString, removeQuotes, ZeroOrMore, Empty, ParseException
from django.db.models import Q

class Filter:
	def __init__(self, t):
		self.filter = {t[0]: t[1]}
	
	def __str__(self):
		return str(self.filter)
	
	def as_q(self):
		return Q(**self.filter)
	
	__repr__ = __str__

class BoolBinOp:
	def __init__(self, t):
		self.args = t[0][0::2]
	
	def __str__(self):
		sep = " %s " % self.reprsymbol
		return "(" + sep.join(map(str,self.args)) + ")"
	
	__repr__ = __str__

class AndOp(BoolBinOp):
	reprsymbol = 'AND'
	
	def as_q(self):
		return reduce(lambda a, b: a & b.as_q(), self.args, Q())

class OrOp(BoolBinOp):
	reprsymbol = 'OR'
	
	def as_q(self):
		return reduce(lambda a, b: a | b.as_q(), self.args, Q())

class NotOp:
	def __init__(self, t):
		self.arg = t[0][1]
	
	def __str__(self):
		return 'NOT ' + str(self.arg)
	
	def as_q(self):
		return ~self.arg.as_q()
	
	__repr__ = __str__

class EmptyFilter:
	def __init__(self):
		pass
	
	def __str__(self):
		return 'Empty'
	
	def as_q(self):
		return Q()
	
	__repr__ = __str__

BasicFilter = Word(alphanums, alphanums + '_') + Suppress('=') + (quotedString.setParseAction(removeQuotes) | ZeroOrMore(' ') + CharsNotIn('() '))
BasicFilter.setParseAction(Filter)

ComplexFilter = infixNotation(BasicFilter, [
	("not", 1, opAssoc.RIGHT, NotOp),
	("and", 2, opAssoc.LEFT, AndOp),
	("or",  2, opAssoc.LEFT, OrOp)
]) | Empty().setParseAction(EmptyFilter)

