from pathlib import Path
from . import console, essentials

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

	def build(self, project, destiny, toCatrobat=True):
		# Validate the paths the user provided
		project = essentials.isvalid(project)
		destiny = essentials.isvalid(destiny)

		# Start the builder ---------------------------------------------------------------
		xml = (
			"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>\n"
			"<program>\n" )

		# Create header -------------------------------------------------------------------
		xml += "\t<header>\n"
		for key in self.header:
			xml += f"\t\t<{key}>{self.header[key]}</{key}>\n"
		xml += "\t</header>\n"

		# Get all scenes ------------------------------------------------------------------
		xml += "\t<scenes>\n"
		try:
			scenes = [scene for scene in (project/'scenes').iterdir()]
		except FileNotFoundError:
			raise console.BuilderException("error", [], "folder.missing.scenes")

		# Raise an error if no scenes founded
		if not scenes:
			raise console.BuilderException("error", [], "scenes.empty")

		# Create scenes
		for scene in scenes:
			scene = essentials.Scene(scene)
			xml += scene.getCode()

		xml += "\t</scenes>\n"
		# End the builder -----------------------------------------------------------------
		xml += "</program>"
		print(xml)