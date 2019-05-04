import subprocess, time
from lib.GPIOSetup import GPIO
from lib.setup import settings

class Appliance:

	def __init__(self, attributes):
		self.attributes = attributes
		self.name = attributes['Name']
		self.type = attributes['Type']
		if self.type == 'GPIO':
			self.pin = attributes['Pin']
			self.active = attributes['ActiveState']
		if self.type == 'Script':
			if 'Timeout' in attributes:
				self.timeout = "timeout "+str(attributes['Timeout'])+" "
			else:
				self.timeout = "timeout 0.2 "
			self.status_cmd = self.timeout + attributes['Status']
			if 'Action' in attributes:
				self.action = True
				self.on_cmd = attributes['Action'][True]
				self.off_cmd = attributes['Action'][False]
			else:
				self.action = False

	def getState(self):
		if self.type == 'GPIO':
			if GPIO.input(self.pin) is self.active:
				return 1
			else:
				return 0
		else:
			#get the state of other Appliances in other rooms
			#not properly implemented yet
			returnCode = subprocess.call([self.status_cmd], shell=True)
			if returnCode == 0:
				return 1
			return 0

	def setState(self, state):
		if self.type == 'GPIO':
			if state > 1:
				original_state= GPIO.input(self.pin)
				new_state = 1 - original_state
			else:
				new_state = 1 - self.active - state
			GPIO.output(self.pin, new_state)
			if GPIO.input(self.pin) is self.active:
				return 1
			else:
				return 0

	def executeAction(self):
		if self.type == 'GPIO':
			original_state= GPIO.input(self.pin)
			new_state = 1 - original_state
			GPIO.output(self.pin, new_state)
			if 'Duration' in self.attributes:
				time.sleep(self.attributes['Duration'])
				GPIO.output(self.pin, original_state)
			if 'Off' in self.attributes:
				time.sleep(self.attributes['Off'])
				GPIO.output(self.pin, 0)
			if 'On' in self.attributes:
				time.sleep(self.attributes['On'])
				GPIO.output(self.pin, 1)
		if self.type == 'Script' and self.action:
			if self.getState():
				subprocess.call([self.off_cmd], shell=True)
			else:
				subprocess.call([self.on_cmd], shell=True)