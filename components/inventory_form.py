from tkinter import *
from tkinter import ttk, messagebox
from .base_component import BaseComponent

class InventoryForm(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.variables = {}
        self.create_form()

    def create_form(self):
        """Create the inventory form"""
        # Create variables
        self.variables.update({
            'bill_number': StringVar(),
            'date': StringVar(),
            'cashier_name': StringVar(),
            'contact': StringVar()
        })

        # Create labels and entries
        labels = [
            ('Bill Number:', 'bill_number'),
            ('Date:', 'date'),
            ('Cashier Name:', 'cashier_name'),
            ('Contact:', 'contact')
        ]

        for i, (label_text, var_name) in enumerate(labels):
            # Create label
            label = self.create_widget(Label, f'label_{var_name}',
                                     text=label_text,
                                     font=('arial', 12, 'bold'))
            label.grid(row=i, column=0, padx=5, pady=5, sticky='e')

            # Create entry
            entry = self.create_widget(Entry, f'entry_{var_name}',
                                     textvariable=self.variables[var_name],
                                     font=('arial', 12))
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')

    def get_values(self):
        """Get all form values"""
        return {name: var.get() for name, var in self.variables.items()}

    def set_values(self, values):
        """Set form values"""
        for name, value in values.items():
            if name in self.variables:
                self.variables[name].set(value)

    def clear(self):
        """Clear all form values"""
        for var in self.variables.values():
            var.set('')

    def validate(self):
        """Validate form values"""
        values = self.get_values()
        empty_fields = [name for name, value in values.items() if not value.strip()]
        
        if empty_fields:
            messagebox.showerror("Error", "Please fill in all fields")
            return False
        return True
