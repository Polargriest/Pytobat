import os, shutil
from pathlib import Path
from . import bldExceptions, essentials

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
		"platformVersion": 33,
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

	def build(self, project, destiny, toCatrobat=True):
		# Validate the paths the user provided --------------------------------------------
		project = essentials.isvalid(project)

		# START THE CODE ##################################################################
		xml = (
			"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>\n"
			"<program>\n" )

		# Create header -------------------------------------------------------------------
		xml += "\t<header>\n"
		for key in self.header:
			xml += f"\t\t<{key}>{self.header[key]}</{key}>\n"
		xml += "\t</header>\n"

		# Create empty settings -----------------------------------------------------------
		xml += "\t<settings/>\n"

		# Get all scenes ------------------------------------------------------------------
		xml += "\t<scenes>\n"
		try:
			scenepaths = [scene for scene in (project/'scenes').iterdir()]
		except FileNotFoundError:
			raise bldExceptions.BuilderException("error", [], "folder.missing.scenes")

		# Raise an error if no scenes founded
		if not scenepaths:
			raise bldExceptions.BuilderException("error", [], "scenes.empty")

		# Create scenes
		for scene in scenepaths:
			scene = essentials.Scene(scene)
			self.scenes.append(scene)
			xml += scene.getCode()

		# End the scripting ---------------------------------------------------------------
		xml += "\t</scenes>\n"
		xml += (
			"\t<programVariableList/>\n"
			"\t<programListOfLists/>\n"
			"\t<programMultiplayerVariableList/>\n"
			)
		xml += "</program>"

		# CREATING THE CATROBAT PROJECT ###################################################

		# Convert destiny to path
		destiny = Path(destiny)

		# Create an scene folder for every scene ------------------------------------------
		for scene in self.scenes:
			scenepath = destiny / scene.name
			os.makedirs(scenepath, exist_ok=True)

			# Create folders for looks and audios -----------------------------------------
			looksdir =  scenepath / 'images'
			audiosdir = scenepath / 'sounds'
			os.makedirs(looksdir, exist_ok=True)
			os.makedirs(audiosdir, exist_ok=True)

			# Add the looks ---------------------------------------------------------------
			looks = scene.getLooks()
			if looks:
				for look in looks:
					shutil.copy(look, looksdir)

			# Add the audios --------------------------------------------------------------
			audios = scene.getAudios()
			if audios:
				for audio in audios:
					shutil.copy(audio, audiosdir)

		# Create the XML file -------------------------------------------------------------
		xmlFile = destiny / 'code.xml'
		with open(xmlFile, 'w') as file:
			file.write(xml)

		# CREATE THE CATROBAT PROJECT #####################################################
		if toCatrobat:
			catrobat = destiny.parent

			if (catrobat / f"{self.programName}.catrobat").exists():
				os.remove(catrobat / f"{self.programName}.catrobat")

			shutil.make_archive(destiny, 'zip', destiny)
			os.rename(catrobat / f"{self.programName}.zip", catrobat / f"{self.programName}.catrobat")

			# SUCCESFUL MESSAGE ###########################################################
			print(f"Succesfully created '{self.programName}'.catrobat at {catrobat / self.programName}.catrobat")