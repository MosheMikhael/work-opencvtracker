# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 12:00:08 2018

@author: moshe.f
"""

import cv2
def click_and_crop(event, x, y, flags, param):
	global bb_pts
	if event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		bb_pts.append((x, y))
        
cam = cv2.VideoCapture(0)
#                       0      1     2      3          4           5        6        7
tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
#                   < 20      <20   30+    <10      >220                  >300      <18
tracker_type = tracker_types[6]

if tracker_type == 'BOOSTING':
    tracker = cv2.TrackerBoosting_create()
if tracker_type == 'MIL':
    tracker = cv2.TrackerMIL_create()
if tracker_type == 'KCF':
    tracker = cv2.TrackerKCF_create()
if tracker_type == 'TLD':
    tracker = cv2.TrackerTLD_create()
if tracker_type == 'MEDIANFLOW':
    tracker = cv2.TrackerMedianFlow_create()
if tracker_type == 'GOTURN':
    tracker = cv2.TrackerGOTURN_create()
if tracker_type == 'MOSSE':
    tracker = cv2.TrackerMOSSE_create()
if tracker_type == "CSRT":
    tracker = cv2.TrackerCSRT_create()

#bbox = []
#cv2.namedWindow("choose")
#cv2.setMouseCallback("choose", click_and_crop)
#ok = True
#while ok:
ok, frame = cam.read()
bbox = cv2.selectROI(frame, False)
ok = tracker.init(frame, bbox)
    
  
while True:
    ok, frame = cam.read()
    if not ok:
        break
        # Start timer
    timer = cv2.getTickCount()
 
    # Update tracker
    ok, bbox = tracker.update(frame)
 
    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    else :
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
    # Display tracker type on frame
    cv2.putText(frame, tracker_type, (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
 
    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
    # Display result
    cv2.imshow("Tracking", frame)
  
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
cam.release()
cv2.destroyAllWindows()
