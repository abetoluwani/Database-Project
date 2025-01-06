import unittest
import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from tkinter import Tk
from AccountSystem import AccountPage
from admin import SecondPage as AdminPage
from Employee import SecondPage as EmployeePage

class TestCoffeeShopSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test database and create necessary tables"""
        # Initialize test database
        cls.test_db = "./Database/CoffeeShop.db"
        
        # Create test tables
        cls.create_test_tables()
        
        # Create test window
        cls.root = Tk()
        cls.root.withdraw()  # Hide the window during tests

    @classmethod
    def create_test_tables(cls):
        """Create test tables with sample data"""
        with sqlite3.connect(cls.test_db) as conn:
            cursor = conn.cursor()
            
            # Create Admin Account table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Admin_Account (
                    admin_id INTEGER PRIMARY KEY,
                    admin_username TEXT NOT NULL,
                    admin_password TEXT NOT NULL
                )
            ''')
            
            # Create Employee Account table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Employee_Account (
                    employee_id INTEGER PRIMARY KEY,
                    employee_username TEXT NOT NULL,
                    employee_password TEXT NOT NULL
                )
            ''')
            
            # Create Guest Account table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Guest_Account (
                    guest_id INTEGER PRIMARY KEY,
                    guest_fullname TEXT NOT NULL,
                    guest_username TEXT NOT NULL,
                    guest_password TEXT NOT NULL
                )
            ''')
            
            # Create Coffee Category table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Coffee_Category (
                    coffee_id INTEGER PRIMARY KEY,
                    coffee_name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    discount INTEGER,
                    in_stock INTEGER,
                    coffee_price REAL
                )
            ''')
            
            # Insert test data
            cursor.execute("INSERT INTO Admin_Account (admin_username, admin_password) VALUES (?, ?)",
                         ("admin_test", "test123"))
            
            cursor.execute("INSERT INTO Employee_Account (employee_username, employee_password) VALUES (?, ?)",
                         ("employee_test", "test123"))
            
            cursor.execute("INSERT INTO Guest_Account (guest_fullname, guest_username, guest_password) VALUES (?, ?, ?)",
                         ("Test Guest", "guest_test", "test123"))
            
            cursor.execute("""
                INSERT INTO Coffee_Category (coffee_name, type, discount, in_stock, coffee_price) 
                VALUES (?, ?, ?, ?, ?)
            """, ("Test Coffee", "purchase", 0, 100, 5.99))
            
            conn.commit()

    def setUp(self):
        """Set up test cases"""
        self.db = db

    def test_admin_login(self):
        """Test admin login functionality"""
        result = self.db.execute_query(
            "SELECT * FROM Admin_Account WHERE admin_username=? AND admin_password=?",
            ("admin_test", "test123")
        )
        self.assertTrue(len(result) > 0)

    def test_employee_login(self):
        """Test employee login functionality"""
        result = self.db.execute_query(
            "SELECT * FROM Employee_Account WHERE employee_username=? AND employee_password=?",
            ("employee_test", "test123")
        )
        self.assertTrue(len(result) > 0)

    def test_guest_login(self):
        """Test guest login functionality"""
        result = self.db.execute_query(
            "SELECT * FROM Guest_Account WHERE guest_username=? AND guest_password=?",
            ("guest_test", "test123")
        )
        self.assertTrue(len(result) > 0)

    def test_coffee_operations(self):
        """Test CRUD operations for coffee"""
        # Test Create
        self.db.execute_update(
            "INSERT INTO Coffee_Category (coffee_name, type, discount, in_stock, coffee_price) VALUES (?, ?, ?, ?, ?)",
            ("New Coffee", "purchase", 10, 50, 4.99)
        )
        
        # Test Read
        result = self.db.execute_query(
            "SELECT * FROM Coffee_Category WHERE coffee_name=?",
            ("New Coffee",)
        )
        self.assertTrue(len(result) > 0)
        
        # Test Update
        self.db.execute_update(
            "UPDATE Coffee_Category SET coffee_price=? WHERE coffee_name=?",
            (5.99, "New Coffee")
        )
        
        # Test Delete
        self.db.execute_update(
            "DELETE FROM Coffee_Category WHERE coffee_name=?",
            ("New Coffee",)
        )

    def test_guest_registration(self):
        """Test guest registration"""
        self.db.execute_update(
            "INSERT INTO Guest_Account (guest_fullname, guest_username, guest_password) VALUES (?, ?, ?)",
            ("New Guest", "new_guest", "password123")
        )
        
        result = self.db.execute_query(
            "SELECT * FROM Guest_Account WHERE guest_username=?",
            ("new_guest",)
        )
        self.assertTrue(len(result) > 0)

    def test_inventory_management(self):
        """Test inventory management"""
        # Test updating stock
        self.db.execute_update(
            "UPDATE Coffee_Category SET in_stock=? WHERE coffee_name=?",
            (90, "Test Coffee")
        )
        
        result = self.db.execute_query(
            "SELECT in_stock FROM Coffee_Category WHERE coffee_name=?",
            ("Test Coffee",)
        )
        self.assertEqual(result[0][0], 90)

    def test_discount_application(self):
        """Test discount application"""
        # Test applying discount
        self.db.execute_update(
            "UPDATE Coffee_Category SET discount=? WHERE coffee_name=?",
            (25, "Test Coffee")
        )
        
        result = self.db.execute_query(
            "SELECT discount FROM Coffee_Category WHERE coffee_name=?",
            ("Test Coffee",)
        )
        self.assertEqual(result[0][0], 25)

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        cls.root.destroy()
        # Remove test database
if __name__ == '__main__':
    unittest.main()
