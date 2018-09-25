FILE_DOC_FORMAT = """~
Name: {0}
Purpose: {1}
Author: DavidGuler (davidguler.1x@gmail.com)
~"""
PACKAGE_PATH = os.path.dirname(__file__)
REGEX_FOR_DOC = re.compile("~\n")


class UnknownElementType(Exception):
	def __init__(self, element_type):
		self.element_type = element_type

	def __str__(self):
		return "Unknown element type recevied: {}".format(self.element_type)


class PackageIsNotFound(Exception):
	"""docstring for PackageIsNotFound"""
	def __init__(self, pkg):
		self.pkg = pkg

	def __str__(self):
		return "The package {} can not be found!".format(self.pkg)
		

class BuilderConsts():
	SKIPPED_PREFIXES = ["__"]