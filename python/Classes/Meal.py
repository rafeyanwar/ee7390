import uuid

class Meal:

	# If no guid is provided (i.e. we are not reading from a log), create one
	def __init__(self, timestamp, guid=None):
		if guid is None:
			guid = str(uuid.uuid4())[:8]
		self.timestamp = timestamp
		self.guid = guid

	def getThumbnailFileName(self):
		return "{0}.jpeg".format(self.guid)

	def getVideoFileName(self):
		return "{0}.mp4".format(self.guid)
