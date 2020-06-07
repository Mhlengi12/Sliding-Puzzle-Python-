# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 12:35:42 2020

@author: Mhlengi Nkosi
"""
import pygame
import csv
from queue import Queue
import networkx as nx
import sys, os

#Set up the slide puzzle
class SlidePuzzle:
    #Default/required code for the slidepuzzle
    def __init__(self,gridsize, tilesize, margin):
        self.gridsize = gridsize
        self.tilesize = tilesize
        self.margin   = margin
        
        self.tiles_len = gridsize[0]*gridsize[1] - 1
        #Tiles size
        self.tiles = [(x,y)
                      for y in range(gridsize[1])
                      for x in range(gridsize[0])
                      ]
        self.tilespos = {(x,y):
                         (x*(tilesize+margin)+margin, y*(tilesize+margin)+margin)
                         for y in range(gridsize[1])
                         for x in range(gridsize[0])
                         }
                        
                         
    
            #add 'images' blit to the program        
    def draw(self,screen):
        for i in range(self.tiles_len):
            x,y = self.tilespos[self.tiles[i]]
            pygame.draw.rect(screen,(255,255,0), (x,y,self.tilesize,self.tilesize)) #255,255,0 = Yellow
    
    def update(self,dt):
        """
        fpsclock = pygame.time.Clock()
        displaytime = fpsclock.tick()/1000"""
        pass

    def score():
        pass
        
"""
#Read csv values
def SlidepuzzleImage(self,filename):
    #csv value [image,starting_pos,correct_pos]
    with open('filename','r') as file:
        file_reader = csv.DictReader(file) ####!!!!!!!!!!!!!!!!!
        
        #load csv values into array
        for line in file_reader:
            image.append(line['image'])
            starting_pos.append(line['starting_pos'])
            correct_pos.append(line['correct_pos'])

   """         


####################  MAIN #######################
startNode = []
goalNode = []
currentNode = []
image = []
correct_pos = []
starting_pos = []

#initialise pygame
pygame.init()

#Game screen
os.environ['SDL_VIDEO_CENTERED'] = '1' # Centres game screen
screen = pygame.display.set_mode((800,600)) 

#Title
pygame.display.set_caption("Slide Puzzle")

program = SlidePuzzle((3,3),100,5)
#Backgrounf image
#background_image = pygame.image.load('Puzzle_image') ###########@@@@@add each image
fpsclock = pygame.time.Clock()
running = True

while running:
    #Background
    screen.fill((0,0,0)) #Red,Green,Blue - 255 limit /Baby Yoda Green 88,132,67
    program.draw(screen)
    pygame.display.flip() # Update screen state
    

    for event in pygame.event.get(): #Recieves all events that occurs
        if event.type == pygame.QUIT:
            runnning = False
            pygame.quit()
            
    pygame.update()



               


