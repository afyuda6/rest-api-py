import json
import os
import re
import sqlite3
import urllib.parse
from http.server import BaseHTTPRequestHandler


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
        parsed_url = urllib.parse.urlparse(self.path)
        if re.match(r"^/users(/.*)?$", parsed_url.path):
            db_path = os.path.join(os.path.dirname(__file__), '../rest_api_python.db')
            conn = sqlite3.connect(os.path.abspath(db_path))
            c = conn.cursor()
            c.execute("SELECT id, name FROM users")
            users = c.fetchall()
            conn.close()
            response_data = [{"id": user[0], "name": user[1]} for user in users]
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
        parsed_url = urllib.parse.urlparse(self.path)
        if re.match(r"^/users(/.*)?$", parsed_url.path):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode("utf-8"))
            name = data.get("name", [None])[0]

            db_path = os.path.join(os.path.dirname(__file__), '../rest_api_python.db')
            conn = sqlite3.connect(os.path.abspath(db_path))
            c = conn.cursor()
            c.execute("INSERT INTO users (name) VALUES (?)", (name,))
            conn.commit()
            conn.close()

            response = {"status": "Created", "code": 201}

            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            response = {"status": "Not Found", "code": 404}
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

    def handleUpdateUser(self):
        parsed_url = urllib.parse.urlparse(self.path)
        if re.match(r"^/users(/.*)?$", parsed_url.path):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode("utf-8"))
            name = data.get("name", [None])[0]
            id = data.get("id", [None])[0]

            db_path = os.path.join(os.path.dirname(__file__), '../rest_api_python.db')
            conn = sqlite3.connect(os.path.abspath(db_path))
            c = conn.cursor()
            c.execute("UPDATE users SET name = ? WHERE id = ?", (name, id,))
            conn.commit()
            conn.close()

            response = {"status": "OK", "code": 200}

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

    def handleDeleteUser(self):
        parsed_url = urllib.parse.urlparse(self.path)
        if re.match(r"^/users(/.*)?$", parsed_url.path):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode("utf-8"))
            id = data.get("id", [None])[0]

            db_path = os.path.join(os.path.dirname(__file__), '../rest_api_python.db')
            conn = sqlite3.connect(os.path.abspath(db_path))
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id = ?", (id,))
            conn.commit()
            conn.close()

            response = {"status": "OK", "code": 200}

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