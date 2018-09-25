__all__ = []

import os
import pkgutil
import re

FILE_DOC_FORMAT = """~
Name: {0}
Purpose: {1}
Author: DavidGuler (davidguler.1x@gmail.com)
~"""
KNOWN_FILES_EXTS = [".py"]
PACKAGE_PATH = os.path.dirname(__file__)
REGEX_FOR_DOC = re.compile("~\n")

file_name_func = lambda file_path: os.path.splitext(os.path.split(file_path)[1])[0]

def modify_file_doc(file_path, docstring, pattern):
	with open(file_path, 'r') as file_obj:
		new_docstring = re.sub(purpose, docstring, file_obj.read())

	with open(file_path, 'w') as file_obj:
		file_obj.write(new_docstring)

for unloaded_mod in pkgutil.walk_packages([PACKAGE_PATH], file_name_func(PACKAGE_PATH) + "."):
	if not unloaded_mod.ispkg:
		mod = unloaded_mod.module_finder.find_loader(unloaded_mod.name)[0].load_module(unloaded_mod.name)
		if mod.__doc__ and not REGEX_FOR_DOC.search(mod.__doc__):
			print(mod.__doc__, type(mod.__doc__))
			purpose = mod.__doc__.strip()
			file_name = file_name_func(mod.__file__)
			mod.__doc__ = FILE_DOC_FORMAT.format(file_name, purpose)
			modify_file_doc(mod.__file__, mod.__doc__, purpose)