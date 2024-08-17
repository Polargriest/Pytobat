import random
import math

phi = (1 + math.sqrt(5)) / 2

class PtbException:

	goofyAhhMessages = [
		"ERM, WHAT THE SIGMA",
		"AIN'T NO WAY YOU DID THAT",
		"BRUH IS NOT THAT HARD",
		"CHAT CLIP THIS",
		"FIX YOUR GAME"
	]

	def __init__(self, type, where, contents, desc):
		self.type = type
		self.where = where
		self.contents = contents
		self.desc = desc

		if type == 'e':
			self.exception()

	def exception(self):
		if random.random() < phi/100:
			message = random.choice(self.goofyAhhMessages)
		else:
			message = "PYTOBAT FATAL ERROR"

		exception = (
			f"--------------- [X] {message} ---------------\n"
			f"[?] At {self.where[0]} | Line {self.where[1]}\n" )

		if self.desc == 'event.notfound':
			exception += f"[!] Event '{self.contents[0]}' does not exists."

		exception += "\n" + ("-" * (len(message) + 36)) + "\n"

		print(exception)
		exit()