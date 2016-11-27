#!/usr/bin/env python

# Text-maze 5
#mazemodpath = (os.path.join('MAZE', 'sample.MOD.txt'))




##############
#wordbindings:
##############
#FORWARD
FORWARDWORDBIND=('w')
#BACKWARD
BACKWARDWORDBIND=('s')
#left
LEFTWORDBIND=('a')
#right
RIGHTWODBIND=('d')
#quit
QUITWORDBIND=('q')
##############
#import LIBTIMG
#import libtextmaze
import pygame.event
import pygame.key
import pygame.display
import pygame.image
import pygame.mixer
#import pygame.mixer.music
import pygame
import time
import os
from pygame.locals import *
import xml.etree.ElementTree as ET

#check for global variables
if 'mazefilepath' in globals():
	print ("Global variable: 'mazefilepath' detected, using as maze refrence.")
else:
	print ("Global variable: 'mazefilepath' not detected, using default maze.")
	mazefilepath = (os.path.join('MAZE', 'sample.xml'))
if 'MENUFLG' in globals():
	print ("Global variable: 'MENUFLG' present. following its setting.")
else:
	print ("Global variable: 'MENUFLG' not present. using default.")
	MENUFLG=0
if 'DEBUG' in globals():
	print ("Global variable: 'DEBUG' present. following its setting.")
else:
	print ("Global variable: 'DEBUG' not present. using default.")
	DEBUG=0
if 'scrnx' in globals():
	print ("Global variable: 'scrnx' present. following its setting.")
else:
	print ("Global variable: 'scrnx' not present. using default.")
	scrnx=400
if 'scrny' in globals():
	print ("Global variable: 'scrny' present. following its setting.")
else:
	print ("Global variable: 'scrny' not present. using default.")
	scrny=400



def debugmsg(msg, printplaypos=0):
	if DEBUG==1:
		
		if printplaypos==1:
			print (msg + " x(" + str(playx) + "),y(" + str(playy) + ")")
		else:
			print msg


#load window icon, make window, set caption, start music, init things. etc.
debugmsg("Initalizing graphics and sound...")
pygame.mixer.init()
if MENUFLG==0:
	pygame.mixer.music.load(os.path.join('AUDIO', 'vg-mus-2_spooky-hall.ogg'))
	#pygame.mixer.music.load(os.path.join('AUDIO', 'vgtrack1.mid'))
	pygame.mixer.music.play(-1)
stepfx=pygame.mixer.Sound(os.path.join('AUDIO', 'step.ogg'))
mipfx=pygame.mixer.Sound(os.path.join('AUDIO', 'mip.ogg'))
switchonfx=pygame.mixer.Sound(os.path.join('AUDIO', 'switchon.ogg'))
switchofffx=pygame.mixer.Sound(os.path.join('AUDIO', 'switchoff.ogg'))

pygame.display.init()
pygame.font.init()
windowicon=pygame.image.load(os.path.join('TILE', 'icon32.png'))
pygame.display.set_icon(windowicon)
screensurfdex=pygame.display.set_mode((scrnx, scrny), RESIZABLE)
screensurf=pygame.Surface((400, 400))
pygame.display.set_icon(windowicon)
pygame.display.set_caption("Text-maze 5", "Text-maze 5")
debugmsg("Loading Graphical data.")
#load tiles
gamebg=pygame.image.load(os.path.join('TILE', 'game-bg.png'))

#player overlay
tileplayer=pygame.image.load(os.path.join('TILE', 'player.png'))
tileplayerB=pygame.image.load(os.path.join('TILE', 'playerB.png'))
tileplayerL=pygame.image.load(os.path.join('TILE', 'playerL.png'))
tileplayerR=pygame.image.load(os.path.join('TILE', 'playerR.png'))
#shadowwall variants:
shadtileplayer=pygame.image.load(os.path.join('TILE', 'shadplayer.png'))
shadtileplayerB=pygame.image.load(os.path.join('TILE', 'shadplayerB.png'))
shadtileplayerL=pygame.image.load(os.path.join('TILE', 'shadplayerL.png'))
shadtileplayerR=pygame.image.load(os.path.join('TILE', 'shadplayerR.png'))

tilewall=pygame.image.load(os.path.join('TILE', 'wall.png'))

tilefloor=pygame.image.load(os.path.join('TILE', 'floor.png'))
tileexit=pygame.image.load(os.path.join('TILE', 'exit.png'))
tilewater=pygame.image.load(os.path.join('TILE', 'water.png'))
tilegrass=pygame.image.load(os.path.join('TILE', 'grass.png'))
tiledock=pygame.image.load(os.path.join('TILE', 'dock.png'))
tilebridge=pygame.image.load(os.path.join('TILE', 'bridge.png'))
tileroof1=pygame.image.load(os.path.join('TILE', 'roof1.png'))
tileinsidewall=pygame.image.load(os.path.join('TILE', 'insidewall.png'))
tilecarpet=pygame.image.load(os.path.join('TILE', 'carpet.png'))
tileredcarpet=pygame.image.load(os.path.join('TILE', 'redcarpet.png'))
tiletiledfloor=pygame.image.load(os.path.join('TILE', 'tilefloor.png'))
tileoutside=pygame.image.load(os.path.join('TILE', 'outsidein.png'))
tilebrickpath=pygame.image.load(os.path.join('TILE', 'brickpath.png'))
tilesand=pygame.image.load(os.path.join('TILE', 'sand.png'))
#(added batch-o-tiles 1)
tilecobblewall=pygame.image.load(os.path.join('TILE', 'cobblewall.png'))
tiledirt=pygame.image.load(os.path.join('TILE', 'dirt.png'))
tilestone=pygame.image.load(os.path.join('TILE', 'stone.png'))
tiledarkstone=pygame.image.load(os.path.join('TILE', 'darkstone.png'))
tilelava=pygame.image.load(os.path.join('TILE', 'lava.png'))
tilegreengoo=pygame.image.load(os.path.join('TILE', 'greengoo.png'))
#second interior set
tilehardwood=pygame.image.load(os.path.join('TILE', 'hardwoodfloor.png'))
tileconcretefloor=pygame.image.load(os.path.join('TILE', 'concretefloor.png'))
tilesteelfloor=pygame.image.load(os.path.join('TILE', 'steelfloor.png'))
tilegirderwall=pygame.image.load(os.path.join('TILE', 'girderwall.png'))

#skytiles
tilesky1=pygame.image.load(os.path.join('TILE', 'sky1.png'))

#overlay graphics
ovflowers=pygame.image.load(os.path.join('TILE', 'ovflowers.png'))
ovcrate=pygame.image.load(os.path.join('TILE', 'ovcrate.png'))
ovbuntowel=pygame.image.load(os.path.join('TILE', 'ovbuntowel.png'))
ovbunraft=pygame.image.load(os.path.join('TILE', 'ovbunraft.png'))
ovbunstand=pygame.image.load(os.path.join('TILE', 'ovbunstand.png'))
ovsink=pygame.image.load(os.path.join('TILE', 'ovsink.png'))
ovsinkr1=pygame.image.load(os.path.join('TILE', 'ovsinkr1.png'))
ovsinkr2=pygame.image.load(os.path.join('TILE', 'ovsinkr2.png'))
ovsinkr3=pygame.image.load(os.path.join('TILE', 'ovsinkr3.png'))

ovcounter=pygame.image.load(os.path.join('TILE', 'ovcounter.png'))
ovcounterr1=pygame.image.load(os.path.join('TILE', 'ovcounterr1.png'))
ovcounterr2=pygame.image.load(os.path.join('TILE', 'ovcounterr2.png'))
ovcounterr3=pygame.image.load(os.path.join('TILE', 'ovcounterr3.png'))

ovarrow=pygame.image.load(os.path.join('TILE', 'ovarrow.png'))

ovtoilet=pygame.image.load(os.path.join('TILE', 'ovtoilet.png'))
ovtoiletr1=pygame.image.load(os.path.join('TILE', 'ovtoiletr1.png'))
ovtoiletr2=pygame.image.load(os.path.join('TILE', 'ovtoiletr2.png'))
ovtoiletr3=pygame.image.load(os.path.join('TILE', 'ovtoiletr3.png'))

ovcat1=pygame.image.load(os.path.join('TILE', 'cat1.png'))
ovcat2=pygame.image.load(os.path.join('TILE', 'cat2.png'))
ovcat3=pygame.image.load(os.path.join('TILE', 'cat3.png'))

ovmouse1=pygame.image.load(os.path.join('TILE', 'mouse1.png'))
ovbulletin=pygame.image.load(os.path.join('TILE', 'ovbulletin.png'))
ovbulletinr1=pygame.image.load(os.path.join('TILE', 'ovbulletinr1.png'))
ovbulletinr2=pygame.image.load(os.path.join('TILE', 'ovbulletinr2.png'))
ovbulletinr3=pygame.image.load(os.path.join('TILE', 'ovbulletinr3.png'))

NPCballoon=pygame.image.load(os.path.join('TILE', 'NPCballoon.png'))
#overlay signs
signwater=pygame.image.load(os.path.join('TILE', 'signwater.png'))
signlava=pygame.image.load(os.path.join('TILE', 'signlava.png'))
signacid=pygame.image.load(os.path.join('TILE', 'signacid.png'))
signpool=pygame.image.load(os.path.join('TILE', 'signpool.png'))
signriver=pygame.image.load(os.path.join('TILE', 'signriver.png'))
signtree=pygame.image.load(os.path.join('TILE', 'signtree.png'))
signdiner=pygame.image.load(os.path.join('TILE', 'signdiner.png'))
signbeach=pygame.image.load(os.path.join('TILE', 'signbeach.png'))
signbun=pygame.image.load(os.path.join('TILE', 'signbun.png'))
signinfo=pygame.image.load(os.path.join('TILE', 'signinfo.png'))
signtask=pygame.image.load(os.path.join('TILE', 'signtask.png'))
#special shadows
wallshadow=pygame.image.load(os.path.join('TILE', 'wallshadow.png'))
landshadow=pygame.image.load(os.path.join('TILE', 'landshadow.png'))
wallliquidshadow=pygame.image.load(os.path.join('TILE', 'wallliquidshadow.png'))
#wall "side" hints
hinthedge=pygame.image.load(os.path.join('TILE', 'hinthedge.png'))
hintcobble=pygame.image.load(os.path.join('TILE', 'hintcobble.png'))
hintbuild=pygame.image.load(os.path.join('TILE', 'hintbuild.png'))
hintbuildgreen=pygame.image.load(os.path.join('TILE', 'hintbuildgreen.png'))

hintbuildout=pygame.image.load(os.path.join('TILE', 'hintbuildout.png'))
hintdoor=pygame.image.load(os.path.join('TILE', 'hintdoor.png'))

playerfuzzshad=pygame.image.load(os.path.join('TILE', 'playerfuzzshad.png'))
#gates
gateopen=pygame.image.load(os.path.join('TILE', 'gateopen.png'))
gateclosed=pygame.image.load(os.path.join('TILE', 'gateclosed.png'))
#switches
switchon=pygame.image.load(os.path.join('TILE', 'switchon.png'))
switchoff=pygame.image.load(os.path.join('TILE', 'switchoff.png'))

#hudfaces
hudfacehappy=pygame.image.load(os.path.join('TILE', 'hudfacehappy.png'))
hudfacesad=pygame.image.load(os.path.join('TILE', 'hudfacesad.png'))
hudfaceshock=pygame.image.load(os.path.join('TILE', 'hudfaceshock.png'))
hudfaceangry=pygame.image.load(os.path.join('TILE', 'hudfaceanger.png'))
hudfacecasual=pygame.image.load(os.path.join('TILE', 'hudfacecasual.png'))
hudfacebored=pygame.image.load(os.path.join('TILE', 'hudfacebored.png'))

winscreen=pygame.image.load(os.path.join('TILE', 'winscreen.png'))

# *.MAZE file data loader
print ("loading data from:" + mazefilepath)
tree = ET.parse(mazefilepath)
root = tree.getroot()
setuptag=root.find('setup')
playx=int((setuptag.find('startposx')).text)
playy=int((setuptag.find('startposy')).text)
viewfilterflg=setuptag.attrib.get('filter', "0")
if viewfilterflg=="1":
	filterA=setuptag.attrib.get('a')
	filterR=setuptag.attrib.get('r')
	filterB=setuptag.attrib.get('b')
	filterG=setuptag.attrib.get('g')
	viewfilter=pygame.Surface((80, 80))
	viewfiltertall=pygame.Surface((80, 88))
	viewfilter.fill((int(filterR), int(filterG), int(filterB)))
	viewfilter.set_alpha(int(filterA))
	viewfiltertall.fill((int(filterR), int(filterG), int(filterB)))
	viewfiltertall.set_alpha(int(filterA))
else:
	viewfilter=pygame.Surface((80, 80))
	viewfiltertall=pygame.Surface((80, 88))
	viewfiltertall.set_alpha(0)
	viewfilter.set_alpha(0)
mazemodpath=os.path.join("MAZE", ((root.find('maingrid')).text))
nodetag=root.find('nodes')
forktag=root.find('forks')
mazetitle=(setuptag.find('mazename')).text
print ("data loaded. \n")
debugset = ('1')
gameend = ('0')
CANTMOVE = ("Can't move in that direction.")
WINGAME = ("You win!")
lastmove="F"
inside=0

#define a simple font from the system font
simplefont = pygame.font.SysFont(None, 16)
simplefontB = pygame.font.SysFont(None, 24)

#draws tiles. used by tilegriddraw internally.
bgtext = simplefont.render(mazetitle, True, (5, 59, 186))
gamebg.blit(bgtext, (0, 0))
hudface="1"
def tileblit(xval, yval, tilestring, xfoo, yfoo, drawfox=0):
	tilepost=pygame.Surface((400, 400), SRCALPHA)
	if tilestring=="1":
		screensurf.blit(tilewall, (xval, (yval-8)))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="C":
		screensurf.blit(tilecobblewall, (xval, (yval-8)))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="0":
		screensurf.blit(tilefloor, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="e":
		screensurf.blit(tiledirt, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="S":
		screensurf.blit(tilestone, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="X":
		screensurf.blit(tilegreengoo, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="l":
		screensurf.blit(tilelava, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="z":
		screensurf.blit(tilesky1, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="D":
		screensurf.blit(tiledarkstone, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="3":
		screensurf.blit(tileexit, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="w":
		screensurf.blit(tilewater, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="g":
		screensurf.blit(tilegrass, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		#print "ping"
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
			#print "pong"
	if tilestring=="s":
		screensurf.blit(tilesand, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		#print "ping"
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
			#print "pong"
	if tilestring=="d":
		screensurf.blit(tiledock, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="B":
		screensurf.blit(tilebrickpath, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="b":
		screensurf.blit(tilebridge, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	#"inside" tiles below.
	if tilestring=="R":
		
		if inside==1:
			screensurf.blit(tileinsidewall, (xval, (yval-8)))
			Qinside=1
		else:
			screensurf.blit(tileroof1, (xval, (yval-8)))
			Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="c":
		
		if inside==1:
			Qinside=1
			screensurf.blit(tilecarpet, (xval, yval))
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="Q":
		
		if inside==1:
			Qinside=1
			screensurf.blit(tilegirderwall, (xval, (yval-8)))
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="P":
		
		if inside==1:
			screensurf.blit(tilesteelfloor, (xval, yval))
			Qinside=1
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="Z":
		
		if inside==1:
			screensurf.blit(tileconcretefloor, (xval, yval))
			Qinside=1
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="H":
		
		if inside==1:
			screensurf.blit(tilehardwood, (xval, yval))
			Qinside=1
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	
	if tilestring=="r":
		
		if inside==1:
			screensurf.blit(tileredcarpet, (xval, yval))
			Qinside=1
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="t":
		
		if inside==1:
			screensurf.blit(tiletiledfloor, (xval, yval))
			Qinside=1
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	#screensurf.blit(tilepost, (0, 0))
#new function to draw tile grid
def tilegriddraw2():
	xfoo=LEFTWARD3x
	yfoo=LEFTWARD3y
	tileblit(80, 20, LEFTWARD3, xfoo, yfoo)
	xfoo=RIGHTWARD3x
	yfoo=RIGHTWARD3y
	tileblit(240, 20, RIGHTWARD3, xfoo, yfoo)
	xfoo=FARLEFT3x
	yfoo=FARLEFT3y
	tileblit(0, 20, FARLEFT3, xfoo, yfoo)
	xfoo=FARRIGHT3x
	yfoo=FARRIGHT3y
	tileblit(320, 20, FARRIGHT3, xfoo, yfoo)
	xfoo=FORWARD2x
	yfoo=FORWARD2y
	tileblit(160, 20, FORWARD2, xfoo, yfoo)
	xfoo=LEFTWARD2x
	yfoo=LEFTWARD2y
	tileblit(80, 100, LEFTWARD2, xfoo, yfoo)
	xfoo=RIGHTWARD2x
	yfoo=RIGHTWARD2y
	tileblit(240, 100, RIGHTWARD2, xfoo, yfoo)
	xfoo=FARLEFT2x
	yfoo=FARLEFT2y
	tileblit(0, 100, FARLEFT2, xfoo, yfoo)
	xfoo=FARRIGHT2x
	yfoo=FARRIGHT2y
	tileblit(320, 100, FARRIGHT2, xfoo, yfoo)
	xfoo=FORWARDx
	yfoo=FORWARDy
	tileblit(160, 100, FORWARD, xfoo, yfoo)
	xfoo=CENTERx
	yfoo=CENTERy
	tileblit(160, 180, CENTER, xfoo, yfoo, 1)
	xfoo=LEFTWARDx
	yfoo=LEFTWARDy
	tileblit(80, 180, LEFTWARD, xfoo, yfoo)
	xfoo=RIGHTWARDx
	yfoo=RIGHTWARDy
	tileblit(240, 180, RIGHTWARD, xfoo, yfoo)
	xfoo=FARLEFTx
	yfoo=FARLEFTy
	tileblit(0, 180, FARLEFT, xfoo, yfoo)
	xfoo=FARRIGHTx
	yfoo=FARRIGHTy
	tileblit(320, 180, FARRIGHT, xfoo, yfoo)
	xfoo=LEFTWARD0x
	yfoo=LEFTWARD0y
	tileblit(80, 260, LEFTWARD0, xfoo, yfoo)
	xfoo=RIGHTWARD0x
	yfoo=RIGHTWARD0y
	tileblit(240, 260, RIGHTWARD0, xfoo, yfoo)
	xfoo=FARLEFT0x
	yfoo=FARLEFT0y
	tileblit(0, 260, FARLEFT0, xfoo, yfoo)
	xfoo=FARRIGHT0x
	yfoo=FARRIGHT0y
	tileblit(320, 260, FARRIGHT0, xfoo, yfoo)
	xfoo=BACKWARDx
	yfoo=BACKWARDy
	tileblit(160, 260, BACKWARD, xfoo, yfoo)
	xfoo=LEFTWARDZx
	yfoo=LEFTWARDZy
	tileblit(80, 340, LEFTWARDZ, xfoo, yfoo)
	xfoo=RIGHTWARDZx
	yfoo=RIGHTWARDZy
	tileblit(240, 340, RIGHTWARDZ, xfoo, yfoo)
	xfoo=FARLEFTZx
	yfoo=FARLEFTZy
	tileblit(0, 340, FARLEFTZ, xfoo, yfoo)
	xfoo=FARRIGHTZx
	yfoo=FARRIGHTZy
	tileblit(320, 340, FARRIGHTZ, xfoo, yfoo)
	xfoo=BACKWARDZx
	yfoo=BACKWARDZy
	tileblit(160, 340, BACKWARDZ, xfoo, yfoo)
	
	
	#if viewfilterflg=="1":
	#	screensurf.blit(viewfilter, (0, 20))
	labelscan()

def ovrot(Qrot, Qgfx):
	if Qrot=="1":
		Qgfx=pygame.transform.rotate(Qgfx, 90)
	if Qrot=="2":
		Qgfx=pygame.transform.rotate(Qgfx, 180)
	if Qrot=="3":
		Qgfx=pygame.transform.rotate(Qgfx, 270)
	return Qgfx

def overlayblit(overlaytype, Qrotate="0"):
	if overlaytype=="flowers":
		return(ovrot(Qrotate, ovflowers), 0)
	if overlaytype=="2":
		return(ovrot(Qrotate, ovbuntowel), 0)
	if overlaytype=="3":
		return(ovrot(Qrotate, ovbunraft), 0)
	if overlaytype=="4":
		return(ovrot(Qrotate, ovbunstand), 0)
	if overlaytype=="sink":
		if Qrotate=="1":
			return(ovsinkr1, 1)
		if Qrotate=="2":
			return(ovsinkr2, 1)
		if Qrotate=="3":
			return(ovsinkr3, 1)
		else:
			return(ovsink, 1) #TWEAKS DONE
	if overlaytype=="counter":
		if Qrotate=="1":
			return(ovcounterr1, 1)
		if Qrotate=="2":
			return(ovcounterr2, 1)
		if Qrotate=="3":
			return(ovcounterr3, 1)
		else:
			return(ovcounter, 1) #TWEAKS DONE
	if overlaytype=="toilet":
		if Qrotate=="1":
			return(ovtoiletr1, 1)
		if Qrotate=="2":
			return(ovtoiletr2, 1)
		if Qrotate=="3":
			return(ovtoiletr3, 1)
		else:
			return(ovtoilet, 1) #TWEAKS DONE
	if overlaytype=="crate":
		return(ovrot(Qrotate, ovcrate), 1)# TWEAKING DONE
	if overlaytype=="cat1":
		return(ovrot(Qrotate, ovcat1), 0)
	if overlaytype=="cat2":
		return(ovrot(Qrotate, ovcat2), 0)
	if overlaytype=="cat3":
		return(ovrot(Qrotate, ovcat3), 0)
	if overlaytype=="mouse1":
		return(ovrot(Qrotate, ovmouse1), 0)
	if overlaytype=="arrow":
		return(ovrot(Qrotate, ovarrow), 0)
	if overlaytype=="signwater":
		return(ovrot(Qrotate, signwater), 0)
	if overlaytype=="signlava":
		return(ovrot(Qrotate, signlava), 0)
	if overlaytype=="signacid":
		return(ovrot(Qrotate, signacid), 0)
	if overlaytype=="signbeach":
		return(ovrot(Qrotate, signbeach), 0)
	if overlaytype=="signdiner":
		return(ovrot(Qrotate, signdiner), 0)
	if overlaytype=="signpool":
		return(ovrot(Qrotate, signpool), 0)
	if overlaytype=="signriver":
		return(ovrot(Qrotate, signriver), 0)
	if overlaytype=="signtree":
		return(ovrot(Qrotate, signtree), 0)
	if overlaytype=="signbun":
		return(ovrot(Qrotate, signbun), 0)
	if overlaytype=="signinfo":
		return(ovrot(Qrotate, signinfo), 0)
	if overlaytype=="signtask":
		return(ovrot(Qrotate, signtask), 0)
	if overlaytype=="NPCballoon":
		return(ovrot(Qrotate, NPCballoon), 0)
	if overlaytype=="bulletin":
		return(ovrot(Qrotate, ovbulletin), 1) #needs separate rotate views and 8 pix offset
	

def overlayscan():
	for node in nodetag.findall("overlay"):
		QX=int(node.attrib.get('x'))
		QY=int(node.attrib.get('y'))
		Qtype=node.attrib.get('type')
		Qvis=node.attrib.get('area')
		if Qvis=="i" and inside==1:
			ovvis=1
		elif Qvis=="o" and inside==0:
			ovvis=1
		elif Qvis=="b":
			ovvis=1
		else:
			ovvis=0
		labtext=overlayblit(Qtype)
		if ovvis==1:
			if QX==LEFTWARD3x and QY==LEFTWARD3y:
				screensurf.blit(labtext, (80, 20))
			if QX==RIGHTWARD3x and QY==RIGHTWARD3y:
				screensurf.blit(labtext, (240, 20))
			if QX==FARLEFT3x and QY==FARLEFT3y:
				screensurf.blit(labtext, (0, 20))
			if QX==FARRIGHT3x and QY==FARRIGHT3y:
				screensurf.blit(labtext, (320, 20))
			if QX==FORWARD2x and QY==FORWARD2y:
				screensurf.blit(labtext, (160, 20))
			if QX==LEFTWARD2x and QY==LEFTWARD2y:
				screensurf.blit(labtext, (80, 100))
			if QX==RIGHTWARD2x and QY==RIGHTWARD2y:
				screensurf.blit(labtext, (240, 100))
			if QX==FARLEFT2x and QY==FARLEFT2y:
				screensurf.blit(labtext, (0, 100))
			if QX==FARRIGHT2x and QY==FARRIGHT2y:
				screensurf.blit(labtext, (320, 100))
			if QX==FORWARDx and QY==FORWARDy:
				screensurf.blit(labtext, (160, 100))
			if QX==LEFTWARDx and QY==LEFTWARDy:
				screensurf.blit(labtext, (80, 180))
			if QX==CENTERx and QY==CENTERy:
				screensurf.blit(labtext, (160, 180))
			if QX==RIGHTWARDx and QY==RIGHTWARDy:
				screensurf.blit(labtext, (240, 180))
			if QX==FARLEFTx and QY==FARLEFTy:
				screensurf.blit(labtext, (0, 180))
			if QX==FARRIGHTx and QY==FARRIGHTy:
				screensurf.blit(labtext, (320, 180))
			if QX==LEFTWARD0x and QY==LEFTWARD0y:
				screensurf.blit(labtext, (80, 260))
			if QX==RIGHTWARD0x and QY==RIGHTWARD0y:
				screensurf.blit(labtext, (240, 260))
			if QX==FARLEFT0x and QY==FARLEFT0y:
				screensurf.blit(labtext, (0, 260))
			if QX==FARRIGHT0x and QY==FARRIGHT0y:
				screensurf.blit(labtext, (320, 260))
			if QX==BACKWARDx and QY==BACKWARDy:
				screensurf.blit(labtext, (160, 260))
	
def overlayscanB(xval, yval, xco, yco, drawfox=0, Qinside=0):
	
	
	for node in nodetag.findall("switch"):
		if int(node.attrib.get('x'))==xval and int(node.attrib.get('y'))==yval:
			keyid=node.attrib.get('keyid', "0")
			Qvis=node.attrib.get('area', "b")
			if Qvis=="i" and inside==1:
				ovvis=1
			elif Qvis=="o" and inside==0:
				ovvis=1
			elif Qvis=="b":
				ovvis=1
			else:
				ovvis=0
			
			if keyid!="0" and ovvis==1:
				if not keyid in keylist:
					screensurf.blit(switchoff, (xco, yco))
				elif keyid in keylist:
					screensurf.blit(switchon, (xco, yco))
	yshad=(yval + 1)
	shadblk=lookpoint(xval, yshad)
	curblk=lookpoint(xval, yval)
	nextblock=lookpoint(xval, (yval - 1))
	#depth hint engine:
	if shadblk=="1" or shadblk=="R" or shadblk=="r"  or shadblk=="c"   or shadblk=="t" or shadblk=="C" or shadblk=="Q" or shadblk=="P" or shadblk=="Z" or shadblk=="H":
		if curblk!="1" and curblk!="R" and curblk!="C" and curblk!="c" and curblk!="t" and curblk!="r" and curblk!="Q" and curblk!="P" and curblk!="Z" and curblk!="H":
			if shadblk=="R" or shadblk=="Q":
				screensurf.blit(hintbuildout, (xco, (yco-8)))
			if shadblk=="1":
				screensurf.blit(hinthedge, (xco, (yco-8)))
			if shadblk=="C":
				screensurf.blit(hintcobble, (xco, (yco-8)))
			if shadblk=="r" or shadblk=="c" or shadblk=="t" or shadblk=="P" or shadblk=="Z" or shadblk=="H":
				if inside==0:
					screensurf.blit(hintdoor, (xco, (yco-8)))
	if inside==1:
		if shadblk=="R" or shadblk=="Q":
			if curblk=="t":
				screensurf.blit(hintbuild, (xco, (yco-8)))
			if curblk=="c":
				screensurf.blit(hintbuild, (xco, (yco-8)))
			if curblk=="r":
				screensurf.blit(hintbuild, (xco, (yco-8)))
			if curblk=="P":
				screensurf.blit(hintbuild, (xco, (yco-8)))
			if curblk=="Z":
				screensurf.blit(hintbuild, (xco, (yco-8)))
			if curblk=="H":
				screensurf.blit(hintbuildgreen, (xco, (yco-8)))
	for node in nodetag.findall("gate"):
		if int(node.attrib.get('x'))==xval and int(node.attrib.get('y'))==yval:
			keyid=node.attrib.get('keyid', "0")
			Qvis=node.attrib.get('area', "b")
			if Qvis=="i" and inside==1:
				ovvis=1
			elif Qvis=="o" and inside==0:
				ovvis=1
			elif Qvis=="b":
				ovvis=1
			else:
				ovvis=0
			if ovvis==1:
				if keyid!="0":
					if keyid in keylist:
						screensurf.blit(gateopen, (xco, (yco-8)))
					else:
						screensurf.blit(gateclosed, (xco, (yco-8)))
	for node in nodetag.findall("overlay"):
		xval=int(xval)
		yval=int(yval)
		QX=int(node.attrib.get('x'))
		QY=int(node.attrib.get('y'))
		Qtype=node.attrib.get('type')
		Qvis=node.attrib.get('area')
		Qrotate=node.attrib.get('rotate', "0")
		
		#keyid=node.attrib.get('keyid', "0")
		onkey=node.attrib.get('onkey', "0")
		offkey=node.attrib.get('offkey', "0")
		if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
			#if not keyid in keylist:
			#	keylist.extend([keyid])
			if Qvis=="i" and inside==1:
				ovvis=1
			elif Qvis=="o" and inside==0:
				ovvis=1
			elif Qvis=="b":
				ovvis=1
			else:
				ovvis=0
		else:
			ovvis=0
		labtextQ=overlayblit(Qtype, Qrotate)
		labtext=labtextQ[0]
		offsetflg=labtextQ[1]
		if ovvis==1:
			if QX==xval and QY==yval:
				#if Qrotate=="1":
				#	labtext=pygame.transform.rotate(labtext, 90)
				#if Qrotate=="2":
				#	labtext=pygame.transform.rotate(labtext, 180)
				#if Qrotate=="3":
				#	labtext=pygame.transform.rotate(labtext, 270)
				if offsetflg==0:
					screensurf.blit(labtext, (xco, yco))
				else:
					#print "foobar114"
					screensurf.blit(labtext, (xco, (yco-8)))
	#shadow engine
	if 0==0:
		if shadblk=="1" or shadblk=="R" or shadblk=="r"  or shadblk=="c"   or shadblk=="t" or shadblk=="C" or shadblk=="Q" or shadblk=="P" or shadblk=="Z" or shadblk=="H":
			if curblk!="1" and curblk!="R" and curblk!="C" and curblk!="c" and curblk!="t" and curblk!="r" and curblk!="Q" and curblk!="P" and curblk!="Z" and curblk!="H" and curblk!="z":
				if curblk=="w" or curblk=="l" or curblk=="X":
					screensurf.blit(wallliquidshadow, (xco, yco))
				else:
					screensurf.blit(wallshadow, (xco, yco))
		elif shadblk!="w" and shadblk!="l" and shadblk!="X" and shadblk!="x":
			if curblk=="w" or curblk=="l" or curblk=="X":
				screensurf.blit(landshadow, (xco, yco))
	
	
	if drawfox==1:
		screensurf.blit(playerfuzzshad, (160, 180))
		if inside==1:
			if lastmove=="F":
				screensurf.blit(tileplayer, (160, 180))
			if lastmove=="B":
				screensurf.blit(tileplayerB, (160, 180))
			if lastmove=="L":
				screensurf.blit(tileplayerL, (160, 180))
			if lastmove=="R":
				screensurf.blit(tileplayerR, (160, 180))
		if inside==0:
			yshad=(playy + 1)
			shadblk=lookpoint(playx, yshad)
			curblk=lookpoint(playx, playy)
			if shadblk=="1" or shadblk=="R"  or shadblk=="r"  or shadblk=="c"   or shadblk=="t" or shadblk=="Q" or shadblk=="P" or shadblk=="Z" or shadblk=="H" or shadblk=="C":
				if curblk!="1" and curblk!="R" and curblk!="c" and curblk!="t" and curblk!="r" and curblk!="Q" and curblk!="P" and curblk!="H" and curblk!="Z" and curblk!="C":
					if lastmove=="F":
						screensurf.blit(shadtileplayer, (160, 180))
					if lastmove=="B":
						screensurf.blit(shadtileplayerB, (160, 180))
					if lastmove=="L":
						screensurf.blit(shadtileplayerL, (160, 180))
					if lastmove=="R":
						screensurf.blit(shadtileplayerR, (160, 180))
				else:
					if lastmove=="F":
						screensurf.blit(tileplayer, (160, 180))
					if lastmove=="B":
						screensurf.blit(tileplayerB, (160, 180))
					if lastmove=="L":
						screensurf.blit(tileplayerL, (160, 180))
					if lastmove=="R":
						screensurf.blit(tileplayerR, (160, 180))
			else:
				if lastmove=="F":
					screensurf.blit(tileplayer, (160, 180))
				if lastmove=="B":
					screensurf.blit(tileplayerB, (160, 180))
				if lastmove=="L":
					screensurf.blit(tileplayerL, (160, 180))
				if lastmove=="R":
					screensurf.blit(tileplayerR, (160, 180))
	if Qinside==0:
		if nextblock=="c" or nextblock=="t" or nextblock=="r" or nextblock=="P" or nextblock=="Z" or nextblock=="H":
			screensurf.blit(viewfiltertall, (xco, (yco-8)))
			#if inside==1:
			#	screensurf.blit(tileoutside, (xco, (yco-8)))
		else:
			screensurf.blit(viewfilter, (xco, (yco-8)))
			#if inside==1:
			#	screensurf.blit(tileoutside, (xco, (yco-8)))
			
	
	
	
def labelscan():
	for node in nodetag.findall("label"):
		QX=int(node.attrib.get('x'))
		QY=int(node.attrib.get('y'))
		Qvis=node.attrib.get('area')
		if Qvis=="i" and inside==1:
			labvis=1
		elif Qvis=="o" and inside==0:
			labvis=1
		elif Qvis=="b":
			labvis=1
		else:
			labvis=0
		
		if labvis==1:
			if QX==LEFTWARD3x and QY==LEFTWARD3y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (80, 20))
			if QX==RIGHTWARD3x and QY==RIGHTWARD3y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (240, 20))
			if QX==FARLEFT3x and QY==FARLEFT3y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (0, 20))
			if QX==FARRIGHT3x and QY==FARRIGHT3y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (320, 20))
			if QX==FORWARD2x and QY==FORWARD2y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (160, 20))
			if QX==LEFTWARD2x and QY==LEFTWARD2y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (80, 100))
			if QX==RIGHTWARD2x and QY==RIGHTWARD2y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (240, 100))
			if QX==FARLEFT2x and QY==FARLEFT2y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (0, 100))
			if QX==FARRIGHT2x and QY==FARRIGHT2y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (320, 100))
			if QX==FORWARDx and QY==FORWARDy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (160, 100))
			if QX==LEFTWARDx and QY==LEFTWARDy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (80, 180))
			if QX==CENTERx and QY==CENTERy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (160, 180))
			if QX==RIGHTWARDx and QY==RIGHTWARDy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (240, 180))
			if QX==FARLEFTx and QY==FARLEFTy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (0, 180))
			if QX==FARRIGHTx and QY==FARRIGHTy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (320, 180))
			if QX==LEFTWARD0x and QY==LEFTWARD0y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (80, 260))
			if QX==RIGHTWARD0x and QY==RIGHTWARD0y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (240, 260))
			if QX==FARLEFT0x and QY==FARLEFT0y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (0, 260))
			if QX==FARRIGHT0x and QY==FARRIGHT0y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (320, 260))
			if QX==BACKWARDx and QY==BACKWARDy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (160, 260))
	
#old function to draw tile grid

#function used to wait for a keystroke at the win screen
def winscreenwait():
	while True:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				return()

def convscreenwait():
	while True:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key != K_UP and event.key != K_DOWN and event.key != K_LEFT and event.key != K_RIGHT and event.key != K_w and event.key != K_a and event.key != K_s and  event.key != K_d:
				return([0, 0, 0])
			if event.type == VIDEORESIZE:
				sxh=event.h
				if sxh<400:
					sxh=400
				sxratio=(sxh-400)
				sxw=int(sxratio + 400)
				screensurfdex=pygame.display.set_mode((sxw, sxh), RESIZABLE)
				return([1, sxw, sxh])

#datapoint lookup function. used to read data points from the main .grid file.
#when the point i out-of-range. 1 is returned.
def lookpoint(lookptx, lookpty):
	lineycnt=1
	linexcnt=1
	
	lookupdef=setuptag.attrib.get("defaulttile", "1")
	lookuppointis=lookupdef
	m = open(mazemodpath)
	for lineylst in m:
		if lineycnt==lookpty:
			for linexlst in lineylst:
				if linexcnt==lookptx:
					lookuppointis = linexlst
				linexcnt += 1
		lineycnt += 1
	if lookuppointis=="\n":
		lookuppointis=lookupdef
	return (lookuppointis)

#used by wall detection logic. modified to simplify wall detection.
#wether a tile is walkable is determined HERE
def lookpointB(lookptx, lookpty):
	lineycnt=1
	linexcnt=1
	lookuppointis='1'
	m = open(mazemodpath)
	for lineylst in m:
		if lineycnt==lookpty:
			for linexlst in lineylst:
				if linexcnt==lookptx:
					lookuppointis = linexlst
				linexcnt += 1
		lineycnt += 1
	if lookuppointis=="w":
		lookuppointis='1'
	if lookuppointis=="l":
		lookuppointis='1'
	if lookuppointis=="z":
		lookuppointis='1'
	if lookuppointis=="X":
		lookuppointis='1'
	if lookuppointis=="C":
		lookuppointis='1'
	if lookuppointis=="Q":
		lookuppointis='1'
	if lookuppointis=="\n":
		lookuppointis='1'
	if lookuppointis=="g":
		lookuppointis='0'
	if lookuppointis=="s":
		lookuppointis='0'
	if lookuppointis=="e":
		lookuppointis='0'
	if lookuppointis=="S":
		lookuppointis='0'
	if lookuppointis=="D":
		lookuppointis='0'
	if lookuppointis=="d":
		lookuppointis='0'
	if lookuppointis=="B":
		lookuppointis='0'
	if lookuppointis=="b":
		lookuppointis='0'
	if lookuppointis=="R":
		lookuppointis='1'
	if lookuppointis=="c":
		lookuppointis='0'
	if lookuppointis=="r":
		lookuppointis='0'
	if lookuppointis=="t":
		lookuppointis='0'
	if lookuppointis=="P":
		lookuppointis='0'
	if lookuppointis=="Z":
		lookuppointis='0'
	if lookuppointis=="H":
		lookuppointis='0'
	for node in nodetag.findall("gate"):
		if int(node.attrib.get('x'))==lookptx and int(node.attrib.get('y'))==lookpty:
			keyid=node.attrib.get('keyid', "0")
			if keyid!="0":
				if keyid in keylist:
					lookuppointis="0"
				else:
					lookuppointis="1"
			
			break
	for node in nodetag.findall("walkable"):
		if int(node.attrib.get('x'))==lookptx and int(node.attrib.get('y'))==lookpty:
			onkey=node.attrib.get('onkey', "0")
			offkey=node.attrib.get('offkey', "0")
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				showlooktext=1
				lookuppointis=node.attrib.get('force')
				break
	return (lookuppointis)
	
def debugcon():
	print "TEXT MAZE 5 DEBUG CONSOLE ACTIVE"
	print "type return to return to gameplay."
	USRCMD="null"
	while USRCMD!=("return"):
		USRENTRYLINE = raw_input(':')
		USRLST=USRENTRYLINE.split(" ", 1)
		try:
			USRCMD=(USRLST[0])
		except IndexError:
			USRCMD=""
		try:
			USRTEXT=(USRLST[1])
		except IndexError:
			USRTEXT=""
		if (USRCMD==("keys")):
			print "current keylist:"
			print keylist
		if (USRCMD==("info")):
			print "playx:" + str(playx)
			print "playy:" + str(playy)
			print "mazexml:" + mazefilepath
			print "mazegrid:" + mazemodpath
			print "mazename:" + mazetitle
			print "defaulttile: " + setuptag.attrib.get("defaulttile", "1")
			print "startx: " + (setuptag.find('startposx')).text
			print "starty: " + (setuptag.find('startposy')).text
		if (USRCMD==("give") and USRTEXT!=""):
			if not USRTEXT in keylist:
				keylist.extend([USRTEXT])
		if (USRCMD==("take") and USRTEXT!=""):
			if USRTEXT in keylist:
				keylist.remove(USRTEXT)
		if (USRCMD==("help")):
			print '''Help:

keys: print current keylist
give [keyid]: grant a keyid
take [keyid]: take a keyid
info: engine status info.)
return: return to gameplay.
help: this text.
(be sure to double check any manual changes!)
'''
#function that draws text at the bottom of the display
def drawfoottext(textto, linemode):
	text = simplefont.render(textto, True, (255, 255, 255), (0, 0, 0))
	if linemode==0:
		screensurf.blit(text, (0, 340))
	if linemode==1:
		screensurf.blit(text, (0, 353))
#function that draws text at the top of the display
def drawheadertext(textto, linemode):
	text = simplefont.render(textto, True, (255, 255, 255), (0, 0, 0))
	if linemode==0:
		screensurf.blit(text, (0, 0))
	if linemode==1:
		screensurf.blit(text, (0, 12))
#main input reading function
showlooktext=0
def keyread():
	while True:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_w:
				return(FORWARDWORDBIND)
			if event.type == KEYDOWN and event.key == K_a:
				return(LEFTWORDBIND)
			if event.type == KEYDOWN and event.key == K_s:
				return(BACKWARDWORDBIND)
			if event.type == KEYDOWN and event.key == K_d:
				return(RIGHTWODBIND)
			if event.type == KEYDOWN and event.key == K_q:
				return(QUITWORDBIND)
			if event.type == QUIT:
				return(QUITWORDBIND)
			if event.type == KEYDOWN and event.key == K_UP and (pygame.key.get_mods() & KMOD_SHIFT or pygame.key.get_mods() & KMOD_CAPS) and DEBUG==1:
				return("debugF")
			if event.type == KEYDOWN and event.key == K_LEFT and (pygame.key.get_mods() & KMOD_SHIFT or pygame.key.get_mods() & KMOD_CAPS) and DEBUG==1:
				return("debugL")
			if event.type == KEYDOWN and event.key == K_DOWN and (pygame.key.get_mods() & KMOD_SHIFT or pygame.key.get_mods() & KMOD_CAPS) and DEBUG==1:
				return("debugB")
			if event.type == KEYDOWN and event.key == K_RIGHT and (pygame.key.get_mods() & KMOD_SHIFT or pygame.key.get_mods() & KMOD_CAPS) and DEBUG==1:
				return("debugR")
			if event.type == KEYDOWN and event.key == K_z and pygame.key.get_mods() & KMOD_SHIFT and DEBUG==1:
				return("debugcon")
			if event.type == KEYDOWN and event.key == K_UP:
				return(FORWARDWORDBIND)
			if event.type == KEYDOWN and event.key == K_LEFT:
				return(LEFTWORDBIND)
			if event.type == KEYDOWN and event.key == K_DOWN:
				return(BACKWARDWORDBIND)
			if event.type == KEYDOWN and event.key == K_RIGHT:
				return(RIGHTWODBIND)
			if event.type == KEYDOWN and event.key == K_1:
				return("resize1")
			if event.type == KEYDOWN and event.key == K_2:
				return("resize2")
			if event.type == KEYDOWN and event.key == K_3:
				return("resize3")
			if event.type == VIDEORESIZE:
				sxh=event.h
				if sxh<400:
					sxh=400
				sxratio=(sxh-400)
				sxw=int(sxratio + 400)
				screensurfdex=pygame.display.set_mode((sxw, sxh), RESIZABLE)
				return("evresize")
			if event.type == KEYDOWN and event.key == K_l:
				return("l")
			if event.type == KEYDOWN and event.key == K_t:
				return("t")

def popuptext(textto):
	text = simplefontB.render(textto, True, (255, 255, 255), (0, 0, 0))
	textbox = text.get_rect()
	textbox.centerx=screensurf.get_rect().centerx
	textbox.centery=380
	screensurf.blit(text, textbox)
	
	
def convdup(convtext):
	textchunk=""
	Qscrnx=scrnx
	Qscrny=scrny
	tiptextmask=simplefontB.render(tiptext, True, (0, 0, 0), (0, 0, 0))
	tiptextmaskbox = tiptextmask.get_rect()
	tiptextmaskbox.centerx=screensurf.get_rect().centerx
	tiptextmaskbox.centery=380
	
	screensurf.blit(tiptextmask, tiptextmaskbox)
	textcont=(convtext + "\n")
	screensurfbak=screensurf.copy()
	fodchange=0
	for texch in textcont:
		#print texch
		if texch=="\n":
			popuptext(textchunk)
			textchunk=""
			screensurfQ=pygame.transform.scale(screensurf, (Qscrnx, Qscrny))
			screensurfdex.blit(screensurfQ, (0, 0))
			pygame.display.update()
			retwile=0
			retwile=convscreenwait()
			if retwile[0]==1:
				Qscrnx=retwile[1]
				Qscrny=retwile[2]
				fodchange=1
			
			screensurf.blit(screensurfbak, (0, 0))
			#print "ping"
		else:
			textchunk=(textchunk + texch)
			#print "pong"
	return(fodchange)


#old test data
#if lookpoint(2, 2)==('0'):
#	print ('blah')
#print (lookpoint(2, 2))
cantmoveflg=0
#main loop
forksanity=0
tiptext=""
showtiptext=0
hudfacedef="1"
forksanitycheck=0
points=0
keylist=["null"]
keybak=["null"]
skiploop=1
loopskipstop=0
while gameend==('0'):
	#POV coordinate determination
	#stageZ
	
	POVbackxZ = playx
	POVbackyZ = playy - 2
	POVleftxZ = playx + 1
	POVleftyZ = playy - 2
	fPOVleftxZ = playx + 2
	fPOVleftyZ = playy - 2
	POVrightxZ = playx - 1
	POVrightyZ = playy - 2
	fPOVrightxZ = playx - 2
	fPOVrightyZ = playy - 2
	#stage0
	POVleftx0 = playx + 1
	POVlefty0 = playy - 1
	fPOVleftx0 = playx + 2
	fPOVlefty0 = playy - 1
	POVrightx0 = playx - 1
	POVrighty0 = playy - 1
	fPOVrightx0 = playx - 2
	fPOVrighty0 = playy - 1
	#stage1
	POVforwardx = playx
	POVforwardy = playy + 1
	POVbackx = playx
	POVbacky = playy - 1
	POVleftx = playx + 1
	POVlefty = playy
	POVrightx = playx - 1
	POVrighty = playy
	fPOVleftx = playx + 2
	fPOVlefty = playy
	fPOVrightx = playx - 2
	fPOVrighty = playy
	#stage2
	POVleftx2 = playx + 1
	POVlefty2 = playy + 1
	POVrightx2 = playx - 1
	POVrighty2 = playy + 1
	fPOVleftx2 = playx + 2
	fPOVlefty2 = playy + 1
	fPOVrightx2 = playx - 2
	fPOVrighty2 = playy + 1
	POVforwardx2 = playx
	POVforwardy2 = playy + 2
	#stage3
	POVleftx3 = playx + 1
	POVlefty3 = playy + 2
	POVrightx3 = playx - 1
	POVrighty3 = playy + 2
	fPOVleftx3 = playx + 2
	fPOVlefty3 = playy + 2
	fPOVrightx3 = playx - 2
	fPOVrighty3 = playy + 2
	POVforwardx3 = playx
	POVforwardy3 = playy + 3
	#POV point lookup
	#stageZ
	LEFTWARDZ = lookpoint(POVleftxZ, POVleftyZ)
	LEFTWARDZx=POVleftxZ
	LEFTWARDZy=POVleftyZ
	RIGHTWARDZ = lookpoint(POVrightxZ, POVrightyZ)
	RIGHTWARDZx=POVrightxZ
	RIGHTWARDZy=POVrightyZ
	FARLEFTZ = lookpoint(fPOVleftxZ, fPOVleftyZ)
	FARLEFTZx=fPOVleftxZ
	FARLEFTZy=fPOVleftyZ
	FARRIGHTZ = lookpoint(fPOVrightxZ, fPOVrightyZ)
	FARRIGHTZx=fPOVrightxZ
	FARRIGHTZy=fPOVrightyZ
	BACKWARDZ = lookpoint(POVbackxZ, POVbackyZ)
	BACKWARDZx=POVbackxZ
	BACKWARDZy=POVbackyZ
	#stage0
	LEFTWARD0 = lookpoint(POVleftx0, POVlefty0)
	LEFTWARD0x=POVleftx0
	LEFTWARD0y=POVlefty0
	RIGHTWARD0 = lookpoint(POVrightx0, POVrighty0)
	RIGHTWARD0x=POVrightx0
	RIGHTWARD0y=POVrighty0
	FARLEFT0 = lookpoint(fPOVleftx0, fPOVlefty0)
	FARLEFT0x=fPOVleftx0
	FARLEFT0y=fPOVlefty0
	FARRIGHT0 = lookpoint(fPOVrightx0, fPOVrighty0)
	FARRIGHT0x=fPOVrightx0
	FARRIGHT0y=fPOVrighty0
	#stage1
	FORWARD = lookpoint(POVforwardx, POVforwardy)
	FORWARDx=POVforwardx
	FORWARDy=POVforwardy
	BACKWARD = lookpoint(POVbackx, POVbacky)
	BACKWARDx=POVbackx
	BACKWARDy=POVbacky
	LEFTWARD = lookpoint(POVleftx, POVlefty)
	LEFTWARDx=POVleftx
	LEFTWARDy=POVlefty
	RIGHTWARD = lookpoint(POVrightx, POVrighty)
	RIGHTWARDx=POVrightx
	RIGHTWARDy=POVrighty
	FARLEFT = lookpoint(fPOVleftx, fPOVlefty)
	FARLEFTx=fPOVleftx
	FARLEFTy=fPOVlefty
	FARRIGHT = lookpoint(fPOVrightx, fPOVrighty)
	FARRIGHTx=fPOVrightx
	FARRIGHTy=fPOVrighty
	#stage2
	FORWARD2 = lookpoint(POVforwardx2, POVforwardy2)
	FORWARD2x=POVforwardx2
	FORWARD2y=POVforwardy2
	LEFTWARD2 = lookpoint(POVleftx2, POVlefty2)
	LEFTWARD2x=POVleftx2
	LEFTWARD2y=POVlefty2
	RIGHTWARD2 = lookpoint(POVrightx2, POVrighty2)
	RIGHTWARD2x=POVrightx2
	RIGHTWARD2y=POVrighty2
	FARLEFT2 = lookpoint(fPOVleftx2, fPOVlefty2)
	FARLEFT2x=fPOVleftx2
	FARLEFT2y=fPOVlefty2
	FARRIGHT2 = lookpoint(fPOVrightx2, fPOVrighty2)
	FARRIGHT2x=fPOVrightx2
	FARRIGHT2y=fPOVrighty2
	#stage3
	FORWARD3 = lookpoint(POVforwardx3, POVforwardy3)
	FORWARD3x=POVforwardx3
	FORWARD3y=POVforwardy3
	LEFTWARD3 = lookpoint(POVleftx3, POVlefty3)
	LEFTWARD3x=POVleftx3
	LEFTWARD3y=POVlefty3
	RIGHTWARD3 = lookpoint(POVrightx3, POVrighty3)
	RIGHTWARD3x=POVrightx3
	RIGHTWARD3y=POVrighty3
	FARLEFT3 = lookpoint(fPOVleftx3, fPOVlefty3)
	FARLEFT3x=fPOVleftx3
	FARLEFT3y=fPOVlefty3
	FARRIGHT3 = lookpoint(fPOVrightx3, fPOVrighty3)
	FARRIGHT3x=fPOVrightx3
	FARRIGHT3y=fPOVrighty3
	
	CENTER = lookpoint(playx, playy)
	CENTERx=playx
	CENTERy=playy
	
	#inside view tiles declared here (walls should not be specified)
	if CENTER=="c" or CENTER=="r" or CENTER=="t" or CENTER=="P" or CENTER=="Z" or CENTER=="H":
		inside=1
	elif CENTER=="3":
		print "nochange intereor flag"
	else:
		inside=0
	#if debugset==('1'):
	#	print ("F:" + FORWARD + " B:" + BACKWARD)
	#	print ("L:" + LEFTWARD + " R:" + RIGHTWARD)
	#	print ("F2:" + FORWARD2 + " L2:" + LEFTWARD2 + " R2:" + RIGHTWARD2)
	#	print ("F3:" + FORWARD3 + " L3:" + LEFTWARD3 + " R3:" + RIGHTWARD3)
	# 3 stage maze drawing function.
	screensurf.fill((100, 120, 100))
	tilegriddraw2()
	screensurf.blit(gamebg, (0, 0))
	
	#if cantmoveflg==1:
		#drawheadertext(CANTMOVE, 1)
	if showlooktext==1:
		#drawheadertext(looktext, 1)
		popuptext(looktext)
		showlooktext=0
		mipfx.play()
	if showtiptext==1:
		#drawheadertext(looktext, 1)
		popuptext(tiptext)
		showtiptext=0
	if hudface=="1":
		hudfacesel=hudfacecasual
	elif hudface=="2":
		hudfacesel=hudfacesad
	elif hudface=="3":
		hudfacesel=hudfaceangry
	elif hudface=="4":
		hudfacesel=hudfaceshock
	elif hudface=="5":
		hudfacesel=hudfacehappy
	elif hudface=="6":
		hudfacesel=hudfacebored
	#hudfacesel=pygame.transform.scale(hudfacesel, (30, 30))
	screensurf.blit(hudfacesel, (54, 340))
	hudface=hudfacedef
		
	#drawheadertext(("Text-Maze 5 | " + mazetitle), 0)
	#print(libtextmaze.mazedraw3(FORWARD, BACKWARD, LEFTWARD, RIGHTWARD, FORWARD2, LEFTWARD2, RIGHTWARD2, FORWARD3, LEFTWARD3, RIGHTWARD3))
	pygame.display.update()
	pygame.event.pump()
	#this should be here! it needs to happen after teh screen update, and before the userentry stuff!
	for node in nodetag.findall("trigconv"):
		if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
			convtext=node.text
			hudface=node.attrib.get('face', "1")
			keyid=node.attrib.get('keyid', "0")
			takekey=node.attrib.get('takekey', "0")
			onkey=node.attrib.get('onkey', "0")
			offkey=node.attrib.get('offkey', "0")
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				debugmsg("conv node:", 1)
				if hudface=="1":
					hudfacesel=hudfacecasual
				elif hudface=="2":
					hudfacesel=hudfacesad
				elif hudface=="3":
					hudfacesel=hudfaceangry
				elif hudface=="4":
					hudfacesel=hudfaceshock
				elif hudface=="5":
					hudfacesel=hudfacehappy
				if not keyid in keylist:
					keylist.extend([keyid])
				if takekey in keylist and takekey!="0":
					keylist.remove([takekey])
				screensurf.blit(hudfacesel, (54, 340))
				hudface=hudfacedef
				fodx=convdup(convtext)
				if fodx==1:
					scrnx=screensurfdex.get_width()
					scrny=screensurfdex.get_height()
				break
		
	
	usrentry = ('null')
	#user prompt loop
	pygame.event.clear()
	if skiploop==0:
		while (usrentry!=FORWARDWORDBIND and usrentry!=BACKWARDWORDBIND and usrentry!=LEFTWORDBIND and usrentry!=RIGHTWODBIND and usrentry!=QUITWORDBIND and usrentry!="l" and usrentry!="t" and usrentry!="debugF" and usrentry!="debugB" and usrentry!="debugL" and usrentry!="debugR"):
			#drawfoottext(("forward:" + FORWARDWORDBIND + " | backward:" + 	BACKWARDWORDBIND + " | look around: l | talk: t"), 0)
			#drawfoottext(("left:" + LEFTWORDBIND + " | right:" + RIGHTWODBIND + " | quit:" + QUITWORDBIND), 1)
			if usrentry=="resize1":
				screensurfdex=pygame.display.set_mode((400, 400), RESIZABLE)
				scrnx=400
				scrny=400
			if usrentry=="resize2":
				screensurfdex=pygame.display.set_mode((600, 600), RESIZABLE)
				scrnx=600
				scrny=600
			if usrentry=="resize3":
				screensurfdex=pygame.display.set_mode((700, 700), RESIZABLE)
				scrnx=700
				scrny=700
			if usrentry=="evresize":
				scrnx=screensurfdex.get_width()
				scrny=screensurfdex.get_height()
			if usrentry=="debugcon":
				debugcon()
				break
			screensurfQ=pygame.transform.scale(screensurf, (scrnx, scrny))
			screensurfdex.blit(screensurfQ, (0, 0))
			pygame.display.update()
			usrentry=keyread()
	else:
		loopskipstop=1
		
	
	#print (chr(27) + "[2J" + chr(27) + "[H")
	#wall detection logic
	cantmoveflg=0
	if usrentry==BACKWARDWORDBIND:
		BIND1 = playy - 1
		if lookpointB(playx, BIND1)==('1'):
			cantmoveflg=1
			lastmove="B"
		elif lookpointB(playx, BIND1)==('0'):
			playy -= 1
			lastmove="B"
		elif lookpointB(playx, BIND1)==('3'):
			playy -= 1
			lastmove="B"
	if usrentry==FORWARDWORDBIND:
		BIND2 = playy + 1
		if lookpointB(playx, BIND2)==('1'):
			cantmoveflg=1
			lastmove="F"
		elif lookpointB(playx, BIND2)==('0'):
			playy += 1
			lastmove="F"
		elif lookpointB(playx, BIND2)==('3'):
			playy += 1
			lastmove="F"
	if usrentry==LEFTWORDBIND:
		BIND4 = playx + 1
		if lookpointB(BIND4, playy)==('1'):
			cantmoveflg=1
			lastmove="L"
		elif lookpointB(BIND4, playy)==('0'):
			playx += 1
			lastmove="L"
		elif lookpointB(BIND4, playy)==('3'):
			playx += 1
			lastmove="L"
	if usrentry==RIGHTWODBIND:
		BIND3 = playx - 1
		if lookpointB(BIND3, playy)==('1'):
			cantmoveflg=1
			lastmove="R"
		elif lookpointB(BIND3, playy)==('0'):
			playx -= 1
			lastmove="R"
		elif lookpointB(BIND3, playy)==('3'):
			playx -= 1
			lastmove="R"
	if usrentry=="debugF":
		playy += 1
		lastmove="F"
	if usrentry=="debugB":
		playy -= 1
		lastmove="B"
	if usrentry=="debugL":
		playx += 1
		lastmove="L"
	if usrentry=="debugR":
		playx -= 1
		lastmove="R"
	#misic user commands
	#print ("player x:" + str(playx) + "player y:" + str(playy))
	
	for node in nodetag.findall("trig"):
		if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
			keyid=node.attrib.get('keyid', "0")
			takekey=node.attrib.get('takekey', "0")
			onkey=node.attrib.get('onkey', "0")
			offkey=node.attrib.get('offkey', "0")
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				showlooktext=1
				if not keyid in keylist:
					keylist.extend([keyid])
				if takekey in keylist and takekey!="0":
					keylist.remove(takekey)
				looktext=node.attrib.get('text')
				hudface=node.attrib.get('face', "1")
				debugmsg("Triggered statement(trig): ", 1)
				break
	if usrentry=="l":
		for node in nodetag.findall("look"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				looktext=node.attrib.get('text')
				takekey=node.attrib.get('takekey', "0")
				keyid=node.attrib.get('keyid', "0")
				onkey=node.attrib.get('onkey', "0")
				offkey=node.attrib.get('offkey', "0")
				if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
					showlooktext=1
					if not keyid in keylist:
						keylist.extend([keyid])
					if takekey in keylist and takekey!="0":
						keylist.remove(takekey)
					hudface=node.attrib.get('face', "1")
					debugmsg("look statement(look): ", 1)
					break
		for node in nodetag.findall("switch"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				keyid=node.attrib.get('keyid', "0")
				if keyid!="0":
					if not keyid in keylist:
						switchonfx.play()
						keylist.extend([keyid])
						debugmsg("switchon")
					elif keyid in keylist:
						debugmsg("switchoff")
						switchofffx.play()
						keylist.remove(keyid)
		for node in nodetag.findall("itemlist"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				onkey=node.attrib.get('onkey', "0")
				offkey=node.attrib.get('offkey', "0")
				if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
					itemlisth=45
					itemlisthjmp=16
					itemhead=node.attrib.get('listname')
					popuptext(itemhead)
					for listitm in node.findall("i"):
						hideon=listitm.attrib.get('hideon', "0")
						keyid=listitm.attrib.get('keyid')
						itemtext=listitm.attrib.get('text')
						
						if (hideon=="0" and keyid in keylist) or (hideon=="1" and keyid not in keylist):
							print itemtext
							itemtextren=simplefontB.render(itemtext, True, (255, 255, 255), (0, 0, 0))
							screensurf.blit(itemtextren, (10, itemlisth))
							itemlisth += itemlisthjmp
					screensurfQ=pygame.transform.scale(screensurf, (scrnx, scrny))
					screensurfdex.blit(screensurfQ, (0, 0))
					pygame.display.update()
					retwile=convscreenwait()
					if retwile[0]==1:
						scrnx=retwile[1]
						scrny=retwile[2]
						fodchange=1
							
				
	
	if usrentry=="t":
		for node in nodetag.findall("conv"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				convtext=node.text
				hudface=node.attrib.get('face', "1")
				keyid=node.attrib.get('keyid', "0")
				takekey=node.attrib.get('takekey', "0")
				onkey=node.attrib.get('onkey', "0")
				offkey=node.attrib.get('offkey', "0")
				if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
					debugmsg("conv node:", 1)
					if hudface=="1":
						hudfacesel=hudfacecasual
					elif hudface=="2":
						hudfacesel=hudfacesad
					elif hudface=="3":
						hudfacesel=hudfaceangry
					elif hudface=="4":
						hudfacesel=hudfaceshock
					elif hudface=="5":
						hudfacesel=hudfacehappy
					if not keyid in keylist:
						keylist.extend([keyid])
					if takekey in keylist and takekey!="0":
						keylist.remove([takekey])
					screensurf.blit(hudfacesel, (54, 340))
					hudface=hudfacedef
					fodx=convdup(convtext)
					if fodx==1:
						scrnx=screensurfdex.get_width()
						scrny=screensurfdex.get_height()
					break
	else:
		for node in nodetag.findall("conv"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				
				onkey=node.attrib.get('onkey', "0")
				offkey=node.attrib.get('offkey', "0")
				if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
					showtiptext=1
					tiptext="press [t] to talk."
	
	if skiploop!=1:
		for node in nodetag.findall("teleport"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				onkey=node.attrib.get('onkey', "0")
				offkey=node.attrib.get('offkey', "0")
				if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
					debugmsg("Teleport node:")
					debugmsg("start pos:", 1)
					playx=int(node.attrib.get('destx'))
					playy=int(node.attrib.get('desty'))
					debugmsg("end pos:", 1)
					skiploop=1
					break
	if keylist!=keybak or forksanitycheck==1:
		debugmsg("keyid change detected. reparsing forks.")
		for fork in forktag.findall("batchtrig"):
			masterkey=fork.attrib.get("keyid")
			complist=[1] 
			for keyif in fork.findall("k"):
				ifpol=keyif.attrib.get("if")
				subkey=keyif.attrib.get("keyid")
				if subkey in keylist:
					if ifpol=="1":
						complist.extend([1])
					else:
						complist.extend([0])
				elif not subkey in keylist:
					if ifpol=="0":
						complist.extend([1])
					else:
						complist.extend([0])
			if len(set(complist)) == 1:
				if not masterkey in keylist:
					keylist.extend([masterkey])
					forksanity=1
			else:
				if masterkey in keylist:
					keylist.remove(masterkey)
					forksanity=1
		for fork in forktag.findall("batchset"):
			masterkey=fork.attrib.get("keyid")
			toggpol=fork.attrib.get("set")
			if masterkey in keylist:
				keylist.remove(masterkey)
				if toggpol=="1":
					for subkey in fork.findall("k"):
						subkeyid=subkey.attrib.get("keyid")
						if not subkeyid in keylist:
							keylist.extend([subkeyid])
					forksanity=1
				else:
					for subkey in fork.findall("k"):
						subkeyid=subkey.attrib.get("keyid")
						if subkeyid in keylist:
							keylist.remove(subkeyid)
					forksanity=1
		if forksanity==1:
			forksanitycheck=1
			forksanity=0
			skiploop=1
		else:
			forksanitycheck=0
	keybak=list(keylist)
	if loopskipstop==1:
		skiploop=0
		loopskipstop=0
	if playx<1:
		playx=1
		debugmsg("ERROR: player x pos illegal value. correcting.")
	if playy<1:
		debugmsg("ERROR: player y pos illegal value. correcting.")
		playy=1
	if usrentry==QUITWORDBIND:
		gameend=('1')
		debugmsg("User Has Quit.")
	#plays footstep sound fx
	if (cantmoveflg==0 and usrentry!=QUITWORDBIND and usrentry!="l" and usrentry!="t" and usrentry!="null"):
		stepfx.play()
		if usrentry=="debugF" or usrentry=="debugB" or usrentry=="debugL" or usrentry=="debugR":
			debugmsg("Player DEBUG move:", 1)
		else:
			debugmsg("Player move:", 1)
	#game win check
	if lookpoint(playx, playy)=='3':
		#print(WINGAME)
		debugmsg("User has reached an exit tile.")
		wintext = simplefont.render("Press a key.", True, (255, 255, 255), (0, 0, 0))
		wintextbox = wintext.get_rect()
		wintextbox.centerx = screensurf.get_rect().centerx
		wintextbox.centery = ((screensurf.get_rect().centery))
		winscreenbox = winscreen.get_rect()
		winscreenbox.centerx = screensurf.get_rect().centerx
		winscreenbox.centery = ((screensurf.get_rect().centery) - 60)
		screensurf.blit(winscreen, winscreenbox)
		screensurf.blit(wintext, wintextbox)
		screensurfQ=pygame.transform.scale(screensurf, (scrnx, scrny))
		screensurfdex.blit(screensurfQ, (0, 0))
		pygame.display.update()
		pygame.event.clear()
		winscreenwait()
		gameend=1
		
		

