# Import all lark functionalities
from lark import Lark, Transformer
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

class TranformXML(Transformer):
	xml = ""
	buffer = []

	def __init__(self, path):
		super().__init__()
		self.path = path

		# Open the Pytobat Bricks data
		with open(os.path.join(__file__, '../bricks.json'), 'r') as _bricksData:
			self.brickData = json.load(_bricksData)

	def event(self, items): # Event handler -------------------------------------------------------

		# Check if the event exists
		eventName = items[0].children[0]
		if not eventName in self.brickData["events"]:
			cnsl.PtbException('e', [self.path, eventName.line], [eventName], 'event.notfound')

		# Start script in XML code
		self.xml += "\t\t\t\t\t\t<script type=\"type\" posX=\"0.0\" posY=\"0.0\">\n"
		print("Items: " + str(items))

		if items[1].data == 'pass': # Run this if event is empty
			self.xml += (
				 "\t\t\t\t\t\t\t<brickList/>\n"
				 "\t\t\t\t\t\t\t<commentedOut>false</commentedOut>\n"
				f"\t\t\t\t\t\t\t<scriptId>{uuid.uuid4()}</scriptId>\n"
				 "\t\t\t\t\t\t</script>\n"
			)
		else:
			self.xml += "\t\t\t\t\t\t\t<brickList>\n"
			self.buffer.append(
				 "\t\t\t\t\t\t\t</brickList>\n"
				 "\t\t\t\t\t\t\t<commentedOut>false</commentedOut>\n"
				f"\t\t\t\t\t\t\t<scriptId>{uuid.uuid4()}</scriptId>\n"
				 "\t\t\t\t\t\t</script>\n"
				)

	def asdfmovie(self, contents):
		print("Brick found!")
		return ""


class Interpreter:
	def __init__(self, script):
		self.scriptPath = script

		# Open the script
		with open(script, 'r') as _script:
			self.script = _script.read()

		# Open the grammar and create the parser
		with open(os.path.join(__file__, '../pytobat.gram'), 'r') as _grammar:
			self.parser = Lark(_grammar, parser='lalr', postlex=IndenterParser(), start='statements')

	# This method is the interpreter manager
	def interprete(self):
		tree = self.parser.parse(self.script + "\n")
		transoformer = TranformXML(self.scriptPath)
		transoformer.transform(tree)

		print("----------------- PRINTING TREE -----------------\n" + tree.pretty())
		print("----------------- PRINTING CODE -----------------\n" + transoformer.xml)

		return transoformer.xml