import os
from pathlib import Path
from . import bldExceptions
from .interpreter import interpreter as ptbint

def isvalid(path, exception=True):
		# This function is used to validate a certain path the user provided.
		# Returns the path is valid, otherwise throws path.invalid.

		path = Path(path)

		if path.exists() and path.is_dir():
			return path
		else:
			if exception:
				raise bldExceptions.BuilderException("error", [path], "path.invalid")
			else:
				return None

class Scene:
	objects = []

	def __init__(self, path):
		self.path = path
		self.name = path.name

	def getCode(self):
		code =   "\t\t<scene>\n" # The start of a scene
		code += f"\t\t\t<name>{self.path.name}</name>\n" # Name of the scene
		code +=  "\t\t\t<objectList>\n" # The start of the object list

		# Get the object list ------------------------------------------------------
		objects = [obj for obj in self.path.iterdir()]

		# First of all, get the background
		code += Object(self.path / 'bg').getCode()
		if 'bg' in os.listdir(self.path):
			objects.remove(self.path / 'bg')
		
		# Then we create all the other objects
		for obj in objects:
			newobj = Object(obj)
			self.objects.append(newobj)
			code += newobj.getCode()

		# End the scene ------------------------------------------------------------
		code +=  "\t\t\t</objectList>\n" # The end of the object list
		code += "\t\t</scene>\n" #The end of an scene
		return code

	def getLooks(self):
		looks = []
		for obj in self.objects:
			looks += obj.getLooks()

		return looks

	def getAudios(self):
		audios = []
		for obj in self.objects:
			audios += obj.getAudios()

		return audios

class Object:
	lookslist = []
	audioslist = []

	def __init__(self, path):
		self.path = path

	def getCode(self):
		code =  f"\t\t\t\t<object type=\"Sprite\" name=\"{self.path.name}\">\n" # The start of a scene

		looks =  isvalid(self.path / 'looks', False)
		audios = isvalid(self.path / 'audios', False)
		script = self.path / 'script.ptb' if Path(self.path / 'script.ptb').exists() else None

		# Get looks ----------------------------------------------------------------
		if looks:
			# There are looks! Listing them
			code += "\t\t\t\t\t<lookList>\n"

			for look in looks.iterdir():
				# Detected look! Opening <looks>
				self.lookslist.append(look)
				code += ( f"\t\t\t\t\t\t<look fileName=\"{look.name}\" name=\"{look.stem}\">\n"
					"\t\t\t\t\t\t\t<isWebRequest>false</isWebRequest>\n"
					"\t\t\t\t\t\t\t<valid>true</valid>\n"
					"\t\t\t\t\t\t</look>\n"
				)

			code += "\t\t\t\t\t</lookList>\n"
		else:
			# No looks detected
			code += "\t\t\t\t\t<lookList/>\n"

		# Get audios ---------------------------------------------------------------
		if audios:
			# There are audios! Listing them
			code += "\t\t\t\t\t<soundList>\n"

			for audio in audios.iterdir():
				# Detected audio! Opening <sound>
				self.audioslist.append(audio)
				code += ( f"\t\t\t\t\t\t<sound fileName=\"{audio.name}\" name=\"{audio.stem}\">\n"
					"\t\t\t\t\t\t\t<midiFile>false</midiFile>\n"
					"\t\t\t\t\t\t</sound>\n"
				)

			code += "\t\t\t\t\t</soundList>\n"
		else:
			# No audios detected
			code += "\t\t\t\t\t<soundList/>\n"

		# Get the script -----------------------------------------------------------
		if not script:
			code += "\t\t\t\t\t<scriptList/>\n"
		else:
			# Script detected! Opening <scriptList>
			with open(script) as _script:
				if not _script.read().strip():
					code += "\t\t\t\t\t<scriptList/>\n"
				else:
					code += "\t\t\t\t\t<scriptList>\n"
					objCode = ptbint.Interpreter(script)
					code += objCode.interprete()
					code += "\t\t\t\t\t</scriptList>\n"

		# Other variables that we don't support yet --------------------------------
		code += (
			"\t\t\t\t\t<nfcTagList/>\n"
			"\t\t\t\t\t<userVariables/>\n"
			"\t\t\t\t\t<userLists/>\n"
			"\t\t\t\t\t<userDefinedBrickList/>\n"
			)

		code +=  "\t\t\t\t</object>\n" # The start of a scene
		return code

	def getLooks(self):
		return self.lookslist

	def getAudios(self):
		return self.audioslist