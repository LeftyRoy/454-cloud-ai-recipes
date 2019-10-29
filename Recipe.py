class Recipe(object):
	def __init__(self, data):
		self.__dict__ = data

	def getDict(self):
		return self.__dict__
