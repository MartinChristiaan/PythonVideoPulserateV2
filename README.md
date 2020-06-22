## Video Pulse Monitor

This repository features a python script which is able to measure your heartbeat using a webcam or some other camera attached to a computer. Blood flow in the skin plays a role in determining skin color, as for example evident by the reddening of the skin when someone is blushing. Likewise, blood circulation triggers a similar yet far more subtle change in color. 

In the figure below, the underlying principle that we want to exploit has been animated. Blood reflects red light while it strongly absorbs green light. Consequently, the ratio between red and green light forms the basis for the pulse signal. Additionally, we will make use of some additional post-processing techniques proposed by G. de Haan to attenuate the effect of specular reflection and make the measurement somewhat motion robust [1].  

![Alt text](./underlying_principle.svg)



## Face Detection and Tracking


The most convenient location to extract the pulse is the face. Not only is this one of the most pulsatile regions on the body, many face detectors already exist. The face detector featured in this approach is the openCV implementation of the Violet Jones detector. However, this detector can be a bit inconsistent and cause the bounding box to jump around sometimes. Because this would lead to additional disturbance motion tracking is added to ensure a temporally smooth detection. 

Once a face is detected the motion tracker should become active so it can stabilize the region of interest. If at some point the motion tracker fails to track the face, it should wait until the detector is able to relocate the face. To ensure this behavior the face detector/tracker follows the finite state machine as depicted in the figure below. From the face region, a pulse signal can be created by averaging the pixels in the region predicted by the face detector/tracker.


![Alt text](./mtrack.svg)

## Resampling

However, before we can measure the pulse another problem has to be solved. Because camera frame rates can be inconsistent it is important to resample the signal so that it matches the expected sampling frequency. This is why a timestamp is required for every frame recorded from the camera. To get the temporal positions for every measurement a time array using the sampling frequency. Subsequently, the numpy interpolate function can be used to interpolate between the recorded pixel values to obtain a signal with fixed timesteps.


## Pulse Extraction


The final segment of the code contains a pulse extraction method from ... which can start once enough samples have been collected. The first step is to collect the last part of the signal and to extract the slowly changing DC component by normalizing and detrending the signal. Subsequently, the signal is compensated for skin tone using the skin vector.  This combined with the normalization stage are important steps to ensure proper operation for non-white illumination and light of any intensity. After this compensation the chrominance signals Xf and Yf can be created. These signals are composed in such a way that blood volume changes affect both signals differently, but specular reflection has the same effect on both signals. By bandpass filtering these signals various components that are outside of the expected spectrum can be removed. Finally, the coefficient alpha_chrom is created using the ratio of the standard deviation of the chrominance signals. This compensates possible deviations from the standardized skin tone.

## References

1. Chrominance Method : Haan, G. De, & Jeanne, V. (2013). Robust pulse-rate from chrominance-based rPPG. (c), 1–9. https://doi.org/10.1109/TBME.2013.2266196