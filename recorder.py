import cv2,os,time
from tqdm import tqdm

name = "recording_rest"
if not os.path.exists(name):
    os.mkdir(name)

cap = cv2.VideoCapture(0)
timestamps = []
for idx in tqdm(range(1500)):
    ret, frame = cap.read()
    timestamps+=[str(time.time())]


    cv2.imshow('Camera',frame) 
    cv2.imwrite(f"{name}/{idx}.png",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

f = open(f"{name}/timestamps.txt","w")
f.write(",".join(timestamps))
f.close()