from flask import Flask,render_template,Response,request
from camera import VideoCamera
import cv2
import requests
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.secret_key="secret key"
#app.config['UPLOAD_FOLDER']=r"C:\Users\Kritika\Desktop\face_flask\static"
app.config['UPLOAD_FOLDER']='static/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS']=["jpg","png","mov","jpeg"]
app.config['DEBUG']=True

@app.route('/')
def index():
	return render_template('index.html')

def gen(camera):
	while(True):
		frame=camera.get_frame()
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
	video_stream = VideoCamera()
	return Response(gen(video_stream),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		return 'file uploaded successfully'
	#return render_template('index.html',filename=f)
	