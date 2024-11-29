import sqlite3

def init_db():
    conn = sqlite3.connect('rest_api_python.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS users''')
    c.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT NOT NULL)''')
    conn.commit()
    conn.close()