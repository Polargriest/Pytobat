import re, uuid
from . import console

# Reserved words ------------------------------------------------------
KEYWORDS = ["event", "pass"]
EVENTS = {
	"WHEN_SCENE_STARTS": "StartScript",
	"WHEN_TAPPED": "WhenScript",
	"WHEN_STAGE_IS_TAPPED": "WhenTouchDownScript"
}
FUNCTIONS = {
	# Looks bricks
	"hide": { "args": 0, "type" : "HideBrick"},
	"show": { "args": 0, "type": "ShowBrick" },
	"nextLook": { "args": 0, "type": "NextLookBrick" },
	"previousLook": { "args": 0, "type": "PreviousLookBrick" }
}
queue = []

def interprete(scriptRef):
	# INTERPRETE CODE HERE --------------------------------------------

	# Variables we need
	xml = "" # We store all the code here
	lines = [] # We store all the individual of the script lines here
	contextStack = [] # We store all the current contexts of the program
	currentLine = 0 # Current line reading

	xml += ""

	# Opens the script and split it all in lines
	with open(scriptRef) as script:
		lines = script.read().splitlines()

	# We start looking every line
	for line in lines:
		currentLine += 1

		# Interpreter ignores ----------------------
		if line.strip('\t').startswith('#'): # Comments
			continue

		if line == "": # Blank line
			continue

		# Get the context --------------------------
		context = getContext(line)

		if context > len(contextStack): # If there are more indents than context, throw error
			raise console.PtbException("error", [scriptRef, currentLine], [], "syntax.indent.unexpected")
		elif context < len(contextStack): # If there are more contexts than indents, pop contexts
			while context < len(contextStack):
				xml = xml + queue[0]
				queue.pop()
				contextStack.pop()


		# Remove indent from line and tokenize
		line = line.strip('\t')
		tokens = line.split()

		# Keyword handler -------------------------
		if tokens[0] in KEYWORDS:
			# Event keyword handler
			if tokens[0] == "event":
				# Event validations
				try:
					event = re.search(r'^\w+', tokens[1]).group()
				except IndexError as e: # If user just wrote 'event' without elaborating
					raise console.PtbException("error", [scriptRef, currentLine], [], "syntax.eventkw.none")
				except AttributeError as e: # If user wrote invalid event
					raise console.PtbException("error", [scriptRef, currentLine], [], "syntax.eventkw.invalid")

				if "event" in contextStack: # Not an event paradox
					raise console.PtbException("error", [scriptRef, currentLine], [], "event.paradox")

				if not event in EVENTS: # Does event exists?
					raise console.PtbException("error", [scriptRef, currentLine], [event], "event.notfound")

				# Event behaviour
				contextStack.append("event")
				xml += openEvent(event)
			
			# Pass keyword handler
			if tokens[0] == "pass":
				# Pass validations
				if len(contextStack) == 0:
					raise console.PtbException("error", [scriptRef, currentLine], [], "pass.nothing")

			continue

		# Function handler ------------------------
		elif validateFunction(line):
			name = validateFunction(line)
			args = validateFunction(line, False)

			# Function validations
			if not "event" in contextStack: # Function must be inside an event
				raise console.PtbException("error", [scriptRef, currentLine], [name], "function.context.outside")
			
			if not name in FUNCTIONS: # Check if function exists
				raise console.PtbException("error", [scriptRef, currentLine], [name], "function.notfound")

			if len(args) != FUNCTIONS[name]["args"]: # Check if number of arguments is ok
				raise console.PtbException("error", [scriptRef, currentLine], [name, FUNCTIONS[name]["args"], len(args)], "function.args.incorrect")

			# Function behaviour
			xml += createBrick(name, args)

			continue

	# -----------------------------------------------------------------

	for waiter in queue:
		xml += waiter

	return xml

"""
Here ends the interpreter code.
Now entering: functions that makes the interpreter work
"""

def openEvent(event):
	result =     f"""						<script type="{EVENTS[event]}" posX="0.0" posY="0.0">\n"""
	result +=    f"""							<brickList>\n"""
	queuePush =  f"""							</brickList>\n"""
	queuePush += f"""							<commentedOut>false</commentedOut>\n"""
	queuePush += f"""							<scriptId>{uuid.uuid4()}</scriptId>\n"""
	queuePush += f"""						</script>\n"""
	queue.append(queuePush)
	return result

def createBrick(function, args):
	result =  f"""								<brick type="{FUNCTIONS[function]["type"]}" posX="0.0" posY="0.0">\n"""
	result += f"""									<brickId>{uuid.uuid4()}</brickId>\n"""
	result += f"""									<commentedOut>false</commentedOut>\n"""
	result += f"""								</brick>\n"""
	return result

def validateFunction(string, getName=True):
	# Check if is a function
	function = re.search(r'\w+(?=\()', string)

	if function: # Is a function!
		if getName:
			return function.group() # Return only the name if wanted
		else:
			arguments = re.search(r'(?<=\().+?(?=\))', string)
			return arguments.group().split(', ') if arguments else [] # Return the function's arguments
	else:
		return False

def getContext(string):
	# This functions return the context of the current string
	count = 0
	for char in string:
		if (char == '\t'):
			count += 1
		else:
			return count