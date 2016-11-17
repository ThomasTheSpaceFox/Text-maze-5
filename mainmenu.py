#!/usr/bin/env python
import os
import pygame
import time
from pygame.locals import *
import xml.etree.ElementTree as ET
#some notes

#this is the maze selection program/main menu for Text-maze 4. the mazes are semi-softcoded. 
#what i mean is the maze engine itself can be executed from another python program that
#points it to a *.MAZE file using a global variable: "mazefilepath"
#see maze-series.py's comments for more info on this.

#some variables used in the menu list.
menitm1='Launcher'
#menitm2='null'
#menitm3='null'

#set MENUFLG to 1. this will tell Text-maze-4.py to not try to play and start the music. 
#(as when Text-maze-4.py is run from here the music is already playing)
MENUFLG=1
#list of menu options.
mainlist=(menitm1, "about", "quit")
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
pygame.mixer.music.play(-1)


print ('Text-maze 5 maze selection menu')
#init stuff
pygame.display.init()
pygame.font.init()

#set up display
screensurf=pygame.display.set_mode((400, 370))
screensurf.fill((100, 120, 100))
#prep and display titlescreen image
titlescreenbox = titlescreen.get_rect()
titlescreenbox.centerx = screensurf.get_rect().centerx
titlescreenbox.centery = ((screensurf.get_rect().centery) - 90)
screensurf.blit(titlebg, (0, 0))
#screensurf.blit(titlescreen, titlescreenbox)



pygame.display.set_caption("Text-maze 5 menu", "Text-maze 5")
menuhighnum=1  #integer used to track the highlighted menu item. 
menusel="null"
simplefont = pygame.font.SysFont(None, 16) #define a simple font from the system fonts
ixreturn=0
while menusel!="quit":
	#does things that need done upon returning to the menu from an option.
	if ixreturn==1:
		print ("Maze execution complete, returning to menu.")
		pygame.display.set_caption("Text-maze 5 menu", "Text-maze 5 menu")
		screensurf.fill((100, 120, 100))
		screensurf.blit(titlebg, (0, 0))
		#screensurf.blit(titlescreen, titlescreenbox)
		ixreturn=0
	menucnt=1
	evhappenflg=0
	#wraps around menu, i.e. when your at the top and you press up you will be at the bottom of the list.
	if menuhighnum<=0:
		menuhighnum=findcnt
	elif menuhighnum>findcnt:
		menuhighnum=1
	#starting point for menu
	texhigcnt=240
	#separation between each line of text's origin
	texhigjump=14
	#menu line count variable. should be set to 1 here.
	indlcnt=1
	#draws the menu. inverting the colors of the selected menu item.
	for indx in mainlist:
		if indlcnt==menuhighnum:
			textit=simplefont.render(indx, True, (0, 0, 0), (255, 255, 255))
		else:
			textit=simplefont.render(indx, True, (255, 255, 255), (0, 0, 0))
		screensurf.blit(textit, (0, texhigcnt))
		texhigcnt += texhigjump
		indlcnt += 1
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
			if event.type == KEYDOWN and event.key == K_DOWN:
				menuhighnum += 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_RETURN:
				ixreturn=1
				evhappenflg=1
				break
	#second menu line count variable. should be set to 1 here.
	indlcnt2=1
	#executes option in menu when ixreturn is 1, (this means player has pressed return.)
	if ixreturn==1:
		#print "blk1"
		for indxB in mainlist:
			#print indxB
			if indlcnt2==menuhighnum:
				if indxB==menitm1:
					#MAZEIS='sample.xml'
					#mazefilepath=(os.path.join('MAZE', MAZEIS)) #global variable used by Text-maze-4.py
					execfile('launcher.py')
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
					execfile('about.py')
			indlcnt2 += 1
	pygame.display.update()


