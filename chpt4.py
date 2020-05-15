import cv2,utils,time
import numpy as np
from scipy import signal

#%%
haar_cascade_path 	= "haarcascade_frontalface_default.xml"
face_cascade 		= cv2.CascadeClassifier(haar_cascade_path)
tracker 			= cv2.TrackerMOSSE_create()
cap 				= utils.RecordingReader() #cv2.VideoCapture(0)

fs					= 30
B,G,R               = 0,1,2

found_face 	            = False
initialized_tracker		= False
face_box            	= []
mean_colors             = []
timestamps 	            = []

mean_colors_resampled   = np.zeros((3,1))


while True: 
	
	ret, frame = cap.read() 
	frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	
	if found_face and initialized_tracker :
		print("Tracking")
		found_face,face_box = tracker.update(frame)
		if not found_face:
			print("Lost Face")
			
	if not found_face:
		initialized_tracker = False
		print("Redetecing")
		faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
		found_face = len(faces) > 0

	if found_face and not initialized_tracker:			
		face_box = faces[0]
		tracker = cv2.TrackerMOSSE_create()
		tracker.init(frame,tuple(face_box))			
		initialized_tracker = True

	if found_face:
		face = utils.crop_to_boundingbox(face_box,frame)
		if face.shape[0] > 0 and face.shape[1]>0:
			
			mean_colors += [face.mean(axis=0).mean(axis=0)] 
			timestamps  +=  [ret]#[time.time()]
			utils.draw_face_roi(face_box,frame)
			
			t = np.arange(timestamps[0],timestamps[-1],1/fs)
			mean_colors_resampled = np.zeros((3,t.shape[0]))
			
			for color in [B,G,R]:
				resampled = np.interp(t,timestamps,np.array(mean_colors)[:,color])
				mean_colors_resampled[color] = resampled



	cv2.imshow('Camera',frame) 
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release() 
cv2.destroyAllWindows() 





#plt.figure()
