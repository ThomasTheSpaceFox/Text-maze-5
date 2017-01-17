#!/usr/bin/env python
import os
import pygame
import time
from pygame.locals import *
import xml.etree.ElementTree as ET
#some notes


scrnx=400
scrny=400
#some variables used in the menu list.
menitm1='Launcher'
#menitm2='null'
#menitm3='null'

screensurfdex=pygame.display.set_mode((scrnx, scrny), RESIZABLE)
screensurf=screensurfdex.copy()

#set MENUFLG to 1. this will tell Text-maze-4.py to not try to play and start the music. 
#(as when Text-maze-4.py is run from here the music is already playing)
MENUFLG=1
#list of menu options.
mainlist=(menitm1, "about", "options", "quit")
#find out number of options in menu. (used by the menu selection wrap-around)
findcnt=0
for flx in mainlist:
	findcnt += 1

#load titlescreen image.
titlescreen=pygame.image.load(os.path.join('TILE', 'titlescreen.png'))
titlebg=pygame.image.load(os.path.join('TILE', 'game-bg.png'))

#init the mixer and start the music
pygame.mixer.init()
pygame.mixer.music.load(os.path.join('AUDIO', 'vg-mus-2_spooky-hall.ogg'))



print ('Text-maze 5 maze selection menu')
#init stuff
pygame.display.init()
pygame.font.init()

#prep subcode scripts
sclaunch=open('launcher.py', 'r')
exlaunch=compile(sclaunch.read(), 'launcher.py', 'exec')
scabt=open('about.py', 'r')
exabt=compile(scabt.read(), 'about.py', 'exec')
scopt=open('options.py', 'r')
exopt=compile(scopt.read(), 'options.py', 'exec')
#load conf.xml
mainconf = ET.parse("conf.xml")
mainconfroot = mainconf.getroot()
animtag=mainconfroot.find("anim")
gfxtag=mainconfroot.find("gfx")
sndtag=mainconfroot.find("sound")
musicflg=int(sndtag.attrib.get("music", "1"))
movescrlflg=int(animtag.attrib.get("smoothscrl", "1"))
rgbafilterflg=int(gfxtag.attrib.get("rgbafilter", "1"))
scrx=int(gfxtag.attrib.get("scrx", "400"))
scry=int(gfxtag.attrib.get("scry", "400"))
CONFLOADED=1
if musicflg==1:
	pygame.mixer.music.play(-1)
#set up display
screensurfdex=pygame.display.set_mode((scrnx, scrny), RESIZABLE)
screensurf=screensurfdex.copy()
screensurf.fill((100, 120, 100))
#prep and display titlescreen image
titlescreenbox = titlescreen.get_rect()
titlescreenbox.centerx = screensurf.get_rect().centerx
titlescreenbox.centery = ((screensurf.get_rect().centery) - 90)
screensurf.blit(titlebg, (0, 0))
screensurf.blit(titlescreen, (0, 20))
scrnx=scrx
scrny=scry
screensurfdex=pygame.display.set_mode((scrnx, scrny), RESIZABLE)
screensurfQ=pygame.transform.scale(screensurf, (scrnx, scrny))
screensurfdex.blit(screensurfQ, (0, 0))
pygame.display.update()
def popuptextMENU(textto):
	text = simplefont.render(textto, True, (255, 255, 255), (0, 0, 0))
	textbox = text.get_rect()
	textbox.centerx=screensurf.get_rect().centerx
	textbox.centery=390
	screensurf.blit(text, textbox)



pygame.display.set_caption("Text-maze 5 menu", "Text-maze 5")
menuhighnum=1  #integer used to track the highlighted menu item. 
menusel="null"
simplefontB = pygame.font.SysFont(None, 22)
simplefont = pygame.font.SysFont(None, 16) #define a simple font from the system fonts

popuptextMENU("Text Maze v5.2 (c) 2015-2017 Thomas Leathers")
ixreturn=0
while menusel!="quit":
	#does things that need done upon returning to the menu from an option.
	if ixreturn==1:
		print ("Maze execution complete, returning to menu.")
		pygame.display.set_caption("Text-maze 5 menu", "Text-maze 5 menu")
		screensurf.fill((100, 120, 100))
		screensurf.blit(titlebg, (0, 0))
		#screensurf.blit(titlescreen, titlescreenbox)
		screensurf.blit(titlescreen, (0, 20))
		popuptextMENU("Text Maze v5.2 (c) 2015-2017 Thomas Leathers")
		ixreturn=0
	menucnt=1
	evhappenflg=0
	#wraps around menu, i.e. when your at the top and you press up you will be at the bottom of the list.
	if menuhighnum<=0:
		menuhighnum=findcnt
	elif menuhighnum>findcnt:
		menuhighnum=1
	#starting point for menu
	texhigcnt=54
	#separation between each line of text's origin
	texhigjump=14
	#menu line count variable. should be set to 1 here.
	indlcnt=1
	#draws the menu. inverting the colors of the selected menu item.
	for indx in mainlist:
		if indlcnt==menuhighnum:
			textit=simplefontB.render(indx, True, (0, 0, 0), (255, 255, 255))
		else:
			textit=simplefontB.render(indx, True, (5, 59, 186), (163, 169, 195))
		screensurf.blit(textit, (texhigcnt, 349))
		texhigcnt +=(textit.get_width())
		texhigcnt += texhigjump
		indlcnt += 1
	screensurfQ=pygame.transform.scale(screensurf, (scrnx, scrny))
	screensurfdex.blit(screensurfQ, (0, 0))
	pygame.display.update()
	pygame.event.pump()
	pygame.event.clear()
	#reads keyboard controlls, moves cursers when instructed by up/down arrow keys.
	#sets ixreturn to 1 when return is pressed.
	while evhappenflg==0:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_UP:
				menuhighnum -= 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_RIGHT:
				menuhighnum += 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_DOWN:
				menuhighnum += 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_LEFT:
				menuhighnum -= 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_RETURN:
				ixreturn=1
				evhappenflg=1
				break
			if event.type == QUIT:
				menusel="quit"
				evhappenflg=1
				break
			if event.type == VIDEORESIZE:
				sxh=event.h
				if sxh<400:
					sxh=400
				sxratio=(sxh-400)
				sxw=int(sxratio + 400)
				screensurfdex=pygame.display.set_mode((sxw, sxh), RESIZABLE)
				scrnx=sxw
				scrny=sxh
				screensurfQ=pygame.transform.scale(screensurf, (scrnx, scrny))
				screensurfdex.blit(screensurfQ, (0, 0))
				pygame.display.update()
	#second menu line count variable. should be set to 1 here.
	indlcnt2=1
	#executes option in menu when ixreturn is 1, (this means player has pressed return.)
	if ixreturn==1 and menusel!="quit":
		#print "blk1"
		for indxB in mainlist:
			#print indxB
			if indlcnt2==menuhighnum:
				if indxB==menitm1:
					#MAZEIS='sample.xml'
					#mazefilepath=(os.path.join('MAZE', MAZEIS)) #global variable used by Text-maze-4.py
					
					exec(exlaunch)
					
				#if indxB==menitm2:
					#MAZEIS='sample.MAZE'
					#mazefilepath=(os.path.join('MAZE', MAZEIS))
					#execfile('Text-maze-4.py')
				#if indxB==menitm3:
					#MAZEIS='switchback1.MAZE'
					#mazefilepath=(os.path.join('MAZE', MAZEIS))
					#execfile('Text-maze-4.py')
				if indxB=='quit':
					menusel="quit"
				if indxB=='about':
					exec(exabt)
				if indxB=='options':
					exec(exopt)
			indlcnt2 += 1
	pygame.display.update()
print "saving conf.xml"
gfxtag.set("scrx", str(scrnx))
gfxtag.set("scry", str(scrny))
mainconf.write("conf.xml")
