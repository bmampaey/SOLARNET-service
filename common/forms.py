# -*- coding: utf-8 -*-
from django import forms

class BaseForm(forms.Form):
	"""Base form to set common methods and parameters to all forms"""
	
	@classmethod
	def initials(cls):
		"""Return a dictionnary of the initial values"""
		data = dict()
		for name, field in cls.base_fields.iteritems():
			data[name] = field.initial
		return data
	
	
	@classmethod
	def get_cleaned_data(cls, request_data):
		""" Clean up the request data and return a dictionnary of clean values """
		# Parse the request data
		form = cls(request_data)
		if not form.is_valid():
			raise Exception(str(form.errors))
		
		# For each parameter we try to get the values from the form or else from the initials value
		cleaned_data = cls.initials()
		cleaned_data.update(form.cleaned_data)
		
		return cleaned_data