import cv2,utils
source	= utils.RecordingReader() #cv2.VideoCapture(0)
while True: 
	
	time, frame = source.read() 
	cv2.imshow('Camera',frame) 
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

source.release() 
cv2.destroyAllWindows() 
