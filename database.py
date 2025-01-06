import sqlite3
from contextlib import contextmanager
from typing import Any, Generator, List, Tuple

class Database:
    _instance = None
    DATABASE_PATH = "./Database/CoffeeShop.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Get a database connection with context management."""
        conn = sqlite3.connect(self.DATABASE_PATH)
        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    def get_cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        """Get a database cursor with context management."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            finally:
                cursor.close()

    def execute_query(self, query: str, params: tuple = ()) -> List[Tuple]:
        """Execute a query and return all results."""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update query and return number of affected rows."""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount

    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Execute many updates and return number of affected rows."""
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount

# Create a singleton instance
db = Database()
