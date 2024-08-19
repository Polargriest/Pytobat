# Import all lark functionalities
from lark import Lark, Visitor
from lark.indenter import Indenter

# Libraries needed for the interpreter to work
import os
import json
import uuid

# Libraries to handle exceptions in the interpreter
#from . import ptbExceptions as cnsl

class IndenterParser(Indenter):
	NL_type = '_NEWLINE'
	OPEN_PAREN_types = []
	CLOSE_PAREN_types = []
	INDENT_type = '_INDENT'
	DEDENT_type = '_DEDENT'
	tab_len = 4

class WriteXML(Visitor):
	xml = ""
	buffer = []

	def __init__(self, path):
		super().__init__()
		self.path = path

		# Open the Pytobat Bricks data
		bricksPath = os.path.join(os.path.dirname(__file__), "bricks.json")
		bricksPath = os.path.abspath(bricksPath)

		with open(os.path.join(__file__, '../bricks.json'), 'r') as _bricksData:
			self.brickData = json.load(_bricksData)

	def pop_context(self):
		try:
			self.xml += self.buffer[0]
			self.buffer.pop()
		except IndexError:
			pass

	def event(self, items): # Event handler -------------------------------------------------------

		# Check if the event exists
		eventName = items.children[0].children[0]
		if not eventName in self.brickData["events"]:
			cnsl.PtbException('e', [self.path, eventName.line], [eventName.value], 'event.notfound')

		# Empty the buffer to let next event start
		self.pop_context()

		# Start script in XML code
		self.xml += f"\t\t\t\t\t\t<script type=\"{self.brickData['events'][eventName.value]}\" posX=\"0.0\" posY=\"0.0\">\n"

		self.xml += "\t\t\t\t\t\t\t<brickList>\n"
		self.buffer.append(
			"\t\t\t\t\t\t\t</brickList>\n" +
			makeFooter(7, 'event') + 
			"\t\t\t\t\t\t</script>\n"
			)

	def ptb_pass(self): # Empty code block using ptb_pass -----------------------------------------
		self.xml = self.xml[:-12] + "<bricklist/>\n"
		self.xml += "\n".join(self.buffer[0].splitlines()[1:])

	def brick(self, contents): # Bricks -----------------------------------------------------------

		# Check if brick exists
		brickName = contents.children[0].children[0]
		if not brickName in self.brickData["bricks"]:
			cnsl.PtbException('e', [self.path, brickName.line], [brickName.value], 'brick.notfound')

		# Check if the amonut of arguments sent is correct
		givenArguments = contents.children[1].children
		argumentsNeeded = self.brickData["bricks"][brickName.value]["arguments"]
		if len(givenArguments) != argumentsNeeded:
			cnsl.PtbException('e', [self.path, brickName.line], [brickName.value, len(givenArguments), argumentsNeeded], 'brick.args.mismatch')
		
		# Write brick on XML
		self.xml += (
			f"\t\t\t\t\t\t\t\t<brick type=\"{self.brickData['bricks'][brickName.value]['type']}\">\n" + 
			 makeFooter(9, 'brick') +
			 "\t\t\t\t\t\t\t\t</brick>\n"
		)

	def on_finish(self): # Runs when tree visiting finishes ---------------------------------------
		for item in self.buffer:
			self.xml += item


class Interpreter:
	def __init__(self, script):
		self.scriptPath = script

		# Open the script
		with open(script, 'r') as _script:
			self.script = _script.read()

		# Open the grammar and create the parser
		grammarPath = os.path.join(os.path.dirname(__file__), 'pytobat.gram')
		grammarPath = os.path.abspath(grammarPath)

		with open(grammarPath, 'r') as _grammar:
			self.parser = Lark(_grammar, parser='lalr', postlex=IndenterParser(), start='statements')

	# This method is the interpreter manager
	def interprete(self):
		tree = self.parser.parse(self.script + "\n")
		transoformer = WriteXML(self.scriptPath)
		transoformer.visit_topdown(tree)
		transoformer.on_finish()

		#print("----------------- PRINTING TREE -----------------\n" + tree.pretty())
		#print("----------------- PRINTING CODE -----------------\n" + transoformer.xml)

		return transoformer.xml

def makeFooter(indention, type):
	if type == 'event':
		footer = "\t"*indention + f"<scriptId>{uuid.uuid4()}</scriptId>\n"
	else:
		footer = "\t"*indention + f"<brickId>{uuid.uuid4()}</brickId>\n"
	footer += "\t"*indention +  "<commentedOut>false</commentedOut>\n"

	return footer