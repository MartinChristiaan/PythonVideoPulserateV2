import cv2,utils,time
#%%
haar_cascade_path 	= "haarcascade_frontalface_default.xml"
face_cascade 		= cv2.CascadeClassifier(haar_cascade_path)
cap 				= utils.RecordingReader() #cv2.VideoCapture(0)


while True: 
	
	time, frame = cap.read() 
	frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
				
	faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
	if len(faces) > 0:
		face_box = faces[0]	
		utils.draw_face_roi(face_box,frame)


	cv2.imshow('Camera',frame) 
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release() 
cv2.destroyAllWindows() 





#plt.figure()
