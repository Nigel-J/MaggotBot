# USAGE
# python circle_boundary_tracking.py --color_circles.mp4
# python circle_boundary_tracking.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import paramiko
import time
 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('172.24.1.1', username='pi', password='raspberry')

def get_center(cnts):
	# find the largest contour in the mask, then use
	# it to compute the minimum enclosing circle and
	# centroid
	c = max(cnts, key=cv2.contourArea)
	((x, y), radius) = cv2.minEnclosingCircle(c)
	M = cv2.moments(c)
	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	# only proceed if the radius meets a minimum size
	if radius > 10:
		# draw the circle and centroid on the frame,
		# then update the list of tracked points
		cv2.circle(frame, (int(x), int(y)), int(radius),
			(0, 255, 255), 2)
		cv2.circle(frame, center, 5, (0, 0, 255), -1)
	return center, radius

def get_dist(objcenter, bndcenter):
	x = objcenter[0] - bndcenter[0]
	y = objcenter[1] - bndcenter[1]
	return np.sqrt(x*x + y*y)

def get_dir(objcenter, bndcenter):
	x = objcenter[0] - bndcenter[0]
	y = objcenter[1] - bndcenter[1]
	if x < 0 and y < 0:
		dir = "right down"
	elif x < 0 and y > 0:
		dir = "right up"
	elif x > 0 and y < 0:
		dir = "left down"
	else:
		dir = "left up"
	return dir

try:
	# main loop goes for duration of experiment time
	stdin, stdout, stderr = ssh.exec_command("sudo python test/threading_test.py")
	while True:

		move = 1
		lastdir = 'none'
		
		# construct the argument parse and parse the arguments
		ap = argparse.ArgumentParser()
		ap.add_argument("-v", "--video",
			help="path to the (optional) video file")
		ap.add_argument("-b", "--buffer", type=int, default=64,
			help="max buffer size")
		args = vars(ap.parse_args())

		# define the lower and upper boundaries of the colors
		# to track in the HSV color space, then initialize the
		# list of tracked points for moving object
		objLower = (77, 100, 100)
		objUpper = (97, 255, 255)
		pts = deque(maxlen=args["buffer"])

		bndLower = (0, 100, 100)
		bndUpper = (55, 255, 255)

		# if a video path was not supplied, grab the reference
		# to the webcam
		if not args.get("video", False):
			camera = cv2.VideoCapture(0)

		# otherwise, grab a reference to the video file
		else:
			camera = cv2.VideoCapture(args["video"])
	
		pts.clear()
	
		# run loop
		while True:
			# grab the current frame
			(grabbed, frame) = camera.read()

			# if we are viewing a video and we did not grab a frame,
			# then we have reached the end of the video
			if args.get("video") and not grabbed:
				break

			# resize the frame, blur it, and convert it to the HSV
			# color space
			frame = imutils.resize(frame, width=600)
			# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			# construct masks for the colors, then perform a series 
			# of dilations and erosions to remove any small
			# blobs left in the mask
			objmask = cv2.inRange(hsv, objLower, objUpper)
			objmask = cv2.erode(objmask, None, iterations=2)
			objmask = cv2.dilate(objmask, None, iterations=2)

			bndmask = cv2.inRange(hsv, bndLower, bndUpper)
			bndmask = cv2.erode(bndmask, None, iterations=2)
			bndmask = cv2.dilate(bndmask, None, iterations=2)

			# find contours in the mask and initialize the current
			# (x, y) center of the object and boundary
			objcnts = cv2.findContours(objmask.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
			objcenter = None

			bndcnts = cv2.findContours(bndmask.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
			bndcenter = None
	
		
			if move == 1:
				# tell robot to go
				print("Tell robot to start")
				stdin.write('"go"\n')
				stdin.flush()
				move = 2
				
			if move == 2:
				# only proceed if at least one contour was found
				if len(bndcnts) > 0 and len(objcnts) > 0:
					bndcenter, bndradius = get_center(bndcnts)
					objcenter, objradius = get_center(objcnts)
					r = get_dist(objcenter, bndcenter)
					# update the points queue
					pts.appendleft(objcenter)
					if r > bndradius:
						print("Object Outside!")
						stdin.write('"out"\n')
						stdin.flush()
						move = 3
			
			if move == 3:
				# only proceed if at least one contour was found
				if len(bndcnts) > 0 and len(objcnts) > 0:
					bndcenter, bndradius = get_center(bndcnts)
					objcenter, objradius = get_center(objcnts)
					r = get_dist(objcenter, bndcenter)
					thisdir = get_dir(objcenter, bndcenter)
					if r < 20.0:
						print(str(r) + " winner!")
						stdin.write('"go"\n')
						stdin.flush()
						break
					else:
						if lastdir != thisdir:
		 					if thisdir == 'right down': 
			 					stdin.write('"right"\n')
			 					stdin.flush()
			 				elif thisdir == 'right up': 
			 					stdin.write('"right"\n')
			 					stdin.flush()
			 				elif thisdir == 'left down': 
			 					stdin.write('"left"\n')
			 					stdin.flush()
			 				elif thisdir == 'left up': 
			 					stdin.write('"left"\n')
			 					stdin.flush()
					thisdir = lastdir
	
			# show the frame to our screen
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF

except KeyboardInterrupt:
	stdin.write('"quit"\n')
	stdin.flush()	
	

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()