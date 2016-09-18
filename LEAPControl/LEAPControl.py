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

	def command(self, cmd):
		pyautogui.hotkey(*cmd.split("-"))
		print(cmd)
		self.lastCommand = None
		self.lastCommandTime = time.time()

	def updateDelta(self, hull):
		#assume that for our case, the hull could be approximated
		#to a circle
		radius = sqrt(hull/pi)
		self.deltaThreshold = DELTA_THRESHOLD_COEFF * radius - DELTA_THRESHOLD_Y_INT
		print("\t\t\t\t\t", radius, self.deltaThreshold)

	def streamHandler(self, post):
		event = post["event"]
		key = post["path"]
		value = post["data"]

		if event == "put":
			if self.lastCommand == "fist" and \
				key == "/values/fist" and value and \
				(time.time() - self.lastCommandTime) < DOUBLE_COMMAND_TIME:
					self.command("ctrl-t")

			elif (time.time() - self.lastCommandTime) > COMMAND_TIME: #TODO: Check for double commands
				print(self.lastCommandTime, time.time())
				if key == "/":
					print("INFO: Initial data:", value)

				print(key+":\t", value, end="\t")

				if key == "/values/fist" and value:
					self.command("")
					self.lastCommand = "fist"

				elif key == "/values/deltaX":
					if self.swipingX:
						self.swipingX = False
					else:
						self.swipingX = True
						if value >  self.deltaThreshold:
							self.command("ctrl-tab")
						elif value < -self.deltaThreshold:
							self.command("ctrl-shift-tab")

				elif key == "/values/deltaY":
					if self.swipingY:
						self.swipingY = False
					else:
						self.swipingY = True
						if value >  self.deltaThreshold:
							self.command("ctrl-w")
						elif value < -self.deltaThreshold:
							self.command("ctrl-w")

				elif key == '/values/hullArea':
					self.updateDelta(value)

		else:
			print("WARN:", "Other event:", event)

LEAPCommand().start()