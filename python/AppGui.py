from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5 import  QtCore, QtGui
import sys
from Classes.MealLog import MealLog
from Classes.Meal import Meal

# Create the window and set its size
application = QApplication([])
appWindow = QWidget()
grid = QGridLayout()
appWindow.setLayout(grid)
appWindow.setGeometry(100, 100, 600, 600)

# Create a place to show a thumbnail of the last meal
lastMealImageLabel = QLabel()
#lastMealImage = None#QtGui.QPixmap('TestImage.jpeg')
lastMealImageLabel.setScaledContents(True)
#lastMealImageLabel.setPixmap(lastMealImage)
grid.addWidget(lastMealImageLabel, 0, 1)
lastMealImageLabel.show()

# Create a place to show video of the last Meal
mediaPlayer = QMediaPlayer()
mediaPlaylist = QMediaPlaylist(mediaPlayer)
videoWidget = QVideoWidget()
mediaPlayer.setPlaylist(mediaPlaylist)
mediaPlayer.setVideoOutput(videoWidget)
videoWidget.show()
grid.addWidget(videoWidget, 1, 1, 2, 1)

# Create a button to pull up the video of the last meal
mealLog = MealLog("log.txt")
mealSelector = QComboBox()
mealSelector.addItems(mealLog.getMeals())
def mealSelected(selectedMeal):
	meal = mealLog.getMeal(selectedMeal)
	mediaPlaylist.clear()
	videoFilePath = QFileInfo("MealVideos/{0}".format(meal.getVideoFileName())).absoluteFilePath()
	mediaPlaylist.addMedia(QMediaContent(QUrl.fromLocalFile(videoFilePath)))
	mediaPlaylist.setPlaybackMode(QMediaPlaylist.Loop)
	mediaPlaylist.setCurrentIndex(0)
	mediaPlayer.play()
	lastMealImage = QtGui.QPixmap("MealImages/{0}".format(meal.getThumbnailFileName()))
	lastMealImageLabel.setPixmap(lastMealImage)
mealSelector.activated[str].connect(mealSelected)
grid.addWidget(mealSelector, 1, 0)

# Create a label indicating the last feeding times
refreshButton = QPushButton('Refresh')
def on_refreshButton_clicked():
	mealLog = MealLog("log.txt")
	mealSelector = QComboBox()
	mealSelector.addItems(mealLog.getMeals())
refreshButton.clicked.connect(on_refreshButton_clicked)
grid.addWidget(refreshButton, 0, 0)
refreshButton.show()

appWindow.setWindowTitle('Biscuit Meals')
appWindow.show()
application.exec_()
