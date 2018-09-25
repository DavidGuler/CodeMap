"""
Define and implement the Builder class.
"""

from CodeViewer.core.base_elements.base_elements import BaseCodeElement, BaseCodeConnection
from CodeViewer.core.builder.consts import UnknownElementType, PackageIsNotFound, BuilderConsts
from pkgutil import walk_packages
import sys

class Builder(object):
	"""
	The Builder is the key class for crawling through a package
	and pour it into a data structure.

	The current data structure is tree.
	"""
	_CODE_ELEMENTS = {}
	_CODE_CONNECTIONS = {}

	def __init__(self):
		r"""
		Init the class.
		Sets all the code and connection elements defined at elements\*,
		and a cache attribute for the package structure.
		"""
		self._set_elements(Builder._CODE_ELEMENTS)
		self._set_elements(Builder._CODE_CONNECTIONS)
		self._cached_code_element = dict()

	def create_code_element(self, code_element_obj, root_code_element=None):
		"""
		create_code_element(code_element_obj, root_code_element=None) -> CodeElement

		Creates and returns a CodeElement from code_element_obj. If received a root_code_element,
		Creates a CodeConnection between them.

		:param	code_element_obj(any) 		   -> An object for creating a CodeElement.
		:param	root_code_element(CodeElement) -> A CodeElement object, presumably the parent.
		:return code_element(CodeElement)	   -> A new CodeElement created from code_element_obj.
		"""
		code_element = self._create_code_element(code_element_obj)

		# Create a connection between the new code_element and root_code_element.
		if root_code_element:
			code_connection = self._create_code_connection(root_code_element, code_element)
			root_code_element.code_connections.append(code_connection)
			
		return code_element

	def build(self, pkg_name, pkg_path=None):
		"""
		build(pkg_name, pkg_path=None) -> CodeElement

		
		"""
		self._test_pkg(pkg_name, pkg_path)
		if pkg_name not in self._cached_code_element.keys():
			code_element = self.create_code_element(pkg_name)
			self._cached_code_element[pkg_name] = self._build(code_element, True)
		return self._cached_code_element[pkg_name]

	@classmethod
	def register_element(cls, element_cls):
		if issubclass(element_cls, BaseCodeConnection):
			cls._CODE_CONNECTIONS[element_cls.__name__] = element_cls
		elif issubclass(element_cls, BaseCodeElement):
			cls._CODE_ELEMENTS[element_cls.__name__] = element_cls
		else:
			raise UnknownElementType(element_cls)

		return element_cls

	def _test_pkg(self, pkg_name, pkg_path=None):
		if pkg_path:
			sys.path.append(pkg_path)

		if not pkgutil.get_loader(pkg_name):
			raise PackageIsNotFound(pkg_name)

	def _set_elements(self, elements_dict):
		for element_name, element_cls in elements_dict.items():
			setattr(self, element_name, element_cls)

	def _create_code_element(self, code_element_obj):
		for element_cls in Builder._CODE_ELEMENTS.values():
			if element_cls.match(code_element_obj):
				return element_cls(code_element_obj)

	def _create_code_connection(self, root_code_element, code_element):
		for element_cls in Builder._CODE_CONNECTIONS.values():
			if element_cls.match(root_code_element, code_element):
				return element_cls(code_element)

	def _is_in_pkg(self, code_element):
		return self.pkg == code_element.name.split(".", 1)[0]

	def _get_build_pre_loop_values(self, is_pkg, code_element):
		if is_pkg:
			return pkgutil.walk_packages, (list(code_element.obj),)
		else:
			return dir, (code_element.path)

	def _get_build_in_loop_values(self, is_pkg, code_element, sub_code_element_data)
		if is_pkg:
			return ".".join([code_element.name, sub_code_element_data.name])
		else:
			if sub_code_element_data.startswith(BuilderConsts.SKIPPED_PREFIXES):
				return getattr(code_element, sub_code_element_data)

	def _get_build_loop_condition_values(self, is_pkg, sub_code_element)
		if is_pkg:
			return sub_code_element.is_pkg, True
		else:
			return is_pkg, self._is_in_pkg(sub_code_element)

	def _build(self, code_element, is_pkg):
		loop_method, loop_method_args = self._get_build_pre_loop_values(is_pkg, code_element)

		for sub_code_element_data in loop_method(*loop_method_args):
			sub_code_element_obj = self._get_build_in_loop_values(is_pkg, code_element, \
																  sub_code_element_data)
			sub_code_element = self.create_code_element(sub_code_element_obj, code_element)

			is_pkg, loop_condition = self._get_build_loop_condition_values(is_pkg, sub_code_element)

			if loop_condition:
				self._build(sub_code_element, is_pkg)

		return code_element