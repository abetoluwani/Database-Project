from tkinter import *
from tkinter import ttk, messagebox
from .base_component import BaseComponent
from database import db

class CoffeeForm(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.variables = {
            'coffee_id': StringVar(),
            'coffee_name': StringVar(),
            'type': StringVar(),
            'discount': StringVar(),
            'in_stock': StringVar(),
            'price': StringVar()
        }
        self.create_form()

    def create_form(self):
        """Create coffee form"""
        fields = [
            ('Coffee ID:', 'coffee_id'),
            ('Coffee Name:', 'coffee_name'),
            ('Type:', 'type'),
            ('Discount:', 'discount'),
            ('In Stock:', 'in_stock'),
            ('Price:', 'price')
        ]

        for i, (label_text, var_name) in enumerate(fields):
            # Create label
            label = self.create_widget(Label, f'label_{var_name}',
                                     text=label_text,
                                     font=("yu gothic ui", 12, "bold"))
            label.grid(row=i, column=0, padx=5, pady=5, sticky='e')

            # Create entry
            entry = self.create_widget(Entry, f'entry_{var_name}',
                                     textvariable=self.variables[var_name],
                                     font=("yu gothic ui", 12))
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')

    def get_values(self):
        """Get form values"""
        return {name: var.get() for name, var in self.variables.items()}

    def set_values(self, values):
        """Set form values"""
        for i, (name, value) in enumerate(zip(self.variables.keys(), values)):
            self.variables[name].set(value)

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

        # Validate numeric fields
        try:
            float(values['price'])
            int(values['in_stock'])
            float(values['discount'])
        except ValueError:
            messagebox.showerror("Error", "Invalid numeric values")
            return False

        return True

    def save_coffee(self):
        """Save coffee to database"""
        if not self.validate():
            return False

        values = self.get_values()
        try:
            if values['coffee_id']:  # Update existing
                db.execute_update("""
                    UPDATE Coffee_Category 
                    SET coffee_name=?, type=?, discount=?, in_stock=?, coffee_price=? 
                    WHERE coffee_id=?
                """, (values['coffee_name'], values['type'], values['discount'],
                     values['in_stock'], values['price'], values['coffee_id']))
            else:  # Insert new
                db.execute_update("""
                    INSERT INTO Coffee_Category 
                    (coffee_name, type, discount, in_stock, coffee_price)
                    VALUES (?, ?, ?, ?, ?)
                """, (values['coffee_name'], values['type'], values['discount'],
                     values['in_stock'], values['price']))
            
            messagebox.showinfo("Success", "Coffee saved successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save coffee: {str(e)}")
            return False
