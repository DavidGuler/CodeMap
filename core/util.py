import os.path
import re
import pkgutil
from CodeMap.core.consts import PACKAGE_PATH, REGEX_FOR_DOC, FILE_DOC_FORMAT

def update_mods_doc():
	"""
	update_mods_doc() -> Updates all pkg mods docs.
	"""
	for unloaded_mod in pkgutil.walk_packages([PACKAGE_PATH], get_file_name(PACKAGE_PATH) + "."):
		if not unloaded_mod.ispkg:
			mod = load_mod(unloaded_mod)
			if mod.__doc__ and not REGEX_FOR_DOC.search(mod.__doc__):
				modify_mod_doc(mod)

def get_file_name(file_path):
	"""
	get_file_name(file_path) -> Extracts the file name without the ext from a path.
	"""
	return os.path.splitext(os.path.split(file_path)[1])[0]

def load_mod(u_m):
	"""
	load_mod(u_m) -> Loads the module using the ModuleFinderobj received.
	"""
	return u_m.module_finder.find_loader(u_m.name)[0].load_module(u_m.name)

def modify_mod_doc(mod):
	"""
	modify_file_doc(mod) -> Modifies the docstring in the mod received.
	"""
	purpose = mod.__doc__.strip()
	file_name = get_file_name(mod.__file__)
	docstring = FILE_DOC_FORMAT.format(file_name, purpose)

	with open(mod.__file__, 'r') as file_obj:
		new_docstring = re.sub(purpose, docstring, file_obj.read())

	with open(mod.__file__, 'w') as file_obj:
		file_obj.write(new_docstring)