#!/usr/bin/env python
#import argparse
import sys
#this is a console-based launcher that is meant for engine and level testing.
#it will launch the specifed maze xml in debug mode.
#this prints extra status messages to teh console.
#when the engine itself is in debug mode, you mau hold shift to walk on unwalkable nodes.
DEBUG=1
print sys.argv[1]
if sys.argv[1]=="-h" or sys.argv[1]=="--help":
	print '''This is a simple MAZE-ENG2.py console launcher.
It will start the engine in debug mode.
this will let you move through walls with shift. 
usage:
./testlaunch.py [maze xml file], -h, --help'''
else:
	mazefilepath=(sys.argv[1])
	execfile('MAZE-ENG2.py')