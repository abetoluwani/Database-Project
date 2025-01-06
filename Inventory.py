from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from components import InventoryTable, InventoryForm, InventorySearch
from database import db

class InventoryPage:
    def __init__(self, Manage_window):
        self.Manage_window = Manage_window
        self.setup_window()
        self.create_components()
        self.setup_layout()

    def setup_window(self):
        """Setup the main window properties"""
        self.Manage_window.title("Inventory Management")
        self.Manage_window.geometry("1366x768")

    def create_components(self):
        """Create all UI components"""
        # Create main frames
        self.top_frame = Frame(self.Manage_window, bd=2, relief=RIDGE)
        self.top_frame.place(x=20, y=20, width=1325, height=90)

        self.left_frame = Frame(self.Manage_window, bd=2, relief=RIDGE)
        self.left_frame.place(x=20, y=120, width=400, height=620)

        self.right_frame = Frame(self.Manage_window, bd=2, relief=RIDGE)
        self.right_frame.place(x=430, y=120, width=915, height=620)

        # Create title
        title = Label(self.top_frame, text="Inventory Management", 
                     font=("times new roman", 30, "bold"),
                     bg="lightgray", fg="darkblue", bd=3, relief=RIDGE)
        title.pack(side=TOP, fill=X)

        # Create components
        self.search = InventorySearch(self.left_frame)
        self.form = InventoryForm(self.left_frame)
        self.table = InventoryTable(self.right_frame)

        # Create buttons frame
        self.buttons_frame = Frame(self.left_frame)
        self.buttons_frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)

        # Create buttons
        self.create_buttons()

    def create_buttons(self):
        """Create action buttons"""
        buttons = [
            ("Clear", self.clear_form),
            ("Delete", self.delete_record),
            ("Update", self.update_record),
            ("Logout", self.logout)
        ]

        for text, command in buttons:
            btn = Button(self.buttons_frame, text=text, command=command,
                        font=("arial", 12, "bold"), bg="lightgray", fg="darkblue")
            btn.pack(side=LEFT, padx=5, expand=True)

    def setup_layout(self):
        """Setup component layout and bindings"""
        # Setup form in left frame
        self.search.get_widget('search_frame').pack(fill=X, padx=5, pady=5)
        
        # Bind table selection to form
        self.table.on_select(self.on_record_select)

        # Initial data load
        self.table.refresh_data()

    def on_record_select(self, values):
        """Handle record selection in table"""
        if values:
            data = {
                'bill_number': values[0],
                'date': values[1],
                'cashier_name': values[2],
                'contact': values[3]
            }
            self.form.set_values(data)

    def clear_form(self):
        """Clear form and search"""
        self.form.clear()
        self.search.clear()

    def delete_record(self):
        """Delete selected record"""
        if self.table.delete_selected():
            self.clear_form()

    def update_record(self):
        """Update selected record"""
        if not self.form.validate():
            return

        values = self.form.get_values()
        try:
            db.execute_update("""
                UPDATE Inventory 
                SET date=?, cashier_name=?, contact=?
                WHERE bill_number=?
            """, (values['date'], values['cashier_name'], 
                 values['contact'], values['bill_number']))
            
            self.table.refresh_data()
            messagebox.showinfo("Success", "Record updated successfully")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update record: {str(e)}")

    def logout(self):
        """Logout and close window"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.Manage_window.destroy()
            import AccountSystem
            AccountSystem.AccountPage()

def page():
    window = Tk()
    InventoryPage(window)
    window.mainloop()

if __name__ == '__main__':
    page()
