from CodeViewer.core.builder.builder import Builder
from CodeViewer.core.base_elements.base_elements import BaseCodeConnection
import tkinter

@Builder.register_element
class CC_Inherit(BaseCodeConnection):
	pass

@Builder.register_element
class CC_Property(BaseCodeConnection):
	pass

@Builder.register_element
class CC_Namespace(BaseCodeConnection):
	pass

@Builder.register_element
class CC_Submodule(BaseCodeConnection):
	pass