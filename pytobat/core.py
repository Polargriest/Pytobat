from pytobat import Pytobat

"""
* Welcome to the Pytobat Builder! :)
* This file is used to convert your Pytobat code into Pocket Code projects.
* Follow the steps below to build your first game effortlessly.
"""

# --------------------------------------------------------------------------

# 1. Project name
name = "My project"

# 2. Orientation mode (true: landscape | false: portrait)
header = { "landscapeMode": "true" }

# 3. Resolution (we'll adjust for orientation)
width = 1080
height = 1126

# --------------------------------------------------------------------------

# 4. Specify
#      1) Your Pytobat project folder
#      2) where you want to save your converted Pocket Code files
ptc_project = "../Game"
ptc_destiny = "../"

# 4. Create the .catrobat file? (False for testing only)
catrobat_file = False

# 5. Additional preferences (check Pytobat documentation for details)

# --------------------------------------------------------------------------

# That's it! Run this Python file to start the builder.
# Everyhting below is for the builder. DO NOT CHANGE.

ptc = Pytobat(name)

# Apply header settings
for attribute in header:
	ptc.header[attribute] = header[attribute]

ptc.build(ptc_project, ptc_destiny, catrobat_file)