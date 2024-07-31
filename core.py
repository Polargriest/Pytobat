from pytobat import Pytobat

##################################

# Welcome to CORE.PY :)
# Here you can configure your game. Please, change these options carefully.

gameName = "Apariencias y asi"

ptc = Pytobat(gameName) # Do not erase this line

# Settings
ptc.header["platformVersion"] = "30"     # Pocket Code version. Last public release is 30
ptc.header["landscapeMode"] = "true"

# When you are done and want to compile the game, please run this program.

##################################

ptc.build(True) # Acá lo compilas