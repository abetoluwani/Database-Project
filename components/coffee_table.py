from tkinter import *
from tkinter import ttk, messagebox
from .base_component import BaseComponent
from database import db

class CoffeeTable(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_table()

    def create_table(self):
        """Create coffee table"""
        columns = (
            "ID",
            "Name",
            "Type",
            "Discount",
            "In Stock",
            "Price"
        )
        
        # Create treeview
        self.tree = self.create_widget(ttk.Treeview, 'tree',
                                     columns=columns,
                                     show="headings",
                                     height=15)

        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col, anchor=CENTER)
            self.tree.column(col, anchor=CENTER)

        # Add scrollbars
        y_scroll = self.create_widget(ttk.Scrollbar, 'y_scroll',
                                    orient=VERTICAL,
                                    command=self.tree.yview)
        x_scroll = self.create_widget(ttk.Scrollbar, 'x_scroll',
                                    orient=HORIZONTAL,
                                    command=self.tree.xview)

        self.tree.configure(yscrollcommand=y_scroll.set,
                          xscrollcommand=x_scroll.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

    def refresh_data(self):
        """Refresh table data"""
        rows = db.execute_query("SELECT * FROM Coffee_Category")
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', END, values=row)

    def get_selected(self):
        """Get selected item"""
        selected = self.tree.focus()
        if not selected:
            return None
        return self.tree.item(selected)['values']

    def on_select(self, callback):
        """Set callback for selection"""
        self.tree.bind('<<TreeviewSelect>>', 
                      lambda ev: callback(self.get_selected()))
