"""
~
Name: base_code_connection
Purpose: Defines the ABC subclass of BaseElement named BaseConnectionElement.
Author: DavidGuler (davidguler.1x@gmail.com)
~
"""

import abc
from CodeMap.core.base_elements.base_element import BaseElement

class BaseCodeConnection(BaseElement):
	def __init__(self, connected_code_element):
		self.connected_code_element = connected_code_element

	@classmethod
	@abc.abstractmethod
	def _match(cls, code_element_1, code_element_2):
		return False