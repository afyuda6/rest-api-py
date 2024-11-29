import json
import sqlite3
from http.server import BaseHTTPRequestHandler
from database.sqlite import init_db


class UserHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handleReadUsers()

    def do_POST(self):
        self.handleCreateUser()

    def do_PUT(self):
        self.handleUpdateUser()

    def do_DELETE(self):
        self.handleDeleteUser()

    def handleReadUsers(self):
        if self.path == "/users":
            conn = sqlite3.connect('rest_api_python.db')
            c = conn.cursor()
            c.execute("SELECT * FROM items")
            items = c.fetchall()
            conn.close()
            response_data = [{"id": item[0], "name": item[1]} for item in items]
            response = {"status": "OK", "code": 200, "data": response_data}

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            response = {"status": "Not Found", "code": 404}
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

    def handleCreateUser(self):
        return

    def handleUpdateUser(self):
        return

    def handleDeleteUser(self):
        return