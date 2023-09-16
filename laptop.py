from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

def server_thread():
    server = HTTPServer(("", 8000), RequestHandler)
    server.serve_forever()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/take_picture":
            print("take picture!")
            self.send_response(200)
        else:
            self.send_response(500)
        self.end_headers()

Thread(target=server_thread).start()
