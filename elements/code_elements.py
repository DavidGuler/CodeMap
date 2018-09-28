from CodeViewer.core.builder.builder import Builder
from CodeViewer.core.base_elements.base_elements import BaseCodeElement
from CodeViewer.core.util import load_module
import tkinter
import sys
import copy

######------ BaseCodeElement subs implementations ------######

@Builder.register_element
class CE_Package(BaseCodeElement):
	def __init__(self, pkg_name):
		super(CE_Class, self).__init__(self, load_module(pkg_name))

	@staticmethod
	def match(obj):
		pkg_loader = pkgutil.get_loader(pkg_name)
		return pkg_loader.is_package(pkg_loader.name)

	def view(self, master):
		#TODO: Implement
		pass


@Builder.register_element
class CE_Module(CE_Package):
	"""docstring for CE_Module"""

	@staticmethod
	def match(obj):
		return not super().match(obj)

	def view(obj):
		pass


@Builder.register_element
class CE_Class(BaseCodeElement):

	@staticmethod
	def match(obj):
		if isinstance(obj, type):
			return True

	def view(self, master):
		#TODO: Implement
		pass


@Builder.register_element
class CE_Function(object):
	"""docstring for CE_Function"""

	@classmethod
	def _match(cls, obj, is_method):
		return obj.__class__ == "function" and ("." in obj.__qualname__) == is_method
		
	@staticmethod
	def match(obj):
		return CE_Function._match(obj, False)

	def view(self, master):
		pass


@Builder.register_element
class CE_Method(CE_Function):
	
	@staticmethod
	def match(obj):
		return super()._match(obj, True)

	def view(self, master):
		pass


@Builder.register_element
class CE_Variable(object):
	def __init__(self, value):
		self._name = self._get_var_name(value)
		super(CE_Variable, self).__init__(value)

	def _get_var_name(self, value):
		copied_f_locals = copy.deepcopy(sys._getframe(2).f_locals)
		for var_name in copied_f_locals.keys():
			if copied_f_locals[var_name] == value:
				return var_name
		raise

	@property
	def name(self):
		return self._name
	
	@staticmethod
	def match(obj):
		pass

	def view(self, master):
		pass