from CodeMap.core.builder import Builder
from CodeMap.core.base_elements.base_code_element import BaseCodeElement
from CodeMap.core.util import load_mod
import tkinter
import sys
import copy
import pkgutil
import importlib

######------ BaseCodeElement subs implementations ------######

@Builder.register_element
class CE_Package(BaseCodeElement):
	def __init__(self, pkg_name):
		super(CE_Package, self).__init__(importlib.util.find_spec(pkg_name).loader.load_module(pkg_name))

	@classmethod
	def _match(cls, obj):
		pkg_loader = pkgutil.get_loader(obj)
		return pkg_loader.is_package(pkg_loader.name)

	@property
	def fullname(self):
		return self.obj.__name__
	
	@property
	def name(self):
		return self.fullname.rsplit(DELIM, 1)[1]

	def view(self, master):
		#TODO: Implement
		pass


@Builder.register_element
class CE_Module(CE_Package):
	"""docstring for CE_Module"""

	@classmethod
	def _match(cls, obj):
		return not super(cls).match(obj)

	def view(obj):
		pass


@Builder.register_element
class CE_Class(BaseCodeElement):

	@classmethod
	def _match(cls, obj):
		if isinstance(obj, type):
			return True

	def view(self, master):
		#TODO: Implement
		pass


@Builder.register_element
class CE_Function(BaseCodeElement):
	"""docstring for CE_Function"""

	@classmethod
	def _identify(cls, obj, is_method):
		return obj.__class__ == "function" and ("." in obj.__qualname__) == is_method
		
	@classmethod
	def _match(cls, obj):
		return cls._identify(obj, False)

	def view(self, master):
		pass


@Builder.register_element
class CE_Method(CE_Function):
	
	@classmethod
	def _match(cls, obj):
		return super(cls)._match(obj, True)

	def view(self, master):
		pass


@Builder.register_element
class CE_Variable(BaseCodeElement):
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
	def _match(cls, obj):
		return True

	def view(self, master):
		pass