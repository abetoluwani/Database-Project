from tkinter import *
from tkinter import ttk, messagebox
from .base_component import BaseComponent
from database import db

class InventorySearch(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.search_var = StringVar()
        self.create_search()

    def create_search(self):
        """Create search interface"""
        # Search frame
        frame = self.create_widget(Frame, 'search_frame')
        frame.pack(fill=X, padx=5, pady=5)

        # Search label
        label = self.create_widget(Label, 'search_label',
                                 text="Search Bill:",
                                 font=('arial', 12, 'bold'))
        label.pack(side=LEFT, padx=5)

        # Search entry
        entry = self.create_widget(Entry, 'search_entry',
                                 textvariable=self.search_var,
                                 font=('arial', 12))
        entry.pack(side=LEFT, fill=X, expand=True, padx=5)

        # Search button
        button = self.create_widget(Button, 'search_button',
                                  text="Search",
                                  command=self.search,
                                  font=('arial', 12))
        button.pack(side=LEFT, padx=5)

    def search(self):
        """Perform search"""
        bill_number = self.search_var.get().strip()
        if not bill_number:
            messagebox.showerror("Error", "Please enter a bill number")
            return None

        result = db.execute_query("SELECT * FROM Inventory WHERE bill_number = ?", (bill_number,))
        if not result:
            messagebox.showerror("Error", "Bill not found")
            return None

        return result[0]

    def clear(self):
        """Clear search field"""
        self.search_var.set('')
