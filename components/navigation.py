from tkinter import *
from tkinter import ttk, messagebox
from .base_component import BaseComponent
from PIL import Image, ImageTk

class NavigationBar(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.callbacks = {}
        self.create_navigation()

    def create_navigation(self):
        """Create navigation bar"""
        # Create main frame
        nav_frame = self.create_widget(Frame, 'nav_frame',
                                     bg='#f6f6f9')
        nav_frame.pack(fill=X, pady=5)

        # Create buttons
        buttons = [
            ('Home', 'home'),
            ('Products', 'products'),
            ('Inventory', 'inventory'),
            ('Accounts', 'accounts'),
            ('Logout', 'logout')
        ]

        for text, name in buttons:
            btn = self.create_widget(Button, f'btn_{name}',
                                   text=text,
                                   font=("yu gothic ui", 13, "bold"),
                                   bg='#f6f6f9',
                                   fg='#7a7a7a',
                                   bd=0,
                                   cursor='hand2')
            btn.pack(side=LEFT, padx=10)
            btn.bind('<Button-1>', lambda e, n=name: self._handle_click(n))

    def on_navigate(self, name, callback):
        """Set navigation callback"""
        self.callbacks[name] = callback

    def _handle_click(self, name):
        """Handle navigation click"""
        callback = self.callbacks.get(name)
        if callback:
            callback()

class MenuBar(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.callbacks = {}
        self.create_menu()

    def create_menu(self):
        """Create menu bar"""
        menubar = self.create_widget(Menu, 'menubar')
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", 
                            command=lambda: self._handle_click('new'))
        file_menu.add_command(label="Open", 
                            command=lambda: self._handle_click('open'))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", 
                            command=lambda: self._handle_click('exit'))
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Cut", 
                            command=lambda: self._handle_click('cut'))
        edit_menu.add_command(label="Copy", 
                            command=lambda: self._handle_click('copy'))
        edit_menu.add_command(label="Paste", 
                            command=lambda: self._handle_click('paste'))
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", 
                            command=lambda: self._handle_click('about'))
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.parent.config(menu=menubar)

    def on_menu(self, name, callback):
        """Set menu callback"""
        self.callbacks[name] = callback

    def _handle_click(self, name):
        """Handle menu click"""
        callback = self.callbacks.get(name)
        if callback:
            callback()
