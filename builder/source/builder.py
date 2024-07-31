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