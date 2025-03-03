import http.server
import ssl
from multiprocessing import Process, Queue
import cgi
from server.protocol.interface import ServerLauncher, Server
from typing import Dict
from server.config import *

class HTTPSServer(Server):
    def __init__(self, txt_queue: Queue, file_queue: Queue):
        self.txt_queue = txt_queue
        self.file_queue = file_queue

        self.ip = SERVER_IP
        self.port = HTTPS_PORT

    class RequestHandler(http.server.BaseHTTPRequestHandler):
        def __init__(self, txt_queue: Queue, file_queue: Queue, debug_info: Dict, *args, **kwargs):
            self.txt_queue = txt_queue
            self.file_queue = file_queue
            self.debug_info = debug_info
            super().__init__(*args, **kwargs)

        def log_message(self, format, *args):
            # Suppress logging by overriding this method
            return

        def do_GET(self):
            """Handle GET requests"""
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Hello, world!")

        def do_POST(self):
            """Handle POST requests"""
            if 'Content-Type' in self.headers:
                content_type, pdict = cgi.parse_header(self.headers.get('Content-Type'))
                if content_type == 'multipart/form-data':
                    # Parse multipart form data
                    pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                    form_data = cgi.parse_multipart(self.rfile, pdict)
                    print("form data parsed", form_data)
                    for key, value in form_data.items():
                        if isinstance(value, list):
                            value = value[0]  # Get first item if it's a list

                        if isinstance(value, bytes):
                            filename = key  # Using field name as filename
                            self.file_queue.put((filename, value))
                            response = f"File {filename} saved successfully"
                        else:
                            response = f"Received data: {value.decode()}"
                            self.txt_queue.put(value.decode())

            else:
                # Handle non-file data
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                response = f"Received raw data: {post_data.decode()}"
                self.txt_queue.put(post_data.decode())

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode())

    def run(self):
        server_address = (self.ip, self.port)
        debug_info = {"ip": self.ip, "port": self.port}
        handler = lambda *args, **kwargs: self.RequestHandler(self.txt_queue, self.file_queue, debug_info, *args, **kwargs)
        httpd = http.server.HTTPServer(server_address, handler)
        
        # SSL Context to wrap the HTTP server
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile='certs/server.crt', keyfile='certs/server.key')  # Self-signed cert
        
        # Wrap the HTTP server socket with SSL
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        
        print(f"HTTPS server running on https://{self.ip}:{self.port}")
        httpd.serve_forever()

class HttpsServerLauncher(ServerLauncher):
    def __init__(self, txt_queue: Queue, file_queue: Queue):
        self.txt_queue = txt_queue
        self.file_queue = file_queue
        self.process = None

    def launch(self):
        server = HTTPSServer(self.txt_queue, self.file_queue)
        self.process = Process(target=server.run)
        self.process.start()

