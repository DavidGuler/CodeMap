"""
~
Name: base_element
Purpose: Defines the ABC BaseElement.
Author: DavidGuler (davidguler.1x@gmail.com)
~
"""
import abc

class BaseElement(object, metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def view(self, master):
		return False

	@classmethod
	def match(cls, *args, **kwargs):
		return cls._match(*args, **kwargs)