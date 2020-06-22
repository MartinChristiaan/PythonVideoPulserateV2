import cv2,utils,time
import numpy as np
from scipy import signal

#%% User Settings
use_prerecorded		= True
fs					= 30  # Sampling Frequency

#%% Parameters

haar_cascade_path 	= "haarcascade_frontalface_default.xml"
face_cascade 		= cv2.CascadeClassifier(haar_cascade_path)
tracker 			= cv2.TrackerMOSSE_create()
cap 				= utils.RecordingReader() if use_prerecorded else cv2.VideoCapture(0) 

window				= 300 # Number of samples to use for every measurement
skin_vec            = [0.3841,0.5121,0.7682]
B,G,R               = 0,1,2

found_face 	            = False
initialized_tracker		= False
face_box            	= []
mean_colors             = []
timestamps 	            = []

mean_colors_resampled   = np.zeros((3,1))

#%% Main loop

while True: 
	
	ret, frame = cap.read() 
	frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	# Try to update face location using tracker		
	if found_face and initialized_tracker :
		print("Tracking")
		found_face,face_box = tracker.update(frame)
		if not found_face:
			print("Lost Face")
	
	# Try to detect new face		
	if not found_face:
		initialized_tracker = False
		print("Redetecing")
		faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
		found_face = len(faces) > 0

	# Reset tracker
	if found_face and not initialized_tracker:			
		face_box = faces[0]
		tracker = cv2.TrackerMOSSE_create()
		tracker.init(frame,tuple(face_box))			
		initialized_tracker = True

	# Measure face color
	if found_face:
		face = utils.crop_to_boundingbox(face_box,frame)
		if face.shape[0] > 0 and face.shape[1]>0:
			
			mean_colors += [face.mean(axis=0).mean(axis=0)] 
			timestamps  +=  [ret] if use_prerecorded else [time.time()]
			utils.draw_face_roi(face_box,frame)
			t = np.arange(timestamps[0],timestamps[-1],1/fs)
			mean_colors_resampled = np.zeros((3,t.shape[0]))
			
			for color in [B,G,R]:
				resampled = np.interp(t,timestamps,np.array(mean_colors)[:,color])
				mean_colors_resampled[color] = resampled

	# Perform chrominance method
	if mean_colors_resampled.shape[1] > window:

		col_c = np.zeros((3,window))
        
		for col in [B,G,R]:
			col_stride 	= mean_colors_resampled[col,-window:]# select last samples
			y_ACDC 		= signal.detrend(col_stride/np.mean(col_stride))
			col_c[col] 	= y_ACDC * skin_vec[col]
            
		X_chrom     = col_c[R]-col_c[G]
		Y_chrom     = col_c[R] + col_c[G] - 2* col_c[B]
		Xf          = utils.bandpass_filter(X_chrom) 
		Yf          = utils.bandpass_filter(Y_chrom)
		Nx          = np.std(Xf)
		Ny          = np.std(Yf)
		alpha_CHROM = Nx/Ny
        
		x_stride   				= Xf - alpha_CHROM*Yf
		amplitude 				= np.abs( np.fft.fft(x_stride,window)[:int(window/2+1)])
		normalized_amplitude 	= amplitude/amplitude.max() #  Normalized Amplitude
		
		frequencies = np.linspace(0,fs/2,int(window/2) + 1) * 60
		bpm_index = np.argmax(normalized_amplitude)
		bpm       = frequencies[bpm_index]
		snr       = utils.calculateSNR(normalized_amplitude,bpm_index)
		utils.put_snr_bpm_onframe(bpm,snr,frame)

	cv2.imshow('Camera',frame) 
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release() 
cv2.destroyAllWindows() 





#plt.figure()
