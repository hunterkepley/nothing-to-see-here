import datetime
import time
import io
import logging
import socketserver
from http import server
from threading import Condition
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, JpegEncoder
from picamera2.outputs import FfmpegOutput, FileOutput

resolution = (2048, 1080)

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
    def do_GET(self):
        if self.path == '/stream.mjpg':
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
        elif self.path == "/" or self.path == "/live":
            self.path = '/Templates/index.html'
            try:
                file = open(self.path[1:]).read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(file, 'utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 - Not Found')
        else:
            self.send_error(404)
            self.end_headers()
            self.wfile.write(b'404 - Not Found')


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    picam = Picamera2()
    picam.configure(picam.create_video_configuration(main={"size": resolution}))
    picam.start_recording(JpegEncoder(), FileOutput(output))
    try:
        address = ('', 9911)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        picam.stop_recording()

if __name__ == '__main__':
    main()
