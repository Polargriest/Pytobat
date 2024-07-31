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

class Console:
	def __init__(self, _type, at, contents, desc):
		self.type = _type
		self.at = at
		self.contents = contents
		self.desc = desc
		if _type == "error":
			self.fatalError()

	def fatalError(self):
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
		

class Pytobat:
	header = {
		"applicationBuildName": "",
		"applicationBuildNumber": 0,
		"applicationBuildType": "signedRelease",
		"applicationName": "Pocket Code",
		"applicationVersion": "1.2.4",
		"catrobatLanguageVersion": "1.11",
		"dateTimeUpload": "",
		"description": "",
		"deviceName": "ZTE A7030",
		"isCastProject": "false",
		"landscapeMode": "false",
		"listeningLanguageTag": "",
		"mediaLicense": "",
		"notesAndCredits": "",
		"platform": "Android",
		"platformVersion": 30,
		"programLicense": "",
		"programName": "Pytocat",
		"remixOf": "",
		"scenesEnabled": "true",
		"screenHeight": 720,
		"screenMode": "STRETCH",
		"screenWidth": 1473,
		"tags": "",
		"url": "",
		"userHandle": ""
	}

	scenes = []

	def __init__(self, programName):
		self.header["programName"] = programName
		self.programName = programName

	def build(self, toCatrobat=True):
		code = "" # Crear XML vacío

		code += "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>\n"
		code += "<program>\n" # Abrir programa

		# Crear header ---------------------------------------------
		code += "	<header>\n"

		for key in self.header:
			value = str(self.header[key])
			code += f"		<{key}>{value}</{key}>\n"

		code += "	</header>\n"

		# Crear los settings ---------------------------------------
		code += "	<settings/>\n"

		# Crear la carpeta del proyecto ----------------------------
		directorio = Path(self.programName)
		directorio.mkdir(exist_ok=True)

		# Buscar cuántas escenas tiene el proyecto -----------------
		code += "	<scenes>\n"
		game = Path("Game/scenes")
		self.scenes = [scene for scene in game.iterdir() if scene.is_dir()]

		for scene in self.scenes:
			code += "		<scene>\n"
			code += f"			<name>{scene.name}</name>\n"
			code += "			<objectList>"

			# Comprobar si la escena tiene objeto bg (Background)
			if 'bg' in os.listdir(scene):
				bgPath = scene / 'bg'
				bg = Object("Background", None, bgPath/'looks', bgPath/'audios')
				code += bg.getCode()
			else: # Crear un fondo vacío
				bg = Object("Background", None, None, None)
				code += bg.getCode()

			# Buscar otros objetos en la escena
			objs = os.listdir(scene)
			objs.remove('bg')

			for obj in objs:
				newObject = Object(obj, scene/obj/'script.ptb', scene/obj/'looks', scene/obj/'audios')
				code += newObject.getCode()

			#Crear los directorios de la escena directorio
			directorio = directorio / scene.name
			directorio.mkdir(exist_ok=True) # Directorio de la escena

			directorio = directorio / 'images'
			directorio.mkdir(exist_ok=True) # Directorio de imagenes
			nomedia = directorio / '.nomedia'
			nomedia.write_text('')

			directorio = directorio.parent
			directorio = directorio / 'sounds'
			directorio.mkdir(exist_ok=True) # Directorio de audios
			nomedia = directorio / '.nomedia'
			nomedia.write_text('')

			# Buscar imágenes y audios en el fondo
			game = game / scene.name
			directorio = directorio.parent
			for obj in game.iterdir():
				# Buscar imagenes
				for look in (obj / 'looks').iterdir():
					shutil.copy(look, directorio / 'images')

				for audio in (obj / 'audios').iterdir():
					shutil.copy(audio, directorio / 'sounds')

			directorio = directorio.parent

			code += "\n			</objectList>\n"
			code += "		</scene>\n"

		# Fin de las escenas
		code += "	</scenes>\n"

		# Variables del programa -----------------------------------
		code += "	<programVariableList/>\n"
		code += "	<programListOfLists/>\n"
		code += "	<programMultiplayerVariableList/>\n"

		code += "</program>" # Cerrar programa

		# Crear el archivo XML dentro
		xml_dir = Path(self.programName)
		xml_dir = xml_dir / 'code.xml'
		xml_dir.write_text(code)

		# Comprimir la carpeta y hacerla .catrobat
		if toCatrobat:
			shutil.make_archive(self.programName, 'zip', self.programName)
			os.rename(f"{self.programName}.zip", f"{self.programName}.catrobat")