"""
~
Name: base_code_element
Purpose: Defines the ABC subclass of BaseElement named BaseCodeElement.
Author: DavidGuler (davidguler.1x@gmail.com)
~
"""

import abc
from CodeMap.core.base_elements.base_element import BaseElement

class BaseCodeElement(BaseElement):
	def __init__(self, obj):
		self.code_connections = []
		self.obj = obj

	@property
	def type(self):
		return type(self.obj)

	@property
	def fullname(self):
		return ".".join([self.obj.__module__, self.obj.__name__])

	@property
	def name(self):
		return self.obj.__name__

	@classmethod
	@abc.abstractmethod
	def _match(cls, obj):
		return False