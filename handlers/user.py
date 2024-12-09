import json
import os
import sqlite3
import urllib.parse
from http.server import BaseHTTPRequestHandler

class UserHandler(BaseHTTPRequestHandler):
    def handleRequest(self, method):
        request_path = self.path
        if not self.isValidPath(request_path):
            self.sendNotFound()
            return
        if method == "GET":
            self.handleReadUsers()
        elif method == "POST":
            self.handleCreateUser()
        elif method == "PUT":
            self.handleUpdateUser()
        elif method == "DELETE":
            self.handleDeleteUser()
        else:
            self.sendMethodNotAllowed()

    def do_GET(self):
        self.handleRequest("GET")

    def do_POST(self):
        self.handleRequest("POST")

    def do_PUT(self):
        self.handleRequest("PUT")

    def do_DELETE(self):
        self.handleRequest("DELETE")

    def do_PATCH(self):
        self.handleRequest("PATCH")

    def do_HEAD(self):
        self.handleRequest("HEAD")

    def do_OPTIONS(self):
        self.handleRequest("OPTIONS")

    def isValidPath(self, path):
        return path == "/users" or path == "/users/"

    def sendNotFound(self):
        response = {"status": "Not Found", "code": 404}
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))

    def sendMethodNotAllowed(self):
        response = {"status": "Method Not Allowed", "code": 405}
        self.send_response(405)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))

    def handleReadUsers(self):
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

    def handleCreateUser(self):
        try:
            content_length = self.headers.get('Content-Length', 0)  # Safely get Content-Length
            content_length = int(content_length) if content_length else 0
            if content_length == 0:
                response = {"status": "Bad Request", "code": 400, "errors": "Missing 'name' parameter"}
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return
        except Exception as e:
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

    def handleUpdateUser(self):
        try:
            content_length = self.headers.get('Content-Length', 0)  # Safely get Content-Length
            content_length = int(content_length) if content_length else 0
            if content_length == 0:
                response = {"status": "Bad Request", "code": 400, "errors": "Missing 'id' or 'name' parameter"}
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return
        except Exception as e:
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

    def handleDeleteUser(self):
        try:
            content_length = self.headers.get('Content-Length', 0)  # Safely get Content-Length
            content_length = int(content_length) if content_length else 0
            if content_length == 0:
                response = {"status": "Bad Request", "code": 400, "errors": "Missing 'id' parameter"}
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return
        except Exception as e:
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