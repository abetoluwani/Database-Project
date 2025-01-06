from tkinter import *
from tkinter import ttk, messagebox
from .base_component import BaseComponent
from database import db

class InventoryTable(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_table()
        self.callbacks = {}

    def create_table(self):
        """Create the inventory table"""
        columns = ("Bill Number", "Date", "Cashier Name", "Contact", "Bill Details")
        self.tree = self.create_widget(ttk.Treeview, 'tree', columns=columns, show="headings", height=15)
        
        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col, anchor=CENTER)
            self.tree.column(col, width=150, anchor=CENTER)

        # Create scrollbars
        y_scroll = self.create_widget(ttk.Scrollbar, 'y_scroll', orient=VERTICAL, command=self.tree.yview)
        x_scroll = self.create_widget(ttk.Scrollbar, 'x_scroll', orient=HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

    def refresh_data(self):
        """Refresh table data from database"""
        rows = db.execute_query("SELECT * FROM Inventory")
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', END, values=row)

    def on_select(self, callback):
        """Set callback for row selection"""
        def internal_callback(event):
            selected = self.tree.focus()
            if selected:
                values = self.tree.item(selected)['values']
                callback(values)
        
        self.tree.bind('<<TreeviewSelect>>', internal_callback)

    def delete_selected(self):
        """Delete selected row"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a record to delete")
            return

        values = self.tree.item(selected)['values']
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete bill {values[0]}?"):
            db.execute_update("DELETE FROM Inventory WHERE bill_number = ?", (values[0],))
            self.refresh_data()
            return True
        return False
