"""
                                               (                  
                                 @@@        @   @                 
                               @(     @@@@#     #                 
                              @*  @    /@@    @ ,@                
                              @ @  @@      @@   @                 
                              @  @ @@   @@  &   @#                
                            /@@@@@    &@(  @@ @  @                
                       @@ @ @* @         @@@@   @      @ @@       
                     @     @  @@ @@          .@      .@      @    
                   @         @    @@         @    @@@          @  
                  @      @    %@               @@@  @  @        @ 
                 @ .@   &*        @        @    @@@ @@@@ @       @
                 @     @     /@  @         @       @@@  @/#@&@@@@@
                       /     @@@&*          @    @ @@@            
                             @@@@            /@@                  
                                @                                 
                                 (@ 

88888888ba                                     88                       
88      "8b                 ,d                 88                         ,d
88      ,8P                 88                 88                         88
88aaaaaa8P'  8b       d8  MM88MMM  ,adPPYba,   88,dPPYba,   ,adPPYYba,  MM88MMM
88'''''''    `8b     d8'    88    a8"     "8a  88P'    "8a  ""     `Y8    88
88            `8b   d8'     88    8b       d8  88       d8  ,adPPPPP88    88
88             `8b,d8'      88,   "8a,   ,a8"  88b,   ,a8"  88,    ,88    88,
88               Y88'       "Y888  `"YbbdP"'   8Y"Ybbd8"'   `"8bbdP"Y8    "Y888
                 d8'                                                   
                d8'                                                    

* Run this Python file to convert your Pytobat Project to a Pocket Code game
* Currently using Pytobat version 0.1-dev.2
"""

# Import the builder
from source.builder import Pytobat

def validrange(option, num1, num2):
	try:
		option = int(option)
		return True if (option >= num1 and option <= num2) else False

	# If option is not a number
	except ValueError:
		return False

def validresolution(resolution):
	try:
		resolution = int(resolution)
		return True if (resolution > 0) else False

	# If resolution is not a number
	except ValueError:
		print("[!] I mean, of course we validated THAT.")
		return False

# Welcome message
print(
	"Welcome to the Pytobat Wizard!\n"
	"* You are currently using Pytobat v0.1-dev.2\n"
	"* Press [ENTER] to start the wizard.\n"
)

input()

# Ask for Project name ############################################################################
print(
	"--- 1. Name ----------------------------- [.][_][X]\n"
	"Name of your Pocket Code game:\n"
)

name = input("> ")

# Ask for game orientation ########################################################################
print(
	"\n--- 2. Orientation --------------------------------\n"
	"Orientation of your game:\n\n"

	" 1)  ______    2)  _____________ \n"
	"    |      |      |           | |\n"
	"    |      |      |           | |\n"
	"    |      |      |___________|_|\n"
	"    |      |\n"
	"    |______|         LANDSCAPE\n"
	"    |______|\n"
	"\n"
	"    PORTRAIT\n"
)

orientation = 0

# Repeat until user gives valid number
while not validrange(orientation, 1, 2):
	orientation = input("(1|2) > ")

	# Prints an error if user did not gives valid number
	if not validrange(orientation, 1, 2):
		print("[!] Please insert a number within the valid range (1, 2)")

# Ask for game resolution #########################################################################
print(
	"\n--- 3. Resolution --------------------------------\n"
	"Please, choose the resolution of your game.\n"
	"* Wait, what'd you say? You don't know resolutions? Fear not.\n"
	"* Please choose an options for our Resolution Manager.\n\n"
)

width = 0
height = 0

resManager = True
option = 0

# Repeat until the user gives a valid resolution
resoltuionMenu = True
option = -1

menu = (
		"[1] I want to set an exact resolution.\n"
		"[2] I want to see a list of common resolutions.\n"
		"[3] Keep the resolution as the default (1473x720)\n"
	)
resolutionsList = [
	[720, 1473],  # CupStudios phone
	[1080, 2252]  # My phone lol
]

print(menu)

while resoltuionMenu:

	option = input("(1|2|3) > ")

	# Ask if option is valid
	if not validrange(option, 1, 3):
		print("[!] Please insert a number between the valid range (1, 2 or 3)")
	else:
		option = int(option)
		if option == 1:
			# I want to set an exact resolution.
			print("\n- EXACT RESOLUTION: ----- [To go back: -1]")
			print("Be aware! We do not validate resolutions. Hope you know what you're doing!\n")

			width = 0
			height = 0

			# Validate width
			while not validresolution(width):
				width = input("Width: > ")

				if width == "-1": # If user want to leave
					print("\n------------------------------\nYeah, no problem. Here's the menu again:\n")
					print(menu)
					break
				elif not validresolution(width): # If the resolution is not valid
					print("[!] I mean, of course that resolution is not valid")

			# Validate height
			while (not validresolution(height)) and width != "-1":
				height = input("Height: > ")

				if height == "-1": # If user want to leave
					print("\n------------------------------\nYeah, no problem. Here's the menu again:\n")
					print(menu)
					break
				elif not validresolution(height): # If the resolution is not valid
					print("[!] I mean, of course that resolution is not valid")

			if (width != "-1" and height != "-1"):
				width = int(width)
				height = int(height)

				print(f"\nExcelent! The resolution will be {width}x{height}")
				resoltuionMenu = False

		elif option == 2:
			# I want to see a list of common resolutions.
			print("\n- CHOOSE FROM A LIST: ----- [To go back: -1]")
			print("Aight. We guarantee that these resolutions work for lots of phones.\n")

			resIndex = 0
			for res in resolutionsList:
				resIndex += 1
				print(f"   {resIndex}. {res[0]}x{res[1]}")

			print("\n Please, choose wisely!")
			choosenResolution = 0

			while not validrange(choosenResolution, 1, resIndex):
				choosenResolution = input(f"(1|{resIndex}) > ")

				if not validrange(choosenResolution, 1, resIndex):
					if choosenResolution == "-1":
						print("\n------------------------------\nYeah, no problem. Here's the menu again:\n")
						print(menu)
						break

					print("[!] Sorry, that's not a valid resolution.")
				else:
					choosenResolution = int(choosenResolution) - 1
					width = resolutionsList[choosenResolution][0]
					height = resolutionsList[choosenResolution][1]

					print(f"\nExcelent! The resolution will be {width}x{height}")
					resoltuionMenu = False

		elif option == 3:
			# Keep the resolution as the default (1473x720)
			width = 1473
			height = 720

			resoltuionMenu = False
			print("\n- USE DEFAULTS: ----- \n")
			print("Good choice. Hope you like it!\n\n")

