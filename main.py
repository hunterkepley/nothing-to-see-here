import ssl
import datetime
import time
import io
import logging
import os
import socketserver
import sys
import scripts.cam_server as cs
from http import server
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, JpegEncoder
from picamera2.outputs import FfmpegOutput, FileOutput

resolution = (2048, 1080)

def main():
    os.environ['LOGGED_IN'] = 'f'
    os.environ['CLIENT_IP'] = '-1'
    picam = Picamera2()
    picam.configure(picam.create_video_configuration(main={"size": resolution}))
    picam.start_recording(JpegEncoder(), FileOutput(cs.output))
    try:
        address = ('', 9911)
        server = cs.StreamingServer(address, cs.StreamingHandler)

        # SSL
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain('cert.pem', 'key.pem')

        server.socket = ssl_context.wrap_socket(server.socket, server_side=True)

        server.serve_forever()
    finally:
        picam.stop_recording()

if __name__ == '__main__':
    old_stdout = sys.stdout
    log_file = open('logs.txt', 'a')
    sys.stdout = log_file
    main()
    sys.stdout = old_stdout
    log_file.close()

