from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5 import  QtCore, QtGui
import sys

# Create the window and set its size
application = QApplication([])
appWindow = QWidget()
grid = QGridLayout()
appWindow.setLayout(grid)
appWindow.setGeometry(100, 100, 600, 400)

# Create a label indicating the last feeding times
lastFeedingTimeHeaderLabel = QLabel('Last Feeding Time:')
grid.addWidget(lastFeedingTimeHeaderLabel, 0, 0)
lastFeedingTimeHeaderLabel.show()

# Create a button to pull up the video of the last meal
showLastVideoButton = QPushButton('Show Video of Last Meal')
def on_showLastVideo_clicked():
	alert = QMessageBox()
	alert.setText('You clicked the button')
	alert.exec_()
showLastVideoButton.clicked.connect(on_showLastVideo_clicked)
showLastVideoButton.show()
grid.addWidget(showLastVideoButton, 1, 0)

# Create a place to show a thumbnail of the last meal
lastMealImageLabel = QLabel()
lastMealImage = QtGui.QPixmap('TestImage.png')
lastMealImageLabel.setPixmap(lastMealImage)
#grid.addWidget(lastMealImageLabel, 0, 1)
#lastMealImageLabel.show()

# Create a place to show video of the last Meal
mediaPlayer = QMediaPlayer()
mediaPlaylist = QMediaPlaylist(mediaPlayer)
mediaPlaylist.addMedia(QMediaContent(QUrl.fromLocalFile('/Users/rafeyanwar/OneDrive/Documents/SMU Masters/EE 7390/code/python/AppGui/TrimmedVideo.mp4')))
mediaPlaylist.setPlaybackMode(QMediaPlaylist.Loop)
videoWidget = QVideoWidget()
mediaPlayer.setPlaylist(mediaPlaylist)
mediaPlayer.setVideoOutput(videoWidget)
mediaPlaylist.setCurrentIndex(0)
mediaPlayer.play()
videoWidget.show()
grid.addWidget(videoWidget, 1, 1, 2, 1)


appWindow.setWindowTitle('Biscuit Feeding Stats')
appWindow.show()
application.exec_()
