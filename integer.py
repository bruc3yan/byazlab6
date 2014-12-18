class Integer(object):
	def __init__(self, name):
		self.name = name
		self.value = 0
		self.lock = None
		self.owner = None
		self.last_modified = None #might not be needed
		self.last_server = None #might not be needed

	def set(self, value):
		try:
			new_value = int(value)
			self.value = value
		except StandardError:
			print "Value should be an integer."
		return self.value

	def get(self):
		return self.value



