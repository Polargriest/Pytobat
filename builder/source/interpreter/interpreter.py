from lark import Lark
import os

# Import the grammar
parser = None
with open(os.path.join(os.path.dirname(__file__), 'grammar.lark'), 'r') as grammar:
	parser = Lark(grammar.read())

def interprete(script):
	with open(script, 'r') as ptb_file:
		script = ptb_file.read()

	tree = parser.parse(script)
	print(tree.pretty())
	return ""

#interprete("script.ptb")