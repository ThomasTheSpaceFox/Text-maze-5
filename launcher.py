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

pygame.display.init()
pygame.font.init()
screensurfdex=pygame.display.set_mode((scrnx, scrny))
screensurf=pygame.Surface((400, 400))
titlescreen=pygame.image.load(os.path.join('TILE', 'titlescreen.png'))
listbg=pygame.image.load(os.path.join('TILE', 'UIlistBG.png'))
pygame.display.set_caption("Text-maze 5 launcher", "Text-maze 5 launcher")
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

def trivchooser():
	trivlisttree = ET.parse("launcher.xml")
	trivlistroot = trivlisttree.getroot()
	catlist=(["Main Menu"])
	catdesclist=(["Return to the Main Menu"])
	for fdat in (trivlistroot.findall("cat")):
		catlabel=(fdat.attrib.get("label"))
		catdesc=(fdat.attrib.get("desc"))
		#print fline
		catlist.extend([catlabel])
		catdesclist.extend([catdesc])
		catpic=0
	while catpic!=1:
		screensurf.blit(aboutbg, (0, 20))
		screensurf.blit(titlebg, (0, 0))
		#drawsmalltitle()
		categscreentext=simplefont.render("Category Selection", True, (0, 0, 0))
		screensurf.blit(categscreentext, (0, 0))
		catpic=iteratelistB(catlist, catdesclist)
		catcnt=1
		if catpic!=1:
			for fdat in (trivlistroot.findall("cat")):
				if catcnt==(catpic - 1):
					catlabel=(fdat.attrib.get("label"))
					categheadtext=simplefont.render(catlabel, True, (0, 0, 0))
					
					itemlist=["categories"]
					descriptlist=["return to categories"]
					for qdat in fdat.findall("item"):
						itemfile=qdat.text
						itemfile=os.path.join("MAZE", itemfile)
						#itemlabel=getlabels(itemfile)
						itemlabel=qdat.attrib.get("label")
						itemdesc=qdat.attrib.get("desc")
						itemlist.extend([itemlabel])
						descriptlist.extend([itemdesc])
					itempic=0
					while itempic!=1:
						screensurf.blit(aboutbg, (0, 20))
						screensurf.blit(titlebg, (0, 0))
						#drawsmalltitle()
						screensurf.blit(categheadtext, (0, 0))
						itempic=iteratelistB(itemlist, descriptlist)
						itemcnt=1
						if itempic!=1:
							for qdat in fdat.findall("item"):
								itemfile=qdat.text
								itemfile=os.path.join("MAZE", itemfile)
								if itemcnt==(itempic - 1):
									return(itemfile)
								itemcnt +=1
					
				catcnt += 1
mazefilepathX=trivchooser()
if mazefilepathX!=None:
	screensurf.blit(titlebg, (0, 0))
	screensurf.blit(titlescreen, (0, 20))
	popuptext("Loading...")
	time.sleep(0.1)
	screensurfQ=pygame.transform.scale(screensurf, (scrnx, scrny))
	screensurfdex.blit(screensurfQ, (0, 0))
	pygame.display.update()
	mazefilepath=mazefilepathX
	execfile("MAZE-ENG2.py")
else:
	print "Returning to main menu."



