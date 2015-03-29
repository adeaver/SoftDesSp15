""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
kernel = np.ones((21,21),'uint8')

while(True):
	ret, frame = cap.read()
	faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
	for (x,y,w,h) in faces:
	    frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)
	    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
	    cv2.circle(frame, (x+w/3, y+h/3), 20, (0, 0, 255), -1)
	    cv2.circle(frame, (x+w/3, y+h/3), 5, (255, 255, 255), -1)
	    cv2.circle(frame, (x+2*w/3, y+h/3), 20, (0, 0, 255), -1)
	    cv2.circle(frame, (x+2*w/3, y+h/3), 5, (255, 255, 255), -1)
	    cv2.line(frame, (int(x+w/3), int(y+2*h/3)), (int(x+2*w/3), int(y+2*h/3+h/8)), (0, 0, 255), 10)
	 # Display the resulting frame
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()