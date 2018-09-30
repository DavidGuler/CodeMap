from CodeMap.core.builder import Builder
from CodeMap.core.base_elements.base_code_connection import BaseCodeConnection
from CodeMap.elements.code_elements import *
from CodeMap.elements.consts import *
from CodeMap.core.consts import DELIM
import tkinter


@Builder.register_element
class CC_Inherited(BaseCodeConnection):
	pass


@Builder.register_element
class CC_Property(BaseCodeConnection):
	pass


@Builder.register_element
class CC_Namespaced(BaseCodeConnection):
	pass


@Builder.register_element
class CC_Packaged(BaseCodeConnection):

	@classmethod
	def _match(cls, code_element_1, code_element_2):
		if hasattr(code_element_1.obj, PACKAGE_ATTR) or \
		   hasattr(code_element_2.obj, PACKAGE_ATTR) or
			   	   code_element_1.obj is CE_Package:
			if code_element_2.obj.__package__ == code_element_1.name:
				return True
			elif code_element_2.obj.__name__ == code_element_2.obj.__package__:
				code_element_2_pkg = code_element_2.obj.__package__.rsplit(DELIM, 1)[0]
				if code_element_1.obj.__name__ == code_element_2_pkg:
					return True
		return False

	def view(self, master):
		pass


@Builder.register_element
class CC_Imported(BaseCodeConnection):
	
	@classmethod
	def _match(cls, code_element_1, code_element_2):
		if code_element_2.name.rsplit(DELIM, 1)[1] in dir(code_element_1.obj):
			if code_element_2.type is MODULE:
				return True
		return False

	def view(self, master):
		pass