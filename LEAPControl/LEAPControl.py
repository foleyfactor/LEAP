import pyrebase
import pyautogui
import time
from math import sqrt, pi

PERCENTAGE_FOR_MOVEMENT = 0.7 #percentage of radius of the hull that needs to be moved for a "swipe" to be registered
DOUBLE_COMMAND_TIME = 1.0 # in seconds
COMMAND_TIME = 0.5 # in seconds

class LEAPCommand:
	def __init__(self):
		self.config = {
			"apiKey": "AIzaSyApQZxKcrOJ2L4Tw-FtXADaYO5i9EM47MM",
			"authDomain": "https://leap-5edd0.firebaseapp.com",
			"databaseURL": "https://leap-5edd0.firebaseio.com",
			"storageBucket": "leap-5edd0.appspot.com"
		}

		self.firebase = pyrebase.initialize_app(self.config)

		self.db = self.firebase.database()

		self.lastCommand = None # double commands
		self.lastCommandTime = 0
		self.swipingX = False
		self.swipingY = False
		self.DELTA_THRESHOLD = 500

	def start(self):
		self.stream = self.db.stream(self.streamHandler)

	def command(self, cmd):
		pyautogui.hotkey(*cmd.split("-"))
		print(cmd)
		self.lastCommand = cmd
		self.lastCommandTime = time.time()

	def updateDelta(self, hull):
		#assume that for our case, the hull could be approximated
		#to a circle
		radius = sqrt(hull/pi)
		self.DELTA_THRESHOLD = PERCENTAGE_FOR_MOVEMENT*radius


	def streamHandler(self, post):

		event = post["event"]
		key = post["path"]
		value = post["data"]

		if event == "put":
			if (time.time() - self.lastCommandTime) < COMMAND_TIME:
				if 				

			else:
				print(self.lastCommandTime, time.time())
				if key == "/":
					print("INFO: Initial data:", value)

				print(key+":\t", value, end="\t")

				if key == "/values/fist":
					if value:
						self.command("ctrl-t")

				elif key == "/values/deltaX":
					if self.swipingX:
						self.swipingX = False
					else:
						self.swipingX = True
						if value >  self.DELTA_THRESHOLD:
							self.command("ctrl-tab")
						elif value < -self.DELTA_THRESHOLD:
							self.command("ctrl-shift-tab")

				elif key == "/values/deltaY":
					if self.swipingY:
						self.swipingY = False
					else:
						self.swipingY = True
						if value >  self.DELTA_THRESHOLD:
							self.command("ctrl-w")
						elif value < -self.DELTA_THRESHOLD:
							self.command("ctrl-w")

				elif key == '/values/hullArea':
					self.updateDelta(value)


		else:
			print("WARN:", "Other event:", event)

LEAPCommand().start()