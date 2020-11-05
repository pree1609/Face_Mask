from keras.models import load_model
import cv2
import numpy as np

model=load_model('model-017.model')
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
mouth_cascade=cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
labels={0:'Stay Safe!',1:'Wear a mask!'}
color={0:(0,255,0),1:(0,0,255)}

class VideoCamera(object):

	def __init__(self):
		self.cap=cv2.VideoCapture(0)

	def __del__(self):
		self.cap.release()

	def get_frame(self):
		_,img=self.cap.read()
		imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		faces=face_cascade.detectMultiScale(imgray,1.3,5)
		for(x,y,w,h) in faces:
			roi=imgray[y:y+h,x:x+w]
			resized_img=cv2.resize(roi,(100,100))
			normal=resized_img/255.0
			reshaped=np.reshape(normal,(1,100,100,1))
			res=model.predict(reshaped)
			label=np.argmax(res,axis=1)[0]
			cv2.rectangle(img,(x,y),(x+w,y+h),color[label],2)
			cv2.rectangle(img,(x,y-40),(x+w,y),color[label],-1)
			cv2.putText(img,labels[label],(x,y-10),cv2.FONT_HERSHEY_DUPLEX,0.8,(255,255,255),2)
		r,jpeg=cv2.imencode('.jpg',img)
		return jpeg.tobytes()

class VideoCamera2(object):
	def __init__(self):
		self.cap=cv2.VideoCapture(0)

	def __del__(self):
		self.cap.release()

	def get_frame(self):
		_,img=self.cap.read() #getting each frame
		resized_img=cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
		face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		gray_img=cv2.cvtColor(resized_img,cv2.COLOR_BGR2GRAY)
		faces=face_cascade.detectMultiScale(gray_img,1.1,4)
		for (x,y,w,h) in faces:
			cv2.rectangle(resized_img,(x,y), (x+w,y+h),(0,255,0),2)
		r,jpeg=cv2.imencode('.jpg',resized_img)
		return jpeg.tobytes()
