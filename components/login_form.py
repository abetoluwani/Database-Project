from tkinter import *
from tkinter import ttk, messagebox
from .base_component import BaseComponent
from database import db

class LoginForm(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.variables = {
            'username': StringVar(),
            'password': StringVar()
        }
        self.create_form()

    def create_form(self):
        """Create login form"""
        # Username
        username_label = self.create_widget(Label, 'username_label',
                                          text="Username",
                                          font=("yu gothic ui", 12, "bold"))
        username_label.pack(pady=5)

        username_entry = self.create_widget(Entry, 'username_entry',
                                          textvariable=self.variables['username'],
                                          font=("yu gothic ui", 12))
        username_entry.pack(pady=5)

        # Password
        password_label = self.create_widget(Label, 'password_label',
                                          text="Password",
                                          font=("yu gothic ui", 12, "bold"))
        password_label.pack(pady=5)

        password_entry = self.create_widget(Entry, 'password_entry',
                                          textvariable=self.variables['password'],
                                          font=("yu gothic ui", 12),
                                          show="*")
        password_entry.pack(pady=5)

    def get_credentials(self):
        """Get entered credentials"""
        return {
            'username': self.variables['username'].get(),
            'password': self.variables['password'].get()
        }

    def clear(self):
        """Clear form fields"""
        for var in self.variables.values():
            var.set('')

    def validate(self):
        """Validate form input"""
        credentials = self.get_credentials()
        if not credentials['username'] or not credentials['password']:
            messagebox.showerror("Error", "Please fill in all fields")
            return False
        return True
