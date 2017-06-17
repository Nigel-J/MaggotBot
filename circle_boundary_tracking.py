# USAGE
# python circle_boundary_tracking.py --color_circles.mp4
# python circle_boundary_tracking.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

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
		dir = "Go right and down"
	elif x < 0 and y > 0:
		dir = "Go right and up"
	elif x > 0 and y < 0:
		dir = "Go left and down"
	else:
		dir = "Go left and up"
	return dir

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

# keep looping
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

	# only proceed if at least one contour was found
	if len(bndcnts) > 0 and len(objcnts) > 0:
		bndcenter, bndradius = get_center(bndcnts)
		objcenter, objradius = get_center(objcnts)
		r = get_dist(objcenter, bndcenter)
		print(str(r) +" "+ str(bndradius))
		if r > bndradius:
			print("Object Outside!")
			break

	# update the points queue
	pts.appendleft(objcenter)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

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
	
	# only proceed if at least one contour was found
	if len(bndcnts) > 0 and len(objcnts) > 0:
		bndcenter, bndradius = get_center(bndcnts)
		objcenter, objradius = get_center(objcnts)
		r = get_dist(objcenter, bndcenter)
		if r < 20.0:
			print(str(r) + " winner!")
			break
		else:
			print(get_dir(objcenter, bndcenter))	
	
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
	

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()