from imutils.video import VideoStream
from Classes.Meal import Meal
from Classes.MealLog import MealLog
import argparse
import datetime
import imutils
import time
import sys
import cv2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders

# Function for emailing meal time and image
def sendEmail(meal):
	senderEmail = 'bisccam7390@gmail.com'
	senderPassword = 'h3ll0world'
	recipientEmail = 'rafeyanwar94@gmail.com'

	subject = "Biscuit has eaten at {0}".format(meal.timestamp)

	msg = MIMEMultipart()
	msg['From'] = senderEmail
	msg['To'] = recipientEmail
	msg['Subject'] = subject

	thumbnailFile = "MealImages/{0}".format(meal.getThumbnailFileName())
	attachment  = open(thumbnailFile, 'rb')
	part = MIMEBase('application','octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition',"attachment; filename= " + thumbnailFile)
	msg.attach(part)
	text = msg.as_string()
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(senderEmail,senderPassword)

	server.sendmail(senderEmail,recipientEmail,text)
	server.quit()

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
	# Option of using a video file for development
	vs = cv2.VideoCapture(args["video"])
	print('Using a video file.')

# Flag for showing motion detection during development
# During normal operation, set to False
showProcessing = True

# Parse meal log
mealLog = MealLog("log.txt")

firstFrame = None
printedFrameSize = False

# The subsection of the image near the feeder to look for motion
xLower = 150
xUpper = 200
yLower = 210
yUpper = 260

# Parameters to tweak sensitivity of detector
numFramesBiscuitDetected = 0
fps = 30
numSecondsDetectionRequired = 10
numFramesDetectionRequired = fps * numSecondsDetectionRequired

# Mp4 writer options
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = None

frameSaved = False

# Main loop to process each frame
while True:
	# Take the next frame
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]

	# Reset image text
	if showProcessing:
		text = "Not Found"
		textR = 255
		textG = 0

	# Break if video is finished
	if frame is None:
		break

	# Print the frame size initially as FYI
	if not printedFrameSize:
		height, width = frame.shape[:2]
		print('Image width: ',width,"\t Image height: ",height)
		printedFrameSize = True

	# Resize the frame for quicker processing and draw the target area
	frame = imutils.resize(frame, width=500)
	height, width = frame.shape[:2]
	cv2.rectangle(frame, (xLower, xUpper), (yLower, yUpper), (255, 255, 255), 2)

	# Get relevant section of image, greyscale and blur it
	feederSection = frame[yLower:yUpper, xLower:xUpper]
	gray = cv2.cvtColor(feederSection, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	if showProcessing:
		cv2.imshow("feedersection", feederSection)

	# Set the first/reference frame
	if firstFrame is None:
		firstFrame = gray
		continue

    # Compute delta between current frame and reference frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# Dilate the thresholded image and find contours
	thresh = cv2.dilate(thresh, None, iterations=2)
	contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = contours[0] if imutils.is_cv2() else contours[1]

	# Check if biscuit was found
	biscuitFound = False
	for c in contours:
		if cv2.contourArea(c) < args["min_area"]:
			# The contour is too small. Either motion is not detected or is no longer detectedself.
			# Reset everything, saving the video in the latter case.
			numFramesBiscuitDetected = 0
			frameSaved = False
			if writer is not None:
				print('Closing and saving video.')
				writer.release()
				writer = None
			continue
		else:
			biscuitFound = True

	if biscuitFound:
		numFramesBiscuitDetected = numFramesBiscuitDetected + 1
		if numFramesBiscuitDetected > numFramesDetectionRequired:
			if not frameSaved:
				# First frame that biscuit was detected
				# Save the thumbnail and update the log
				thisMeal = Meal(datetime.datetime.now().strftime("%m-%d-%y_%I:%M%p"))
				print('Biscuit detected, saving thumbnail.')
				cv2.imwrite("MealImages/{0}".format(thisMeal.getThumbnailFileName()), frame)
				frameSaved = True
				mealLog.addMeal(thisMeal)
				mealLog.writeToFile()
				sendEmail(thisMeal)
			if writer is None:
				writer = cv2.VideoWriter("MealVideos/{0}".format(thisMeal.getVideoFileName()), fourcc, 30, (width, height), True)
			writer.write(frame)

		if showProcessing:
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x + xLower, y + yLower), (x + w + xLower, y + h + yLower), (0, 255, 0), 2)
			cv2.putText(frame, "x: {} y: {}".format(x + xLower, y + yLower), (x + xLower, y + yLower),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, textG, textR), 1)
			cv2.putText(frame, "x: {} y: {}".format(x + w + xLower, y + h + yLower), (x + w + xLower, y + h + yLower),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, textG, textR), 1)
			text = "Found"
			textR = 0
			textG = 255

	if showProcessing:
		# Draw what the detector is seeing
		cv2.putText(frame, "Biscuit Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, textG, textR), 2)
		cv2.imshow("Biscuit Cam", frame)
		#cv2.imshow("Thresh", thresh)
		#cv2.imshow("Frame Delta", frameDelta)

	# Exit loop if user types 'q'
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

# Shutdown the processor
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
