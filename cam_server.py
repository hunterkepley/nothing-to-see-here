import datetime
from flask import Flask, render_template, Response
import time
import cv2
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

app = Flask(__name__,template_folder='Templates')
#app.config["CACHE_TYPE"] = "null"

@app.route('/')
def index():
    return render_template('index.html')

def gen(t):
    picam = Picamera2()
    config = picam.create_preview_configuration()
    picam.start()
    encoder = H264Encoder(10000000)
    output = FfmpegOutput('static/latest.mp4')
    picam.start_recording(encoder, output)
    time.sleep(t)
    picam.stop_recording()
    print("New video created!")
    print(datetime.datetime.now())
    picam.close()
        

@app.route('/video_feed')
def video_feed():
    gen(10)
    return render_template('index.html')

@app.route('/video_feed2')
def video_feed2():
    gen(30)
    return render_template('index.html')

@app.route('/video_feed3')
def video_feed3():
    gen(60)
    return render_template('index.html')

@app.route('/video_feed4')
def video_feed4():
    gen(120)
    return render_template('index.html')

@app.route('/video_feed5')
def video_feed5():
    gen(240)
    return render_template('index.html')

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=9911, debug=True, threaded=True)
