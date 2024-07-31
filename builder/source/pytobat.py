from pathlib import Path
import shutil
import os
import uuid
import re
import random
import math

class Interpreter:
	# Reserved words ------------------------------------------------------
	KEYWORDS = ["event", "pass"]
	EVENTS = {
		"WHEN_SCENE_STARTS": "StartScript",
		"WHEN_TAPPED": "WhenScript",
		"WHEN_STAGE_IS_TAPPED": "WhenTouchDownScript"
	}
	FUNCTIONS = {
		# Looks bricks
		"hide": { "args": 0, "type" : "HideBrick"},
		"show": { "args": 0, "type": "ShowBrick" },
		"nextLook": { "args": 0, "type": "NextLookBrick" },
		"previousLook": { "args": 0, "type": "PreviousLookBrick" }
	}
	queue = []

	def __init__(self):
		pass

	def openEvent(self, event):
		result =     f"""						<script type="{self.EVENTS[event]}" posX="0.0" posY="0.0">\n"""
		result +=    f"""							<brickList>\n"""
		queuePush =  f"""							</brickList>\n"""
		queuePush += f"""							<commentedOut>false</commentedOut>\n"""
		queuePush += f"""							<scriptId>{uuid.uuid4()}</scriptId>\n"""
		queuePush += f"""						</script>\n"""
		self.queue.append(queuePush)
		return result

	def createBrick(self, function, args):
		result =  f"""								<brick type="{self.FUNCTIONS[function]["type"]}" posX="0.0" posY="0.0">\n"""
		result += f"""									<brickId>{uuid.uuid4()}</brickId>\n"""
		result += f"""									<commentedOut>false</commentedOut>\n"""
		result += f"""								</brick>\n"""
		return result

	def interprete(self, scriptRef):
		# INTERPRETE CODE HERE --------------------------------------------

		# Variables we need
		xml = "" # We store all the code here
		lines = [] # We store all the individual of the script lines here
		contextStack = [] # We store all the current contexts of the program
		currentLine = 0 # Current line reading

		xml += "					<scriptList>\n"

		# Opens the script and split it all in lines
		with open(scriptRef) as script:
			lines = script.read().splitlines()

		# We start looking every line
		for line in lines:
			currentLine += 1

			# Interpreter ignores ----------------------
			if line.strip('\t').startswith('#'): # Comments
				continue

			if line == "": # Blank line
				continue

			# Get the context --------------------------
			context = self.getContext(line)

			if context > len(contextStack): # If there are more indents than context, throw error
				Console("error", [scriptRef, currentLine], [], "syntax.indent.unexpected")
			elif context < len(contextStack): # If there are more contexts than indents, pop contexts
				while context < len(contextStack):
					xml = xml + self.queue[0]
					self.queue.pop()
					contextStack.pop()


			# Remove indent from line and tokenize
			line = line.strip('\t')
			tokens = line.split()

			# Keyword handler -------------------------
			if tokens[0] in self.KEYWORDS:
				# Event keyword handler
				if tokens[0] == "event":
					# Event validations
					try:
						event = re.search(r'^\w+', tokens[1]).group()
					except IndexError as e: # If user just wrote 'event' without elaborating
						Console("error", [scriptRef, currentLine], [], "syntax.eventkw.none")
					except AttributeError as e: # If user wrote invalid event
						Console("error", [scriptRef, currentLine], [], "syntax.eventkw.invalid")

					if "event" in contextStack: # Not an event paradox
						Console("error", [scriptRef, currentLine], [], "event.paradox")

					if not event in self.EVENTS: # Does event exists?
						Console("error", [scriptRef, currentLine], [event], "event.notfound")

					# Event behaviour
					contextStack.append("event")
					xml += self.openEvent(event)
				
				# Pass keyword handler
				if tokens[0] == "pass":
					# Pass validations
					if len(contextStack) == 0:
						Console("error", [scriptRef, currentLine], [], "pass.nothing")

				continue

			# Function handler ------------------------
			elif self.validateFunction(line):
				name = self.validateFunction(line)
				args = self.validateFunction(line, False)

				# Function validations
				if not "event" in contextStack: # Function must be inside an event
					Console("error", [scriptRef, currentLine], [name], "function.context.outside")
				
				if not name in self.FUNCTIONS: # Check if function exists
					Console("error", [scriptRef, currentLine], [name], "function.notfound")

				if len(args) != self.FUNCTIONS[name]["args"]: # Check if number of arguments is ok
					Console("error", [scriptRef, currentLine], [name, self.FUNCTIONS[name]["args"], len(args)], "function.args.incorrect")

				# Function behaviour
				xml += self.createBrick(name, args)

				continue

		# -----------------------------------------------------------------

		for waiter in self.queue:
			xml = self.mergeXMLtags(xml, waiter)

		xml += "					</scriptList>\n" # Finish scriptList
		return "					<scriptList/>\n" if xml == "					<scriptList>\n					</scriptList>\n" else xml

	def mergeXMLtags(self, xml1, xml2):
		lastLine  = re.search(r'(?<=[\/<])\w+', xml1.splitlines()[-1].lstrip('\t')).group()
		firstLine = re.search(r'(?<=[\/<])\w+', xml2.splitlines()[0].lstrip('\t')).group()
			
		if lastLine == firstLine:
			print("is ture")
			# Quitar la última línea del xml
			strippedLine = xml1.splitlines()
			xml1 = "\n".join(strippedLine[:-1])

			# Quitar la primera línea del waiter
			strippedLine = xml2.splitlines()
			xml2 = "\n".join(strippedLine[1:])
			
			# Escribir la etiqueta abiecerrada
			return xml1 + f"\n							<{firstLine}/>\n" + xml2 + "\n"
		else:
			return xml1 + xml2

	def validateFunction(self, string, getName=True):
		# Check if is a function
		function = re.search(r'\w+(?=\()', string)

		if function: # Is a function!
			if getName:
				return function.group() # Return only the name if wanted
			else:
				arguments = re.search(r'(?<=\().+?(?=\))', string)
				return arguments.group().split(', ') if arguments else [] # Return the function's arguments
		else:
			return False

	def getContext(self, string):
		# This functions return the context of the current string
		count = 0
		for char in string:
			if (char == '\t'):
				count += 1
			else:
				return count

class Object:
	def __init__(self, name, script, looks, audios):
		self.name = name
		self.script = script
		self.looks = looks
		self.audios = audios

	def getCode(self):
		code = "\n"
		code += f"				<object type=\"Sprite\" name=\"{self.name}\">\n"

		# Buscar apariencias -----------------------------------------
		if len(os.listdir(self.looks)) > 0:
			code += "					<lookList>\n"

			looksArray = [look for look in self.looks.iterdir()]

			for look in looksArray:
				code += f"""						<look fileName=\"{look.name}\" name=\"{look.stem}\">
							<isWebRequest>false</isWebRequest>
							<valid>true</valid>
						</look>
				"""

			code += "	</lookList>\n"
		else:
			code += "					<lookList/>\n"

		# Buscar audios ----------------------------------------------
		if len(os.listdir(self.audios)) > 0:
			code += "					<soundList>\n"

			aduiosArray = [audio for audio in self.audios.iterdir()]

			for audio in aduiosArray:
				code += f"""						<sound fileName=\"{audio.name}\" name=\"{audio.stem}\">
							<midiFile>false</midiFile>
						</sound>
				"""

			code += "	</soundList>\n"
		else:
			code += "					<soundList/>\n"

		# Buscar scripts ---------------------------------------------
		if self.script:
			objScripts = Interpreter()
			interpretated = objScripts.interprete(self.script)
			code += interpretated
		else:
			code += "					<scriptList/>\n"

		code += """					<nfcTagList/>
					<userVariables/>
					<userLists/>
					<userDefinedBrickList/>
				</object>"""
		return code