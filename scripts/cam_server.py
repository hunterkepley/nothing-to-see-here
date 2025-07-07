import datetime
import os
import time
import io
import logging
import socketserver
from scripts.login import login
from http import server
from threading import Condition
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, JpegEncoder
from picamera2.outputs import FfmpegOutput, FileOutput

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

output = StreamingOutput()

class StreamingHandler(server.BaseHTTPRequestHandler):
    global output

    def do_POST(self):
        if self.path == '/otp':
            content_length = int(self.headers['content-length'])
            body = self.rfile.read(content_length)
            login(str(body), self.client_address[0])
            print('\n!!!\nUSER WHO TRIED TO LOG IN\'S INFORMATION:\n\n',self.headers,'\n!!!\n')
            self.path = 'Templates/index.html'
            try:
                self.send_response(301)
                self.send_header('Location', '/')
                self.end_headers()
                self.wfile.write(bytes(file, 'utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 - Not Found')
        elif self.path == '/logout':
            os.environ['LOGGED_IN'] = 'f'
            self.path = 'Templates/index.html'
            try:
                self.send_response(301)
                self.send_header('Location', '/')
                self.end_headers()
                self.wfile.write(bytes(file, 'utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 - Not Found')

    def do_GET(self):

        # CSS
        if self.path == '/style.css':
            self.path = '/Templates/style.css'
            try:
                file = open(self.path[1:]).read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/css')
                self.end_headers()
                self.wfile.write(bytes(file, 'utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-Type', 'text/css')
                self.send_headers()
                self.wfile.write(b'404 - Not Found')


        logged_in_value = os.environ['LOGGED_IN'] == 't'

        # HTML
        if not logged_in_value or self.client_address[0] != os.environ['CLIENT_IP']:
            os.environ['LOGGED_IN'] = 'f'
            self.path = '/Templates/login.html'
            try:
                file = open(self.path[1:]).read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(file, 'utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 - Not Found')
            return
        elif self.path == '/stream.mjpg' and logged_in_value:
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        elif self.path == "/" and logged_in_value:
            self.path = '/Templates/index.html'
            try:
                file = open(self.path[1:]).read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(file, 'utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 - Not Found')
        elif self.path == "/live" and logged_in_value:
            self.path = '/Templates/stream.html'
            try:
                file = open(self.path[1:]).read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(file, 'utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 - Not Found')
        else:
            self.send_error(404)
            self.end_headers()
            self.wfile.write(b'404 - Not Found')


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

