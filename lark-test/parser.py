from lark import lark
from lark.indenter import Indenter

class TreeIndenter(Indenter):
	CLOSE_PAREN_types = []
	OPEN_PAREN_types = []
	NL_type = '_NL'
	DEDENT_type = '_DEDENT'
	INDENT_type = '_INDENT'
	tab_len = 4

# Create our parser
parser = None
with open("pytobat.lark") as grammar:
	parser = lark.Lark(grammar.read(), parser='lalr', postlex=TreeIndenter())

# Load our script
text = None
with open("script.ptb") as script:
	text = script.read()

tree = parser.parse(text)
print(tree.pretty())