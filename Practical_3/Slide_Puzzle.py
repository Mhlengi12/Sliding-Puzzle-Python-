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
        
        self.tileslen = gridsize[0]*gridsize[1] - 1
        #Tiles size
        self.tiles = [(x,y)
                      for y in range(gridsize[1])
                      for x in range(gridsize[0])
                      ]
        self.tilepos = {(x,y):
                         (x*(tilesize+margin)+margin, y*(tilesize+margin)+margin)
                         for y in range(gridsize[1])
                         for x in range(gridsize[0])
                         }
                        
            
        font = pygame.font.Font(None,120)
        self.images = []
        
        for num in range(self.tileslen):
            image = pygame.Surface((tilesize,tilesize)) #Set image_size to tilesiez
            image.fill((0,255,0))
            text = font.render(str(num+1),2,(0,0,0))
            w,h = text.get_size()
            image.blit(text,((tilesize-w)/2,(tilesize-h)/2))
            self.images +=[image] ###!!!! might need to change to self.images.append[image]
            
            
    def setBlank(self,pos):
        self.tiles[-1] = pos #Empty tile pos
        
    def getBlank(self):
        return self.tiles[-1]
    
    opentile = property(getBlank,setBlank)
    
    def switch(self,tile):
        n = self.tiles.index(tile)
        self.tiles[n], self.opentile = self.opentile,tile
        
        
    def in_grid(self,tile):
        return tile[0]>=0 and tile[0]<self.gridsize[0] and tile[1]>=0 and tile[1]<self.gridsize[1]
    
    def adjacent(self):
        x,y = self.opentile
        return (x-1,y),(x+1,y),(x,y-1),(x,y+1)
    
            #add 'images' blit to the program        
    def draw(self,screen):
        for num in range(self.tileslen):
            x,y = self.tilepos[self.tiles[num]]
            screen.blit(self.images[num],(x,y))
        
    
        
    
    def update(self,dt):
        #Switch tiles after mouse pressed
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        
        if mouse[0]:
            x,y = mpos[0] %(self.tilesize+self.margin),mpos[1] %(self.tilesize+self.margin)
            if x>self.margin and y>self.margin:
                tile = mpos[0]//self.tilesize,mpos[1]//self.tilesize
                
                if self.in_grid(tile) and tile in self.adjacent():
                        self.switch(tile)
        
      
    def show_score(self,screen):

        font = pygame.font.Font(None,120)
        score_value = 50
        
        image = pygame.Surface((50,50)) #Set image_size to tilesiez
        image.fill((100,100,0))
        score = font.render('Score :' + str(score_value),True, (255,255,255))
        image.blit(score,(100,100))

        #Score pos
        ScoreX = 10 
        ScoreY = 10
        
        score = font.render('Score :' + str(score_value),True, (255,255,255))
        screen.blit(score,(ScoreX,ScoreY))         
      
    
 
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
#Background image
#background_image = pygame.image.load('Puzzle_image') ###########@@@@@add each image
fpsclock = pygame.time.Clock()
running = True
score_value = 0

while running:
    displaytime = fpsclock.tick()/1000
    #Background
    screen.fill((0,255,0)) #Screen color
    program.draw(screen)
    screen.fill((88,132,67)) #Red,Green,Blue - 255 limit /Baby Yoda Green 88,132,67
    program.draw(screen)
    pygame.display.flip() # Update screen state
    

    for event in pygame.event.get(): #Recieves all events that occurs
        if event.type == pygame.QUIT:
            runnning = False
            pygame.quit()
            
    program.update(displaytime)



               


