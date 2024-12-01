import os
import sqlite3

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), '../rest_api_py.db')
    conn = sqlite3.connect(os.path.abspath(db_path))
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS users''')
    conn.commit()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL)''')
    conn.commit()
    conn.close()