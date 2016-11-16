#!/usr/bin/env python

# Text-maze 4
#mazemodpath = (os.path.join('MAZE', 'sample.MOD.txt'))



#>>cosmetic only<<
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


#load window icon, make window, set caption, start music, init things. etc.
pygame.mixer.init()
if MENUFLG==0:
	pygame.mixer.music.load(os.path.join('AUDIO', 'vg-mus-2_spooky-hall.ogg'))
	#pygame.mixer.music.load(os.path.join('AUDIO', 'vgtrack1.mid'))
	pygame.mixer.music.play(-1)
stepfx=pygame.mixer.Sound(os.path.join('AUDIO', 'step.ogg'))
mipfx=pygame.mixer.Sound(os.path.join('AUDIO', 'mip.ogg'))

pygame.display.init()
pygame.font.init()
windowicon=pygame.image.load(os.path.join('TILE', 'icon32.png'))
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((400, 370))
pygame.display.set_icon(windowicon)
pygame.display.set_caption("Text-maze 5", "Text-maze 5")

#load tiles
gamebg=pygame.image.load(os.path.join('TILE', 'game-bg.png'))
tilewall=pygame.image.load(os.path.join('TILE', 'wall.png'))
tileplayer=pygame.image.load(os.path.join('TILE', 'player.png'))
tileplayerB=pygame.image.load(os.path.join('TILE', 'playerB.png'))
tileplayerL=pygame.image.load(os.path.join('TILE', 'playerL.png'))
tileplayerR=pygame.image.load(os.path.join('TILE', 'playerR.png'))
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
#overlay graphics
ovflowers=pygame.image.load(os.path.join('TILE', 'ovflowers.png'))
ovbuntowel=pygame.image.load(os.path.join('TILE', 'ovbuntowel.png'))
ovbunraft=pygame.image.load(os.path.join('TILE', 'ovbunraft.png'))
ovbunstand=pygame.image.load(os.path.join('TILE', 'ovbunstand.png'))
ovsink=pygame.image.load(os.path.join('TILE', 'ovsink.png'))
ovtoilet=pygame.image.load(os.path.join('TILE', 'ovtoilet.png'))


winscreen=pygame.image.load(os.path.join('TILE', 'winscreen.png'))

# *.MAZE file data loader
print ("loading data from:" + mazefilepath)
tree = ET.parse(mazefilepath)
root = tree.getroot()
setuptag=root.find('setup')
playx=int((setuptag.find('startposx')).text)
playy=int((setuptag.find('startposy')).text)
mazemodpath=os.path.join("MAZE", ((root.find('maingrid')).text))
nodetag=root.find('nodes')
mazetitle=(setuptag.find('mazename')).text
print ("data loaded. \n")
debugset = ('1')
gameend = ('0')
CANTMOVE = ("Can't move in that direction.")
WINGAME = ("You win!")
lastmove="F"
inside=0
#draws tiles. used by tilegriddraw internally.

def tileblit(xval, yval, tilestring, xfoo, yfoo):
	if tilestring=="1":
		screensurf.blit(tilewall, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
		if inside==1:
			screensurf.blit(tileoutside, (xval, yval))
	if tilestring=="0":
		screensurf.blit(tilefloor, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
		if inside==1:
			screensurf.blit(tileoutside, (xval, yval))
	if tilestring=="3":
		screensurf.blit(tileexit, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
		if inside==1:
			screensurf.blit(tileoutside, (xval, yval))
	if tilestring=="w":
		screensurf.blit(tilewater, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
		if inside==1:
			screensurf.blit(tileoutside, (xval, yval))
	if tilestring=="g":
		screensurf.blit(tilegrass, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
		#print "ping"
		if inside==1:
			screensurf.blit(tileoutside, (xval, yval))
			#print "pong"
	if tilestring=="d":
		screensurf.blit(tiledock, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
		if inside==1:
			screensurf.blit(tileoutside, (xval, yval))
	if tilestring=="B":
		screensurf.blit(tilebrickpath, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
		if inside==1:
			screensurf.blit(tileoutside, (xval, yval))
	if tilestring=="b":
		screensurf.blit(tilebridge, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
		if inside==1:
			screensurf.blit(tileoutside, (xval, yval))
	#"inside" tiles below.
	if tilestring=="R":
		
		if inside==1:
			screensurf.blit(tileinsidewall, (xval, yval))
		else:
			screensurf.blit(tileroof1, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
	if tilestring=="c":
		
		if inside==1:
			screensurf.blit(tilecarpet, (xval, yval))
		else:
			screensurf.blit(tileroof1, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
	if tilestring=="r":
		
		if inside==1:
			screensurf.blit(tileredcarpet, (xval, yval))
		else:
			screensurf.blit(tileroof1, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
	if tilestring=="t":
		
		if inside==1:
			screensurf.blit(tiletiledfloor, (xval, yval))
		else:
			screensurf.blit(tileroof1, (xval, yval))
		overlayscanB(xfoo, yfoo, xval, yval)
		
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
	tileblit(160, 180, CENTER, xfoo, yfoo)
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
	labelscan()
	if lastmove=="F":
		screensurf.blit(tileplayer, (160, 180))
	if lastmove=="B":
		screensurf.blit(tileplayerB, (160, 180))
	if lastmove=="L":
		screensurf.blit(tileplayerL, (160, 180))
	if lastmove=="R":
		screensurf.blit(tileplayerR, (160, 180))

def overlayblit(overlaytype):
	if overlaytype=="flowers":
		return(ovflowers)
	if overlaytype=="2":
		return(ovbuntowel)
	if overlaytype=="3":
		return(ovbunraft)
	if overlaytype=="4":
		return(ovbunstand)
	if overlaytype=="sink":
		return(ovsink)
	if overlaytype=="toilet":
		return(ovtoilet)

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
	
def overlayscanB(xval, yval, xco, yco):
	for node in nodetag.findall("overlay"):
		xval=int(xval)
		yval=int(yval)
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
			if QX==xval and QY==yval:
				
				screensurf.blit(labtext, (xco, yco))
	
	
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
#datapoint lookup function. used to read data points from the main .grid file.
#when the point i out-of-range. 1 is returned.
def lookpoint(lookptx, lookpty):
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
	if lookuppointis=="\n":
		lookuppointis='1'
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
	if lookuppointis=="\n":
		lookuppointis='1'
	if lookuppointis=="g":
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
	for node in nodetag.findall("walkable"):
		if int(node.attrib.get('x'))==lookptx and int(node.attrib.get('y'))==lookpty:
			showlooktext=1
			lookuppointis=node.attrib.get('force')
			break
	return (lookuppointis)
	

#define a simple font from the system font
simplefont = pygame.font.SysFont(None, 16)
simplefontB = pygame.font.SysFont(None, 24)

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
			if event.type == KEYDOWN and event.key == K_UP:
				return(FORWARDWORDBIND)
			if event.type == KEYDOWN and event.key == K_LEFT:
				return(LEFTWORDBIND)
			if event.type == KEYDOWN and event.key == K_DOWN:
				return(BACKWARDWORDBIND)
			if event.type == KEYDOWN and event.key == K_RIGHT:
				return(RIGHTWODBIND)
			if event.type == KEYDOWN and event.key == K_l:
				return("l")
			if event.type == KEYDOWN and event.key == K_t:
				return("t")

def popuptext(textto):
	text = simplefontB.render(textto, True, (255, 255, 255), (0, 0, 0))
	textbox = text.get_rect()
	textbox.centerx=screensurf.get_rect().centerx
	textbox.centery=330
	screensurf.blit(text, textbox)
	
	
def convdup(convtext):
	textchunk=""
	textcont=(convtext + "\n")
	screensurfbak=screensurf.copy()
	for texch in textcont:
		#print texch
		if texch=="\n":
			popuptext(textchunk)
			textchunk=""
			pygame.display.update()
			winscreenwait()
			screensurf.blit(screensurfbak, (0, 0))
			#print "ping"
		else:
			textchunk=(textchunk + texch)
			#print "pong"
#old test data
#if lookpoint(2, 2)==('0'):
#	print ('blah')
#print (lookpoint(2, 2))
cantmoveflg=0
#main loop
while gameend==('0'):
	#POV coordinate determination
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
	if CENTER=="c" or CENTER=="r" or CENTER=="t":
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
	screensurf.blit(gamebg, (0, 0))
	tilegriddraw2()
	#if cantmoveflg==1:
		#drawheadertext(CANTMOVE, 1)
	if showlooktext==1:
		#drawheadertext(looktext, 1)
		popuptext(looktext)
		showlooktext=0
		mipfx.play()
	drawheadertext(("Text-Maze 5 | " + mazetitle), 0)
	#print(libtextmaze.mazedraw3(FORWARD, BACKWARD, LEFTWARD, RIGHTWARD, FORWARD2, LEFTWARD2, RIGHTWARD2, FORWARD3, LEFTWARD3, RIGHTWARD3))
	pygame.display.update()
	pygame.event.pump()
	
	usrentry = ('null')
	#user prompt loop
	pygame.event.clear()
	while (usrentry!=FORWARDWORDBIND and usrentry!=BACKWARDWORDBIND and usrentry!=LEFTWORDBIND and usrentry!=RIGHTWODBIND and usrentry!=QUITWORDBIND and usrentry!="l" and usrentry!="t"):
		#drawfoottext(("forward:" + FORWARDWORDBIND + " | backward:" + BACKWARDWORDBIND + " | look around: l | talk: t"), 0)
		#drawfoottext(("left:" + LEFTWORDBIND + " | right:" + RIGHTWODBIND + " | quit:" + QUITWORDBIND), 1)
		pygame.display.update()
		usrentry=keyread()
		
		
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
	#misic user commands
	#print ("player x:" + str(playx) + "player y:" + str(playy))
	for node in nodetag.findall("teleport"):
		if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
			playx=int(node.attrib.get('destx'))
			playy=int(node.attrib.get('desty'))
			break
	for node in nodetag.findall("trig"):
		if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
			showlooktext=1
			looktext=node.attrib.get('text')
			break
	if usrentry=="l":
		for node in nodetag.findall("look"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				showlooktext=1
				looktext=node.attrib.get('text')
				break
	if usrentry=="t":
		for node in nodetag.findall("conv"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				convtext=node.text
				convdup(convtext)
				break
		
	if usrentry==QUITWORDBIND:
		gameend=('1')
	#plays footstep sound fx
	if (cantmoveflg==0 and usrentry!=QUITWORDBIND and usrentry!="l"and usrentry!="t" ):
		stepfx.play()
	#game win check
	if lookpoint(playx, playy)=='3':
		#print(WINGAME)
		wintext = simplefont.render("Press a key.", True, (255, 255, 255), (0, 0, 0))
		wintextbox = wintext.get_rect()
		wintextbox.centerx = screensurf.get_rect().centerx
		wintextbox.centery = ((screensurf.get_rect().centery))
		winscreenbox = winscreen.get_rect()
		winscreenbox.centerx = screensurf.get_rect().centerx
		winscreenbox.centery = ((screensurf.get_rect().centery) - 60)
		screensurf.blit(winscreen, winscreenbox)
		screensurf.blit(wintext, wintextbox)
		pygame.display.update()
		pygame.event.clear()
		winscreenwait()
		gameend=1
		
		

