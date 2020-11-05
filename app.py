from flask import Flask,render_template,Response,request
from camera import VideoCamera,VideoCamera2
import cv2
import requests
from werkzeug.utils import secure_filename
import gunicorn

app=Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def gen(camera):
	while(True):
		frame=camera.get_frame()
		yield (b'--frame\r\n'
			b'Content-Type: image/j6peg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
	video_stream = VideoCamera()
	return Response(gen(video_stream),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
	video_stream=VideoCamera2()
	return Response(gen(video_stream),mimetype='multipart/x-mixed-replace; boundary=frame')
