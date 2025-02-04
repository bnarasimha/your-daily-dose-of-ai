import sqlite3
from datetime import datetime

class URLDatabase:
    def __init__(self):
        self.db_name = "custom_urls.db"
        self.init_database()

    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create table for custom URLs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def add_url(self, url: str) -> bool:
        """Add a new URL to the database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Check if URL already exists
            cursor.execute('SELECT url FROM custom_urls WHERE url = ?', (url,))
            if cursor.fetchone() is not None:
                return False
            
            # Insert new URL
            cursor.execute('INSERT INTO custom_urls (url) VALUES (?)', (url,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding URL: {e}")
            return False
        finally:
            conn.close()

    def get_all_urls(self) -> list:
        """Retrieve all URLs from the database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('SELECT url, added_date FROM custom_urls ORDER BY added_date DESC')
            urls = cursor.fetchall()
            return urls
        except Exception as e:
            print(f"Error retrieving URLs: {e}")
            return []
        finally:
            conn.close()

    def delete_url(self, url: str) -> bool:
        """Delete a URL from the database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM custom_urls WHERE url = ?', (url,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting URL: {e}")
            return False
        finally:
            conn.close() 