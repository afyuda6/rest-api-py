import json
import os
import sqlite3
import urllib.parse
from http.server import BaseHTTPRequestHandler

class User(BaseHTTPRequestHandler):
    def do_GET(self):
        self.user_handler("GET")

    def do_POST(self):
        self.user_handler("POST")

    def do_PUT(self):
        self.user_handler("PUT")

    def do_DELETE(self):
        self.user_handler("DELETE")

    def do_PATCH(self):
        self.user_handler("PATCH")

    def do_HEAD(self):
        self.user_handler("HEAD")

    def do_OPTIONS(self):
        self.user_handler("OPTIONS")

    def handle_read_user(self):
        db_path = os.path.join(os.path.dirname(__file__), '../rest_api_py.db')
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

    def handle_create_user(self):
        content_length = self.headers.get('Content-Length', 0)  # Safely get Content-Length
        content_length = int(content_length) if content_length else 0
        if content_length == 0:
            response = {"status": "Bad Request", "code": 400, "errors": "Missing 'name' parameter"}
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode("utf-8"))
        name = data.get("name", [None])[0]
        if name is None or name.strip() == "":
            response = {"status": "Bad Request", "code": 400, "errors": "Missing 'name' parameter"}
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return
        db_path = os.path.join(os.path.dirname(__file__), '../rest_api_py.db')
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

    def handle_update_user(self):
        content_length = self.headers.get('Content-Length', 0)  # Safely get Content-Length
        content_length = int(content_length) if content_length else 0
        if content_length == 0:
            response = {"status": "Bad Request", "code": 400, "errors": "Missing 'id' or 'name' parameter"}
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode("utf-8"))
        name = data.get("name", [None])[0]
        id = data.get("id", [None])[0]
        if name is None or id is None:
            response = {"status": "Bad Request", "code": 400, "errors": "Missing 'id' or 'name' parameter"}
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return
        if name.strip() == "" or id.strip() == "":
            response = {"status": "Bad Request", "code": 400, "errors": "Missing 'id' or 'name' parameter"}
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return
        db_path = os.path.join(os.path.dirname(__file__), '../rest_api_py.db')
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

    def handle_delete_user(self):
        content_length = self.headers.get('Content-Length', 0)  # Safely get Content-Length
        content_length = int(content_length) if content_length else 0
        if content_length == 0:
            response = {"status": "Bad Request", "code": 400, "errors": "Missing 'id' parameter"}
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode("utf-8"))
        id = data.get("id", [None])[0]
        if id is None or id.strip() == "":
            response = {"status": "Bad Request", "code": 400, "errors": "Missing 'id' parameter"}
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return
        db_path = os.path.join(os.path.dirname(__file__), '../rest_api_py.db')
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

    def user_handler(self, method):
        if self.path != "/users" and self.path != "/users/":
            response = {"status": "Not Found", "code": 404}
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return
        if method == "GET":
            self.handle_read_user()
        elif method == "POST":
            self.handle_create_user()
        elif method == "PUT":
            self.handle_update_user()
        elif method == "DELETE":
            self.handle_delete_user()
        else:
            response = {"status": "Method Not Allowed", "code": 405}
            self.send_response(405)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))