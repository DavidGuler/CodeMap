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

	def match(self, *args, **kwargs):
		return self._match(*args, **kwargs)