from tkinter import *
from tkinter import ttk

class BaseComponent:
    def __init__(self, parent):
        self.parent = parent
        self.widgets = {}
    
    def create_widget(self, widget_type, name, **kwargs):
        """Create and store a widget with a given name"""
        widget = widget_type(self.parent, **kwargs)
        self.widgets[name] = widget
        return widget
    
    def get_widget(self, name):
        """Get a widget by name"""
        return self.widgets.get(name)
    
    def destroy(self):
        """Destroy all widgets"""
        for widget in self.widgets.values():
            widget.destroy()
        self.widgets.clear()
