from pathlib import Path
import shutil
import os
import uuid
import re
import random
import math

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