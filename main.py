from http.server import HTTPServer
from database.sqlite import init_db
from handlers.user import UserHandler

def run(server_class=HTTPServer, handler_class=UserHandler, port=6003):
    init_db()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
