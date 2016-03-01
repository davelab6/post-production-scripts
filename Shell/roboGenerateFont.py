#!/usr/bin/env python


"""
roboGenerateFont.py
"""

import os, os.path, sys, optparse, time
from subprocess import call
from pipes import quote
from AppKit import *

__version__ = "2.10"
__copyright__ = "Copyright (c) 2015 by David Brezina"
__description__ = """Generate TTF, OTF, ... from UFO using RoboFont."""
__requirements__ = "Requires Python 2.5 or higher, AppKit (pip install pyobjc & pip install pyobjc-core), and RoboFont command-line tool (installed from the application preferences)."


def parseOptions():
	usage = "usage: %prog [options] path"
	parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=usage, version=__version__, description="%prog " + "version %s. %s. %s" % (__version__, __copyright__, __description__), epilog=__requirements__)

	parser.add_option("-v", "--verbose",
		action="store_true", dest="verbose", default=False,
		help="print additional information")
	parser.add_option("-f", "--formats",
		action="store", dest="formats", type="string", default="ttf",
		help="comma-separated list of font formats to produce, e.g. otf,ttf (if omitted, only ttf is produced)")
	parser.add_option("-d", "--decompose",
		action="store_true", dest="decompose", default=False,
		help="decompose glyphs")
	parser.add_option("-c", "--checkOutlines",
		action="store_true", dest="checkOutlines", default=False,
		help="check outlines")
	parser.add_option("-a", "--autohint",
		action="store_true", dest="autohint", default=False,
		help="autohint")
	parser.add_option("-k", "--de-kern",
		action="store_true", dest="dekern", default=False,
		help="clear all kerning before generating the font, UFO stays unchanged.")
	parser.add_option("-r", "--releaseMode",
		action="store_true", dest="releaseMode", default=False,
		help="release mode")
	parser.add_option("-o", "--output",
		action="store", dest="outpath", type="string", default="",
		help="output everything to this folder instead of the current working folder")
	return parser.parse_args()

def runRoboFont(code = "", script = "", font = ""):
	"""
	Call RoboFont and run python code, script (file path), or open font file from the argument.
	It is assumed that RoboFont is in the Applications folder.
	"""
	
	options = {}
	if code:
		options["pythonCode"] = [code]
	if script:
		options["pythonScripts"] = [script]
	if font:
		options["openFiles"] = [font]
	workspace = NSWorkspace.sharedWorkspace()

	appPath = os.path.join("/","Applications","RoboFont.app")
	launched = workspace.launchApplicationAtURL_options_configuration_error_(NSURL.fileURLWithPath_(appPath), NSWorkspaceLaunchWithoutActivation, None, None)

	if launched:
	    if isinstance(launched, tuple):
	        app, error = launched
	    else:
	        app = launched

	    if app and not app.isFinishedLaunching():
	        app = NSRunningApplication.runningApplicationsWithBundleIdentifier_(app.bundleIdentifier())[-1]
	        time.sleep(1)
	        
	    dnc = NSDistributedNotificationCenter.defaultCenter()
	    dnc.postNotificationName_object_userInfo_deliverImmediately_("com.typemytype.robofont.remote", None, options, True)

def main():
	(options, args) = parseOptions()

	options.formats = options.formats.split(",")

	if args > 0:
		code = "inpath = '%s'\n" % os.path.realpath(args[0])
		code += "f = OpenFont(inpath, showUI=False)\n" # opens font without GUI, faster
		if options.dekern:
			code += "f.kerning.clear()\n"
		if options.outpath:
			code += "outpath = '%s'\n" % os.path.join(os.path.realpath(options.outpath), args[0])
		else:
			code += "outpath = '%s'\n" % os.path.realpath(args[0])
		for suffix in options.formats:
			code += "f.generate(outpath[:-3]+'%s', '%s', decompose=%s, checkOutlines=%s, autohint=%s, releaseMode=%s)\n" % (suffix, suffix, options.decompose, options.checkOutlines, options.autohint, options.releaseMode)
		code += "del f"
		
		if options.verbose:
			print "Running this code in RoboFont:"
			print
			print code
			print
		print "Generating fonts from UFO (RoboFont GUI will not show up)"
		runRoboFont(code=code)

if __name__ == "__main__":
	sys.exit(main())
