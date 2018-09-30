from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import sys
import cv2

print('Starting Program')

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	print('Using a video stream.')

else:
	vs = cv2.VideoCapture(args["video"])
	print('Using a video file.')

firstFrame = None
printedFrameSize = False

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = "Not Found"
	textR = 255
	textG = 0

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		break

	if not printedFrameSize:
		height, width = frame.shape[:2]
		print('Image width: ',width,"\t Image height: ",height)
		printedFrameSize = True

	# resize the frame, draw the target area
	frame = imutils.resize(frame, width=500)
	cv2.rectangle(frame, (150, 200), (210, 260), (255, 255, 255), 2)

	# greyscale and blur the frame
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

    # compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Found"
		textR = 0
		textG = 255

	# draw the text and timestamp on the frame
	cv2.putText(frame, "Biscuit Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, textG, textR), 2)

	# show the frame and record if the user presses a key
	cv2.imshow("Biscuit Cam", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
