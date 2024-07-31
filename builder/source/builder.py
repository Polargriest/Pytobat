from pathlib import Path
from . import console

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

	def isvalid(self, path):
		# This function is used to validate a certain path the user provided.
		# Returns the path is valid, otherwise throws path.invalid.

		path = Path(path)

		if path.exists() and path.is_dir():
			return path
		else:
			raise console.BuilderException("error", [path], "path.invalid")

	def build(self, project, destiny, toCatrobat=True):
		# Validate the paths the user provided
		project = self.isvalid(project)
		destiny = self.isvalid(destiny)

		# Start the builder
		xml = "<program>\n"

		# Create header
		xml += "\t<header>\n"
		for key in self.header:
			xml += f"\t\t<{key}>{self.header[key]}</{key}>\n"
		xml += "\t</header>\n"

		# End the builder
		xml += "</program>"
		print(xml)