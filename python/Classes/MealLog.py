from .Meal import Meal
import csv

class MealLog:

	def __init__(self, fileName):
		self.fileName = fileName
		self.loggedMeals = []
		try:
			with open(self.fileName) as mealLogFile:
				csvReader = csv.reader(mealLogFile, delimiter=',')
				for row in csvReader:
					self.loggedMeals.append(Meal(row[0], row[1]))
		except IOError:
			mealLogFile = open(self.fileName, "w")
			mealLogFile.close()

	def getMeals(self):
		meals = []
		for meal in self.loggedMeals:
			meals.append(meal.timestamp)
		return meals

	def getMeal(self, timestamp):
		mealToReturn = None
		for meal in self.loggedMeals:
			if meal.timestamp == timestamp:
				mealToReturn = meal
		return mealToReturn

	def addMeal(self, meal):
		if len(self.loggedMeals) == 10:
			self.loggedMeals.pop(0)
		self.loggedMeals.append(meal)

	def writeToFile(self):
		with open(self.fileName, "w") as mealLogFile:
			csvWriter = csv.writer(mealLogFile, delimiter=',')
			for meal in self.loggedMeals:
				csvWriter.writerow([meal.timestamp, meal.guid])
