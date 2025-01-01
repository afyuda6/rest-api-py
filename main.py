import os
from http.server import HTTPServer
from database.sqlite import init_db
from handlers.user import User


def run(serverClass=HTTPServer, handlerClass=User):
    port = int(os.environ.get('PORT', 6006))
    init_db()
    serverAddress = ('', port)
    httpd = serverClass(serverAddress, handlerClass)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
