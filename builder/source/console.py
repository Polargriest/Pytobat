class PtbException:
	def __init__(self, _type, at, contents, desc):
		self.type = _type
		self.at = at
		self.contents = contents
		self.desc = desc
		if _type == "error":
			self.ptbLanguageException()

	def ptbLanguageException(self):
		# Header
		if random.random() < (1 + math.sqrt(5)) / 200:
			messages = ["ERM, WHAT THE SIMGA", "HELL NAH", "INFORM THE NEAREST ADULT", "CHAT CLIP THIS"]
			message = random.choice(messages)
		else:
			message = "PYTOBAT FATAL ERROR"

		error =  f"--------------- [X] {message} ---------------\n"
		error += f"[?] At {self.at[0]} | Line {self.at[1]}\n"

		# All Syntax Exceptions
		if self.desc == "syntax.indent.unexpected":
			error += f"[!] Unexpected indent.\n"

		elif self.desc == "syntax.eventkw.none":
			error += f"[!] Expected an event after \'event\'.\n"

		elif self.desc == "syntax.eventkw.invalid":
			error += f"[!] Invalid event after keyword \'event\'.\n"
		
		# All Event Exceptions
		elif self.desc == "event.notfound":
			error += f"[!] Event \'{self.contents[0]}\' does not exists.\n"
		
		elif self.desc == "event.paradox":
			error += f"[!] Tried to put an event inside an event.\n"

		# All Pass Exceptions
		elif self.desc == "pass.nothing":
			error += f"[!] No context to pass.\n"

		# All Function Exceptions
		elif self.desc == "function.notfound":
			error += f"[!] Function \'{self.contents[0]}\' does not exists.\n"

		elif self.desc == "function.context.outside":
			error += f"[!] All functions must be within events.\n"

		elif self.desc == "function.args.incorrect":
			error += f"[!] Function \'{self.contents[0]}\' needs {self.contents[1]} "
			error +=  "argument" if self.contents[1] == 1 else "arguments"
			error += f" but {self.contents[2]} "
			error += "was given.\n" if self.contents[2] == 1 else "were given.\n"

		# Generic Exception
		else:
			error += f"[!] An error was detected, but we didn't handle it!\n"
			error +=  "    It's our bad! Please send us the following error code so we can start fixing this!\n"
			error += f"    Error code: \'{self.desc}\'\n"

		# Footer
		error += "-" * (len(message) + 36) + "\n"
		print(error)
		exit()

class BuilderException:
	def __init__(self, _type, contents, desc):
		self.type = _type
		self.contents = contents
		self.desc = desc
		if _type == "error":
			self.buildException()

	def buildException(self):
		error =  f"############### [X] PTB BUILDER ERROR ###############\n"
		error += f"[?] Something messed up in the builder.\n"

		if self.desc == "path.invalid":
			error += f"[!] The path \'{self.contents[0]}\' is not valid."

		error +=  f"\n#####################################################\n"
		print(error)
		exit()