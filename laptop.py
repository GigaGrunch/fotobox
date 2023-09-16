from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

def server_thread():
    server = HTTPServer(("", 8000), RequestHandler)
    server.serve_forever()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET!")
        self.send_response(200)
        self.end_headers()

Thread(target=server_thread).start()
