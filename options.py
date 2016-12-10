#!/usr/bin/env python
import os
import pygame
import time
from pygame.locals import *
#some notes
import xml.etree.ElementTree as ET

#this is the launcher program for Text Maze 5. 
#it is intended to be executed by mainmenu.py, but can run by itself.
#a max of 22 categories, with 22 levels per category can be displayed properly.
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

#load conf.xml
mainconf = ET.parse("conf.xml")
mainconfroot = mainconf.getroot()
animtag=mainconfroot.find("anim")
gfxtag=mainconfroot.find("gfx")
sndtag=mainconfroot.find("sound")
musicflg=int(sndtag.attrib.get("music", "1"))
movescrlflg=int(animtag.attrib.get("smoothscrl", "1"))
rgbafilterflg=int(gfxtag.attrib.get("rgbafilter", "1"))

pygame.display.init()
pygame.font.init()
screensurfdex=pygame.display.set_mode((scrnx, scrny))
screensurf=pygame.Surface((400, 400))
titlescreen=pygame.image.load(os.path.join('TILE', 'titlescreen.png'))
listbg=pygame.image.load(os.path.join('TILE', 'UIlistBG.png'))
pygame.display.set_caption("Text-maze 5 options menu", "Text-maze 5 options menu")
screensurf.fill((100, 120, 100))
aboutbg=pygame.image.load(os.path.join('TILE', 'about-bg.png'))
titlebg=pygame.image.load(os.path.join('TILE', 'game-bg.png'))
simplefontB = pygame.font.SysFont(None, 22)
screensurf.blit(aboutbg, (0, 20))
screensurf.blit(titlebg, (0, 0))
simplefont = pygame.font.SysFont(None, 16)

def popuptext(textto):
	text = simplefontB.render(textto, True, (255, 255, 255), (0, 0, 0))
	textbox = text.get_rect()
	textbox.centerx=screensurf.get_rect().centerx
	textbox.centery=380
	screensurf.blit(text, textbox)

def iteratelistB(listtoiterate, descriplist):
	findcnt=0
	for flx in listtoiterate:
		findcnt += 1
	selectmade=0
	listhighnum=1
	listbgbox=listbg.get_rect()
	listbgbox.centerx = screensurf.get_rect().centerx
	listbgbox.centery = screensurf.get_rect().centery
	screensurf.blit(listbg, listbgbox)
	
	screensurfbak=screensurf.copy()
	texhigoffset=0
	while selectmade!=1:
		listbound=pygame.Surface((170, 248), SRCALPHA)
		listboundbox=listbound.get_rect()
		listboundbox.centerx = screensurf.get_rect().centerx
		listboundbox.centery = screensurf.get_rect().centery
		if listhighnum<=0:
			listhighnum=findcnt
			texhigoffset=(findcnt*14)-14
		elif listhighnum>findcnt:
			listhighnum=1
			texhigoffset=0
		#starting point for menu
		texhigcnt=80
		
		texhigcnt-=texhigoffset
		#separation between each line of text's origin
		texhigjump=14
		#menu line count variable. should be set to 1 here.
		indlcnt=1
		screensurf.blit(screensurfbak, (0, 0))
		for indx in listtoiterate:
			if indlcnt==listhighnum:
				textit=simplefont.render(("-> " + indx + " <-"), True, (255, 255, 255))
				popuptext(descriplist[(indlcnt-1)])
				
				
			else:
				textit=simplefont.render(indx, True, (255, 255, 255), (132, 135, 152))
			textitbox=textit.get_rect()
			textitbox.centerx = listbound.get_rect().centerx
			textitbox.centery = texhigcnt
			listbound.blit(textit, textitbox)
			
			texhigcnt += texhigjump
			indlcnt += 1
		screensurf.blit(listbound, listboundbox)
		screensurfQ=pygame.transform.scale(screensurf, (scrnx, scrny))
		screensurfdex.blit(screensurfQ, (0, 0))
		pygame.display.update()
		pygame.event.pump()
		pygame.event.clear()
		evhappenflg=0
		while evhappenflg==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_UP:
					listhighnum -= 1
					texhigoffset -= 14
					evhappenflg=1
				if event.type == KEYDOWN and event.key == K_DOWN:
					listhighnum += 1
					texhigoffset += 14
					evhappenflg=1
				if event.type == KEYDOWN and event.key == K_RETURN:
					ixreturn=1
					evhappenflg=1
					return(listhighnum)
					
				#catcnt += 1
optpick=0
while optpick!=1:
	if rgbafilterflg==1:
		RGBFILDIP="RGB tinting engine (currently on)"
	else:
		RGBFILDIP="RGB tinting engine (currently off)"
	if movescrlflg==1:
		SMSCDIP="movement scrolling effect (currently on)"
	else:
		SMSCDIP="movement scrolling effect (currently off)"
	
	if musicflg==1:
		MUSDIP="background music (currently on)"
	else:
		MUSDIP="background music (currently off)"
	optdesc=('return to main menu', RGBFILDIP, SMSCDIP, MUSDIP)
	optlist=("main menu", "RGB filter", "Smooth movement scrolling", "Music")
	screensurf.blit(aboutbg, (0, 20))
	screensurf.blit(titlebg, (0, 0))
	optpick=iteratelistB(optlist, optdesc)
	if optpick==2:
		if rgbafilterflg==1:
			rgbafilterflg=0
			gfxtag.set("rgbafilter", "0")
		else:
			rgbafilterflg=1
			gfxtag.set("rgbafilter", "1")
	if optpick==3:
		if movescrlflg==1:
			movescrlflg=0
			animtag.set("smoothscrl", "0")
		else:
			movescrlflg=1
			animtag.set("smoothscrl", "1")
	if optpick==4:
		if musicflg==1:
			sndtag.set("music", "0")
			musicflg=0
		else:
			sndtag.set("music", "1")
			musicflg=1
print "writing conf.xml"
mainconf.write("conf.xml")
print "returning to menu"


