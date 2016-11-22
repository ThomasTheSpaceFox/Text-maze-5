#!/usr/bin/env python
import os
import pygame
import time
from pygame.locals import *
#some notes

#this acts as a simple file parser that will show the contents of a file in a pygame window. 
#in this case it is used for the about screen (using the text file: 'live-about.txt'

pygame.display.init()
pygame.font.init()
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

screensurfdex=pygame.display.set_mode((scrnx, scrny))
screensurf=pygame.Surface((400, 400))
screensurf.fill((100, 120, 100))
aboutbg=pygame.image.load(os.path.join('TILE', 'about-bg.png'))
titlebg=pygame.image.load(os.path.join('TILE', 'game-bg.png'))
screensurf.blit(aboutbg, (0, 20))
screensurf.blit(titlebg, (0, 0))


pygame.display.set_caption("Text-maze 5 about", "Text-maze 5 about")
simplefont = pygame.font.SysFont(None, 16)
abt = open('live-about.txt')
pixcnt1=20
pixjmp=14

for fnx in abt:
	fnx=fnx.replace('\n', '')
	abttext=simplefont.render(fnx, True, (0, 0, 0))
	abttextB=simplefont.render(fnx, True, (0, 0, 0), (255, 255, 255))
	abttextB.set_alpha(150)
	screensurf.blit(abttextB, (0, pixcnt1))
	screensurf.blit(abttext, (0, pixcnt1))
	pixcnt1 += pixjmp
screensurfQ=pygame.transform.scale(screensurf, (scrnx, scrny))
screensurfdex.blit(screensurfQ, (0, 0))
pygame.display.update()
evhappenflg2=0
while evhappenflg2==0:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_RETURN:
				evhappenflg2=1
				break
screensurfdex=pygame.display.set_mode((scrnx, scrny), RESIZABLE)