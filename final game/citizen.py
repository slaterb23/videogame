'''
Nobel Manayhe

Implements an automatcially moving orb that is followed by a camera

'''
import pygame
import os
import math
import random
from vector2D import Vector2
from physics import Distance,rad
# Two different sizes now! Screen size is the amount we show the player,
#  and world size is the size of the interactable world
SCREEN_SIZE = Vector2(800, 800)
WORLD_SIZE = Vector2(1200, 1000)



class citizen(object):
   '''
   Implements the Orb object
   '''

   def __init__(self,path,xposition,yposition):
      '''
      initializes the Orb oject
      '''

      #initialize variables

      #reserve image to be looked on incase self.image changes due to events
      self.imageres = pygame.image.load(path).convert()
      self.image= pygame.image.load(path).convert()
      self.selimage = pygame.image.load(os.path.join("images","citizenselect.png"))

      
      self.velocity = Vector2(0,0)
      self.position = Vector2(0,0)
      self.position.x = xposition
      self.position.y = yposition
      self.dead = False
      #generate starting conditions for the orb(including random desired speeds, velocity & position vecs)
      
      self.maxspeed = 30
      self.tolerance = 5
      self.going = False
      self.start = [0,0]
      self.end = [0,0]
      self.selected = False
      self.mining = False
      self.starttime = 0
      self.cursor = 1
      self.arrived = False
      
      
    
   
   def goMine(self):
      self.mining = True
      
   def getPosition(self):
      '''
      Returns the positional vector of the orb
      '''
      return self.position
   def getX(self):

      return self.position.x

   def getY(self):
      return self.position.y

   def getWidth(self):
      '''
      Returns the width of the orb image
      '''
      return self.image.get_width()

   def getHeight(self):
      '''
      Returns the height of the orb
      '''
      return self.image.get_height()
   def draw(self,surface):
      '''
       Draws the orb
      '''

      
      
      
      if self.dead == False:
         
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))
         

 
   def getSize(self):
      '''
      Returns the size of the orb
      '''
      return self.image.get_size()

   
      
   def go(self,time,event=None):
      '''
      Updates the position of the orb so that it does not fall of the edge
      '''
      
      #store variables that check for the edge
      if self.going == True:
   
         start = list(self.position)
         end = self.end

         difference = Distance(list(start),list(end))

         angle = rad(list(start),list(end))
            
         if Distance(start,end)>self.tolerance and self.going == True:
            
            self.arrived = False
            angle = rad(start,end)
         
          
            maxspeed = 2

            
            oldpos = self.position

            newposy = oldpos.y + self.velocity.y*time.get_time()/1000
            newposx = oldpos.x +self.velocity.x*time.get_time()/1000

            # if is about to cross the screen, reverse the velocity
            if newposy+self.getHeight() > WORLD_SIZE.y:

               self.velocity.y *=-1

            elif newposy <0:

               self.velocity.y *=-1

            if newposx +self.getWidth()> WORLD_SIZE.x:

               self.velocity.x *=-1


            elif newposx <0:

               self.velocity.x *=-1

            #update the position 
            self.position.y = oldpos.y + ((self.velocity.y)*time.get_time()/1000)
            self.position.x = oldpos.x + ((self.velocity.x)*time.get_time()/1000)

            
         else:
            #reached desitation,stop going, and unselect, flag the arrived variable for event
            
            self.going =False
            pygame.mixer.music.load('mining.mp3')
            pygame.mixer.music.play()
            self.unselect()
            self.velocity.x = 0
            self.velocity.y = 0
            self.arrived = True
               
            
               
            
            
      else:
         
         
         self.handleevent(time,event)
         # its not going, so stop. 
         self.going = False
         self.velocity.x = 0
         self.velocity.y = 0

         return

              

         

          
      
 
   def handleevent(self,time,event):

      if event is None:
         return

      if event == 1 and self.mining == True:
         mine(time)
   def mine(self,time):

      
      time = pygame.time.get_ticks()/100
      if self.mining == True and self.arrived ==True:
         
         
         if abs(time-(self.starttime))> 10:
            self.starttime = int(time)
            self.cursor = 1
            
         else:
            

            
            if (int(time)//2 == int(time)/2):
            

            
               
               self.image = pygame.image.load(os.path.join("images","axe"+str(self.cursor)+".png")).convert()
               self.image.set_colorkey(self.image.get_at((0,0)))
               if self.cursor <5:
                  self.cursor +=1
          

      else:
         
         self.image = self.imageres
         self.mining ==False

         

      
         

   def unmine(self):
      self.mining = False
      
   def beginmoving(self,end):
      self.going = True
      self.start = list(self.position)
      start = self.start
      self.end = end

      

      angle = rad(list(start),list(end))

      #adjust speed according to destination
      if start[1] < end[1]:
         self.velocity.y = abs(math.sin(angle)*self.maxspeed)
      if start[0] < end[0]:
         self.velocity.x = abs(math.cos(angle)*self.maxspeed)
      if start[0] > end[0]:
         self.velocity.x = -abs(math.cos(angle)*self.maxspeed)
      if start[1] >end[1]:
         self.velocity.y = -abs(math.sin(angle)*self.maxspeed)


      

   def getOffset(self):
      '''
         returns a Vector2 variable containing the offset for drawing things to the screen.
      '''
      return Vector2(max(0,
                        min(self.position.x + (self.image.get_width() // 2) - \
                            (SCREEN_SIZE[0] // 2),
                            WORLD_SIZE[0] - SCREEN_SIZE[0])),
                    max(0,
                        min(self.position.y + (self.image.get_height()// 2) - \
                            (SCREEN_SIZE[1] // 2),
                            WORLD_SIZE[1] - SCREEN_SIZE[1])))

   def getCollisionRect(self):
      newRect =  self.position + self.image.get_rect()
      return newRect

   def select(self):
       self.selected = True
       #self.mining = False
       self.image = self.selimage

       
       #self.image = slightly beiged image
   def unselect(self):
       self.selected = False
       self.image = self.imageres
   def isselected(self):
       return self.selected

   def contains(self,point):
      newrect = self.image.get_rect()

      
   def kill(self):
      self.dead  =True
   def isDead(self):
      return self.dead
        
