#!/usr/bin/env python3

import pyrebase
import pyautogui
import time
from math import sqrt, pi

DELTA_THRESHOLD_COEFF = 2
DELTA_THRESHOLD_Y_INT = 62.3
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
		self.deltaThreshold = 500

	def start(self):
		self.stream = self.db.stream(self.streamHandler)

	def press(self, key):
		pyautogui.press(key)
		print(key)
		self.lastCommand = None
		self.lastCommandTime = time.time()

	def streamHandler(self, post):
		event = post["event"]
		key = post["path"]
		value = post["data"]

		if event == "put":
			if (time.time() - self.lastCommandTime) > COMMAND_TIME: #TODO: Check for double commands
				if key == "/":
					print("INFO: Initial data:", value)

				if key == "/values/fist" and value:
					self.press("p")

				elif key == "/values/direction":
					if value == 1:
						self.press("up")
					elif value == 2:
						self.press("right")
					elif value == 3:
						self.press("down")
					elif value == 4:
						self.press("left")

		else:
			print("WARN:", "Other event:", event)

LEAPCommand().start()