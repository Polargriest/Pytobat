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

		# All Event exceptions
		if self.desc == 'event.notfound':
			exception += f"[!] Event '{self.contents[0]}' does not exists."

		# All Bricks exceptions
		elif self.desc == 'brick.notfound':
			exception += f"[!] Brick '{self.contents[0]}' does not exists."

		elif self.desc == 'brick.args.mismatch':
			exception += f"[!] Brick '{self.contents[0]}' takes {self.contents[2]} "
			exception += "argument" if self.contents[2] == 1 else "arguments"
			exception += f" but {self.contents[1]} "
			exception += "was" if self.contents[1] == 1 else "were"
			exception += " given." 

		# Generic error
		else:
			message = "OOPS! OUR BAD!"
			exception = (
				f"--------------- [X] {message} ---------------\n"
				f"[?] At {self.where[0]} | Line {self.where[1]}\n"
				f"[!] We did not register that error. It's our fault!\n"
				 "    Please take a screenshot and send it to us, we'll try fixing it ASAP!\n\n"
				f" -> Error code: '{self.desc}'"
			)

		exception += "\n" + ("-" * (len(message) + 36)) + "\n"

		print(exception)
		exit()