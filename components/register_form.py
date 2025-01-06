from tkinter import *
from tkinter import ttk, messagebox
from .base_component import BaseComponent
from database import db

class RegisterForm(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.variables = {
            'fullname': StringVar(),
            'username': StringVar(),
            'password': StringVar(),
            'confirm_password': StringVar()
        }
        self.create_form()

    def create_form(self):
        """Create registration form"""
        fields = [
            ('Full Name:', 'fullname'),
            ('Username:', 'username'),
            ('Password:', 'password'),
            ('Confirm Password:', 'confirm_password')
        ]

        for label_text, var_name in fields:
            # Create label
            label = self.create_widget(Label, f'label_{var_name}',
                                     text=label_text,
                                     font=("yu gothic ui", 12, "bold"))
            label.pack(pady=5)

            # Create entry
            show = "*" if 'password' in var_name else ""
            entry = self.create_widget(Entry, f'entry_{var_name}',
                                     textvariable=self.variables[var_name],
                                     font=("yu gothic ui", 12),
                                     show=show)
            entry.pack(pady=5)

    def get_values(self):
        """Get form values"""
        return {name: var.get() for name, var in self.variables.items()}

    def clear(self):
        """Clear form fields"""
        for var in self.variables.values():
            var.set('')

    def validate(self):
        """Validate form input"""
        values = self.get_values()
        
        # Check empty fields
        if not all(values.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return False
        
        # Check password match
        if values['password'] != values['confirm_password']:
            messagebox.showerror("Error", "Passwords do not match")
            return False

        return True

    def register_user(self, account_type='guest'):
        """Register a new user"""
        if not self.validate():
            return False

        values = self.get_values()
        try:
            if account_type == 'guest':
                db.execute_update(
                    "INSERT INTO Guest_Account (guest_fullname, guest_username, guest_password) VALUES (?, ?, ?)",
                    (values['fullname'], values['username'], values['password'])
                )
            elif account_type == 'employee':
                db.execute_update(
                    "INSERT INTO Employee_Account (employee_fullname, employee_username, employee_password) VALUES (?, ?, ?)",
                    (values['fullname'], values['username'], values['password'])
                )
            messagebox.showinfo("Success", "Registration successful!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
            return False
