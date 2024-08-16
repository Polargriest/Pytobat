from lark import Lark
from lark.indenter import Indenter
import os

class IndenterParser(Indenter):
	NL_type = '_NEWLINE'
	OPEN_PAREN_types = []
	CLOSE_PAREN_types = []
	INDENT_type = '_INDENT'
	DEDENT_type = '_DEDENT'
	tab_len = 4

class Interpreter:
	def __init__(self, script):
		# Open the script
		with open(script, 'r') as _script:
			self.script = _script.read()

		# Open the grammar and create the parser
		with open(os.path.join(__file__, '../pytobat.gram')) as _grammar:
			self.parser = Lark(_grammar, parser='lalr', postlex=IndenterParser(), start='statements')

	# This method is the interpreter manager
	def interprete(self):
		print(self.parser.parse(self.script).pretty())
		return ""