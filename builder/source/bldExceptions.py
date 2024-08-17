import random, math

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

		# All Path Exceptions
		if self.desc == "path.invalid":
			error += f"[!] The path \'{self.contents[0]}\' is not valid."

		# All Folders Exceptions
		elif self.desc == "folder.missing.scenes":
			error += f"[!] You must create a 'scenes' folder in your project directory."
		elif self.desc == "folder.destiny.perms":
			error +=  "[!] We do not have perms to create folders in destiny."
		elif self.desc == "folder.destiny.error":
			error +=  "[!] There was an error while creating the destiny folder."

		# All Scenes Exceptions
		elif self.desc == "scenes.empty":
			error += f"[!] There must be at least one scene inside the 'scenes' folder."

		error +=  f"\n#####################################################\n"
		print(error)
		exit()