from keras.models import load_model
import cv2
import numpy as np 

model=load_model('model-017.model')
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
labels_dict={0:'Stay Safe!',1:'Wear a mask!'}
color_dict={0:(0,255,0),1:(0,0,255)}

class VideoCamera(object):

	def __init__(self):
		self.cap=cv2.VideoCapture(0)

	def __del__(self):
		self.cap.release()

	def get_frame(self):
		_,frame=self.cap.read()
		gray_img=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		faces=face_cascade.detectMultiScale(gray_img,1.3,5)
		for(x,y,w,h) in faces:
			roi=gray_img[y:y+h,x:x+w]
			resized_img=cv2.resize(roi,(100,100))
			normal=resized_img/255.0
			reshaped=np.reshape(normal,(1,100,100,1))
			res=model.predict(reshaped)
			label=np.argmax(res,axis=1)[0]
			cv2.rectangle(frame,(x,y),(x+w,y+h),color_dict[label],2)
			cv2.rectangle(frame,(x,y-40),(x+w,y),color_dict[label],-1)
			cv2.putText(frame,labels_dict[label],(x,y-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8,(255,255,255),2)
		r,jpeg=cv2.imencode('.jpg',frame)
		return jpeg.tobytes()


