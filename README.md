## Video Pulse Monitor

This repository features a python script which is able to measure your heartbeat using a webcam or some other camera attached to a computer. Blood flow in the skin plays a role in determining skin color, as for example evident by the reddening of the skin when someone is blushing. Likewise, blood circulation triggers a similar yet far more subtle change in color. 

In the figure below, the underlying principle that we want to exploit has been animated. Blood reflects red light while it strongly absorbs green light. Consequently, the ratio between red and green light forms the basis for the pulse signal. Additionally, we will make use of some additional post-processing techniques described in … to attenuate the effect of specular reflection and make the measurement somewhat motion robust.  

![Alt text](./underlying_principle.svg)



## Face Detection and Tracking


The most convenient location to extract the pulse is the face. Not only is this one of the most pulsatile regions on the body, many face detectors already exist. The face detector featured in this approach is the openCV implementation of the Violet Jones detector. However, this detector can be a bit inconsistent and cause the bounding box to jump around sometimes. Because this would lead to additional disturbance motion tracking is added to ensure a temporally smooth detection. 

![Alt text](./mtrack.svg)


## Pulse Extraction




