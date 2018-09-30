"""
~
Name: builder
Purpose: Define and implement the Builder class.
Author: DavidGuler (davidguler.1x@gmail.com)
~
"""

from CodeMap.core.base_elements.base_code_element import BaseCodeElement
from CodeMap.core.base_elements.base_code_connection import BaseCodeConnection
from CodeMap.core.consts import UnknownElementType, PackageIsNotFound, \
										   UnindetifiedElement, BuilderConsts
import pkgutil
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
		self._cache = dict()
		self._is_pkg = True

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
			self._create_code_connection(root_code_element, code_element)
			
		return code_element

	def build(self, pkg_name, pkg_path=None):
		"""
		build(pkg_name, pkg_path=None) -> CodeElement

		The main logic of processing the package into a CodeElement tree.

		:param	pkg_name(str) -> The name of package to import.
		:param	pkg_path(str) -> Optional. A path to add to sys.path in order
								 to import the package.
		:return CodeElement -> Return the code structure of the package requested.
		"""

		# Test if the package exists.
		self._test_pkg(pkg_name, pkg_path)

		# Returns the processed code structure of the package.
		return self._cache.setdefault(pkg_name, self._build(self.create_code_element(pkg_name)))

	@classmethod
	def register_element(cls, element_cls):
		"""
		register_element(cls, element_cls) -> type

		A decorator for registering elements to the Builder class.
		necessary for identifying code elements found in a package.

		:param	element_cls(type) -> The element class decorated.
		:return element_cls(type)
		"""

		# Add the class found to the registry if it is a valid one.
		if issubclass(element_cls, BaseCodeConnection):
			cls._CODE_CONNECTIONS[element_cls.__name__] = element_cls
		elif issubclass(element_cls, BaseCodeElement):
			cls._CODE_ELEMENTS[element_cls.__name__] = element_cls
		else:
			raise UnknownElementType(element_cls)

		return element_cls

	def _test_pkg(self, pkg_name, pkg_path=None):
		"""
		_test_pkg(self, pkg_name, pkg_path=None)

		Tests if the package received exists. If received
		a path, adds it to sys.path and then tests the package.

		:param	pkg_name(str) -> The name of package to import.
		:param	pkg_path(str) -> Optional. A path to add to sys.path in order
								 to import the package.
		"""

		# Adds the package's path to sys.path.
		if pkg_path:
			sys.path.append(pkg_path)

		# Test if the package exists.
		if not pkgutil.get_loader(pkg_name):
			raise PackageIsNotFound(pkg_name)

	def _set_elements(self, elements_dict):
		"""
		_set_elements(self, elements_dict)

		Sets the elements received as instance attributes.

		:param	elements_dict(Dict) -> The elements to set as attriburtes.
		"""
		for element_name, element_cls in elements_dict.items():
			setattr(self, element_name, element_cls)

	def _create_code_element(self, code_element_obj):
		"""
		_create_code_element(self, code_element_obj) -> CodeElement

		Creates a code element from a matching CodeElement subclass.

		:param	code_element_obj(CodeElement) -> The object to process.
		:return CodeElement
		"""
		for element_cls in Builder._CODE_ELEMENTS.values():
			if code_element_obj and element_cls.match(code_element_obj):
				return element_cls(code_element_obj)
		raise UnindetifiedElement(code_element_obj, CodeElement)

	def _create_code_connection(self, root_code_element, code_element):
		"""
		_create_code_connection(self, root_code_element, code_element) -> CodeConnection

		Creates a code connection from a matching CodeConnection subclass,
		and add it to the root code connection.

		:param	root_code_element(CodeElement) -> The object to process.
		:param	code_element(CodeElement) -> The object to process.
		"""
		for element_cls in Builder._CODE_CONNECTIONS.values():
			if element_cls.match(root_code_element, code_element):
				root_code_connection.code_connections.append(element_cls(code_element))
		raise UnindetifiedElement((root_code_element, code_element_obj), CodeConnection)

	def _is_in_pkg(self, code_element):
		"""
		_is_in_pkg(self, code_element) -> Bool

		Tests of the code element is part of the package or outsourced.

		:param	code_element(CodeElement) -> A code element to test.
		"""
		return self.pkg == code_element.name.split(".", 1)[0]

	def _build_iterator(self, code_element):
		"""
		_build_iterator(self, code_element) -> generator/filter

		Retrieves the correct iterator for the building mechanism.

		:param	code_element(Object)
		:return filter, generator
		"""
		if self._is_pkg:
			return pkgutil.walk_packages(code_element.obj.__path__)
		return filter(lambda d: d.startswith(BuilderConsts.SKIPPED_PREFIXES), dir(code_element.obj))

	def _extract_obj(self, code_element, data):
		"""
		_extract_obj(self, code_element, data) -> str/obj

		Extracts the necessary object from the code element using the data.

		:param	code_element(CodeElement)
		:param	data(pkgutil.ModuleInfo, str)
		:return str/obj
		"""
		if self._is_pkg:
			return ".".join([code_element.name, data.name])
		return getattr(code_element, data)

	def _check_sentinel(self, code_element):
		"""
		_check_sentinel(self, code_element) -> Bool

		Checks if a sentinel was found, depends on the iterator.

		:param	code_element(CodeElement)
		:return Bool
		"""
		if self._is_pkg:

			# Set the _is_pkg flag according to the current code_element in the iterator.
			self._is_pkg = code_element.is_pkg
			return True

		return self._is_in_pkg(code_element)

	def _build(self, code_element):
		"""
		_build(self, code_element) -> CodeElement

		Processes all the sub code element found in code_element,
		based on the iterator.

		:param	code_element(CodeElement)
		"""
		for data in self._build_iterator(code_element): 

			# Create a sub code element found in the iterator.
			sub_code_element = self.create_code_element(self._extract_obj(code_element, data), \
														code_element)

			if _check_sentinel(sub_code_element):
				self._build(sub_code_element)

		return code_element