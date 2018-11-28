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
	vs = VideoStream(src=1).start()
	time.sleep(2.0)
	print('Using a video stream.')

else:
	vs = cv2.VideoCapture(args["video"])
	print('Using a video file.')

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
writer = None

# loop over the frames of the video
while True:
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		break

	if writer is None:
		height, width = frame.shape[:2]
		print('creating writer')
		print('height: ', height, ' width: ', width)
		writer = writer = cv2.VideoWriter('test2.mp4', fourcc, 20, (width, height))

	writer.write(frame)

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
print('releasing writer')
writer.release()
cv2.destroyAllWindows()
