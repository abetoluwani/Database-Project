from tkinter import *
from tkinter import ttk, messagebox
from .base_component import BaseComponent
from database import db
import string
import random

class BillingForm(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.variables = {
            'bill_number': StringVar(),
            'date': StringVar(),
            'cashier_name': StringVar(),
            'customer_name': StringVar(),
            'contact': StringVar()
        }
        self.cart_items = []
        self.create_form()

    def create_form(self):
        """Create billing form"""
        # Create main frames
        left_frame = self.create_widget(Frame, 'left_frame')
        left_frame.pack(side=LEFT, fill=Y, padx=5)

        right_frame = self.create_widget(Frame, 'right_frame')
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)

        # Create form fields in left frame
        fields = [
            ('Bill Number:', 'bill_number'),
            ('Date:', 'date'),
            ('Cashier:', 'cashier_name'),
            ('Customer:', 'customer_name'),
            ('Contact:', 'contact')
        ]

        for label_text, var_name in fields:
            field_frame = self.create_widget(Frame, f'frame_{var_name}')
            field_frame.pack(fill=X, pady=5)
            
            label = self.create_widget(Label, f'label_{var_name}',
                                     text=label_text,
                                     font=("yu gothic ui", 12, "bold"))
            label.pack(side=LEFT, padx=5)

            entry = self.create_widget(Entry, f'entry_{var_name}',
                                     textvariable=self.variables[var_name],
                                     font=("yu gothic ui", 12))
            entry.pack(side=LEFT, fill=X, expand=True, padx=5)

        # Create cart table in right frame
        self.create_cart_table(right_frame)

    def create_cart_table(self, parent):
        """Create cart table"""
        # Create table frame
        table_frame = self.create_widget(Frame, 'table_frame')
        table_frame.pack(fill=BOTH, expand=True)

        # Create table with scrollbars
        columns = ("Item", "Price", "Quantity", "Total")
        self.cart_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Create scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.cart_tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient=HORIZONTAL, command=self.cart_tree.xview)
        
        # Configure scrollbars
        self.cart_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Pack everything
        self.cart_tree.pack(side=LEFT, fill=BOTH, expand=True)
        y_scroll.pack(side=RIGHT, fill=Y)
        x_scroll.pack(side=BOTTOM, fill=X)
        
        # Configure columns
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100)

    def add_to_cart(self, item, price, quantity):
        """Add item to cart"""
        total = price * quantity
        self.cart_tree.insert('', END, values=(item, price, quantity, total))
        self.cart_items.append({
            'item': item,
            'price': price,
            'quantity': quantity,
            'total': total
        })

    def get_cart_total(self):
        """Calculate cart total"""
        return sum(item['total'] for item in self.cart_items)

    def clear_cart(self):
        """Clear cart"""
        self.cart_tree.delete(*self.cart_tree.get_children())
        self.cart_items.clear()

    def generate_bill_number(self):
        """Generate unique bill number"""
        chars = string.ascii_uppercase + string.digits
        while True:
            bill_number = ''.join(random.choice(chars) for _ in range(8))
            # Check if bill number exists
            if not db.execute_query("SELECT 1 FROM Inventory WHERE bill_number = ?", 
                                  (bill_number,)):
                return bill_number

    def save_bill(self):
        """Save bill to database"""
        if not self.cart_items:
            messagebox.showerror("Error", "Cart is empty")
            return False

        values = self.get_values()
        bill_details = self.format_bill_details()

        try:
            db.execute_update("""
                INSERT INTO Inventory 
                (bill_number, date, cashier_name, customer_name, contact, bill_details)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (values['bill_number'], values['date'], values['cashier_name'],
                 values['customer_name'], values['contact'], bill_details))
            
            # Update stock
            for item in self.cart_items:
                db.execute_update("""
                    UPDATE Coffee_Category 
                    SET in_stock = in_stock - ? 
                    WHERE coffee_name = ?
                """, (item['quantity'], item['item']))

            messagebox.showinfo("Success", "Bill saved successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {str(e)}")
            return False

    def format_bill_details(self):
        """Format bill details for storage"""
        details = []
        for item in self.cart_items:
            details.append(
                f"{item['item']:<20} {item['price']:>8.2f} x {item['quantity']:>3} = {item['total']:>8.2f}"
            )
        details.append("-" * 50)
        details.append(f"Total: {self.get_cart_total():>8.2f}")
        return "\n".join(details)

    def get_values(self):
        """Get form values"""
        return {name: var.get() for name, var in self.variables.items()}
