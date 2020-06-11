# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 12:35:42 2020

@author: Mhlengi Nkosi
"""
import pygame
import csv
from queue import Queue
import networkx as nx
import sys, os, random


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
    
        self.currentpos =[
                          (x*(tilesize+margin)+margin, y*(tilesize+margin)+margin)
                          for y in range(gridsize[1])
                          for x in range(gridsize[0])
                         ]               
            
        self.font = pygame.font.Font(None,120)
        self.images = []
        self.prev = None
        self.score_value = 0
        self.Bimage = None
        self.Bimage_type = None
        self.Bcolour = None
          
            
    def setBlank(self,pos):
        self.tiles[-1] = pos #Empty tile pos
        
    def getBlank(self):
        return self.tiles[-1]
    
    opentile = property(getBlank,setBlank)
    
    def switch(self,tile):
        n = self.tiles.index(tile)
        self.tiles[n], self.opentile = self.opentile,tile
        self.prev = self.opentile
        
    def randomize(self):
        adj = self.adjacent()
        self.switch(random.choice([pos for pos in adj if self.in_grid(pos) and pos!=self.prev]))
             
        
    def in_grid(self,tile):
        return tile[0]>=0 and tile[0]<self.gridsize[0] and tile[1]>=0 and tile[1]<self.gridsize[1]
    
    def adjacent(self):
        x,y = self.opentile
        return (x-1,y),(x+1,y),(x,y-1),(x,y+1)
    
            #add 'images' blit to the program        
    def draw(self,screen):
        num1 = self.Bcolour.split(',')
        for i in range(0,len(num1)):
            num1[i] = num1[i].replace('(','')
            num1[i] = num1[i].replace(')','')
                    
        screen.fill((int(num1[0]),int(num1[1]),int(num1[2])))
        
        w,h = self.gridsize[0]*(self.tilesize+self.margin)+self.margin, self.gridsize[1]*(self.tilesize+self.margin)+self.margin
        
        pic = pygame.image.load(str(self.Bimage))#Retrieves image
        pic = pygame.transform.scale(pic,(w,h)) #Scales image to given dimensions
    
        for num in range(self.tileslen):
            #image = pygame.Surface((tilesize,tilesize)) #Create surface for tilesiez
            #image.fill((0,255,0))
            x,y = self.tilepos[self.tiles[num]]
            image = pic.subsurface(x,y, self.tilesize, self.tilesize)
            #Code to add numbers to tiles
            """
            text = self.font.render(str(num+1),2,(0,0,0))
            w,h = text.get_size()
            image.blit(text,((self.tilesize-w)/2,(self.tilesize-h)/2))
            """
            self.images +=[image]
            
        #w,h = self.gridsize[0]*(self.tilesize+self.margin)+self.margin, self.gridsize[1]*(self.tilesize+self.margin)+self.margin
        pic = pygame.image.load(str(self.Bimage))
        pic = pygame.transform.scale(pic,(self.tilesize+100,self.tilesize+100))
        screen.blit(pic,(535,200)) #add image preview as but slow down the cpu
        for num in range(self.tileslen):
            x,y = self.tilepos[self.tiles[num]]
            screen.blit(self.images[num],(x,y+30))
        
    
       
    
    def update(self,dt):
        #Switch tiles after mouse pressed
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        
        if mouse[0]:
            x,y = mpos[0] %(self.tilesize+self.margin),mpos[1] %(self.tilesize+self.margin)
            if x>self.margin and y>self.margin: #if mouse click tile && not margin
                tile = mpos[0]//self.tilesize,mpos[1]//self.tilesize
                
                if self.in_grid(tile) and tile in self.adjacent():
                        self.switch(tile)
                        self.score_value += 1 #increase score value when tile moves
        return self.score_value
        
     
    def show_score(self,screen,score_value,finish):

        self.score_value = score_value
        font = pygame.font.Font('freesansbold.ttf',40)
        text_font = pygame.font.Font('freesansbold.ttf',20)
        ScoreX = 535 
        ScoreY = 150
        score = font.render('Score : ' + str(self.score_value),True, (0,0,0) ,(255,255,255))
        text = text_font.render('Keyboard key to restart ',True, (0,0,0) ,(255,255,255))
        if finish:
            cfont = pygame.font.Font('freesansbold.ttf',40)
            TextX = 535 
            TextY = 100
            ctext = cfont.render('Congratulations' ,True, (0,0,0) ,(255,255,255))   
            screen.blit(ctext,(TextX,TextY)) #Outputs congrats for solving puzzle
        
        screen.blit(score,(ScoreX,ScoreY))
        screen.blit(text,(ScoreX,ScoreY +350))
        
    def complete(self,screen):
        #if all tiles in correct pos then done will remain true and program will output congrats
        done = True
        for i in range(self.tileslen):
            x,y = self.currentpos[i] 
            X,Y = self.tilepos[self.tiles[i]]
            if self.currentpos[i] != self.tilepos[self.tiles[i]]:
                done = False
        #if done:
            
            
        return done
                 
#Prints cords of tiles(current & defualt)        
    def cords(self):
        for i in range(self.tileslen):
            x,y = self.currentpos[i] 
            X,Y = self.tilepos[self.tiles[i]]
            print('Current: ' + str(self.currentpos[i]))
            print('Defualt: ' + str(self.tilepos[self.tiles[i]]))

    #Read csv values
    #csv values used in draw to determine slide image
    #and slide puzzle background
    def SlidepuzzleImage(self):
        #csv value [image,correct_pos]
        counter1 = -1
        counter = 0

        with open('puzzle_image.csv','r') as file:
            file_reader = csv.DictReader(file) ####!!!!!!!!!!!!!!!!!
            for line in file_reader:
                counter +=1
                        
        with open('puzzle_image.csv','r') as file:
            
            file_reader = csv.DictReader(file) ####!!!!!!!!!!!!!!!!!
            rand_int = random.randrange(0, counter) #Used to select random image
            #load csv values into array
            for line in file_reader:
                counter1 +=1
                if not line:
                    continue
                else:
                    if counter1 == rand_int:
                        self.Bimage =line['Image_Name'] + line['File type']
                        self.Bcolour = line['Background Colour']
                        break
                    else: continue
            
        
def solve_puzzle(self,complete):
    print("puzzle solved")

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
screen = pygame.display.set_mode((900,600)) 

#Title
pygame.display.set_caption("Slide Puzzle")

program = SlidePuzzle((3,3),160,5)
program.SlidepuzzleImage()
#Background image
#background_image = pygame.image.load('Puzzle_image') ###########@@@@@add each image
fpsclock = pygame.time.Clock()
running = True
first_time = True
score_value = 0

while running:
    displaytime = fpsclock.tick()/1000
    #Background
    #screen.fill((88,132,67)) #Red,Green,Blue - 255 limit /Baby Yoda Green 88,132,67
    program.draw(screen)
    program.show_score(screen,score_value,program.complete(screen))
    pygame.display.flip() # Update screen state/portion if values are given
    
    #Randomize tiles when game starts/ Randomize tiles once
    if first_time:
        for i in range(1000):
            program.randomize() 
            first_time = False

    for event in pygame.event.get(): #Recieves all events that occurs
        if event.type == pygame.QUIT:
            runnning = False
            pygame.quit()
        
    if event.type == pygame.KEYDOWN:
        first_time= True
        score_value = 0
        program = SlidePuzzle((3,3),160,5)
        program.SlidepuzzleImage()
                
    score_value = program.update(displaytime)
    if score_value>=1:
        if program.complete(screen):
            score_value = program.update(displaytime) #update screen -> display congrats
            program.draw(screen)
            program.show_score(screen,score_value,program.complete(screen))
            pygame.display.flip()
            if pygame.time.delay(40000) or event.type == pygame.KEYDOWN:  #Program waits before starting next game
                first_time= True
                score_value = 0
                program = SlidePuzzle((3,3),160,5)
                program.SlidepuzzleImage()
