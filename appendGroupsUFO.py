#!/usr/bin/env python
# encoding: utf-8
"""
appendGroupsUFO.py
"""

import os, sys, optparse
from defcon import Font

__version__ = "1.00"
__copyright__ = "Copyright (c) 2016 by David Brezina"
__description__ = """Appends groups from a text file to UFO."""
__requirements__ = "Requires Python 2.5 or higher and defcon."

def parseOptions():
	usage = "usage: %prog [options] <inputfile> -o <outputfile>"
	parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=usage, version=__version__, description="%prog " + "version %s. %s. %s" % (__version__, __copyright__, __description__), epilog=__requirements__)
	
	parser.add_option("-v", "--verbose",
		action="store_true", dest="verbose", default=False,
		help="print additional information")
	parser.add_option("-g", "--groups",
		action="store", dest="inpath", type="string", default="",
		help="path to a file with groups to add (represented as python dict object)")
	return parser.parse_args()

def main():
	(options, args) = parseOptions()

	if len(args) >= 1:
		if os.path.exists(args[0]) and os.path.exists(options.inpath):
			ufoPath = args[0]
		else: 
			print "File does not exist."

		# main business
		try:
			with open(options.inpath, "r") as groupsfile:
				groups = eval(groupsfile.read())

			font = Font(ufoPath)
			for name, content in groups.items():
				if name not in font.groups:
					font.groups[name] = content
				else:
					for g in content:
						if g not in font.groups[name]:
							font.groups[name].append(g)
			font.save()
		except:
			print "Errors during processing."
	else: 
		print "Add -h for help"

if __name__ == "__main__":
	sys.exit(main())
