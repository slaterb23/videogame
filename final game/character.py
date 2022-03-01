import torch
from doctest import ELLIPSIS_MARKER
import pygame
import os
import math
import random
from vector2D import Vector2
from physics import Distance,rad
from drawable import drawable

SCREEN_SIZE = Vector2(800, 800)
WORLD_SIZE = Vector2(1200, 1000)

class Character(drawable):

    def __init__(self,path,xposition,yposition):

        super().__init__(path,xposition,yposition)
        self.cursor = 1
        self.start = [0,0]
        self.end = [0,0]
        self.maxspeed = 30
        self.tolerance = 2
        self.going = False
        self.selected = False
        self.arrived = False
        
    
    def changespeed(self,end):
      self.start = list(self.position)
      start = self.start
      self.end = end

      
      # Calculate the angle. 
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
    def go(self,time):
      '''
      Updates the position of the orb so that it does not fall of the edge
      '''
      #Go only if its going
      
      if self.going == True:

         
         # Render the start(the current position) and the end
         start = list(self.position)
         end = self.end
         
         
         self.changespeed(end)

         difference = Distance(list(start),list(end))

         angle = rad(list(start),list(end))

         # If the citizen hasn't reached distination yet
            
         if Distance(start,end)>self.tolerance and self.going == True:
            
               
               
               
               

            self.arrived = False
            angle = rad(start,end)
         
          
           
            oldpos = self.position

            #Update the position
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

            #self.graph.unmark(self.getHeight(), self.getWidth(), list(self.position))
            self.position.y = oldpos.y + ((self.velocity.y)*time.get_time()/1000)
            self.position.x = oldpos.x + ((self.velocity.x)*time.get_time()/1000)

            
         else:
            #reached desitation,stop going, and unselect, flag the arrived variable for event
            
            self.going =False
            self.updated = False
            self.unselect()
            #Stop
            self.velocity.x = 0
            self.velocity.y = 0
            
            self.arrived = True
            
                                      
      else:
         # Its not going, So stop         
         self.going = False
         self.velocity.x = 0
         self.velocity.y = 0

         return

    def beginmoving(self,end):
      '''
      Initializes the go method with the appropriate end variable
      '''
      self.going = True
      self.selected = False
      self.start = list(self.position)
      start = self.start
      self.end = end

      
      # # Calculate the angle. 
      # angle = rad(list(start),list(end))

      # #adjust speed according to destination
      # if start[1] < end[1]:
      #    self.velocity.y = abs(math.sin(angle)*self.maxspeed)
      # if start[0] < end[0]:
      #    self.velocity.x = abs(math.cos(angle)*self.maxspeed)
      # if start[0] > end[0]:
      #    self.velocity.x = -abs(math.cos(angle)*self.maxspeed)
      # if start[1] >end[1]:
      #    self.velocity.y = -abs(math.sin(angle)*self.maxspeed)

    def select(self):
        '''
        Selects the gamepiece 
        '''

        # select the fool, change the image to a selected image
        self.selected = True
        self.image = self.selimage

       #self.image = slightly beiged image
    def unselect(self):
        '''
        Unselects the game piece
        '''

        # Unselect it 
        self.selected = False
        self.image = self.imageres

    def getAngle(self):
       if self.velocity.x != 0 and self.velocity.y != 0:
         Angle = math.atan((self.velocity.y/self.velocity.x))*180/(math.pi)
         return Angle
       elif self.velocity.x ==0:
          if self.velocity.y <0:
             return 0
          if self.velocity.y > 0:
             return 180 
       else:
          return 0
    def getAnglestate(self):
       angle = self.getAngle()
       
       
       newangle = abs(angle)
       #print("this is angle"+ str(newangle))

       if self.velocity.x >0 and self.velocity.y > 0:
          if newangle < 15:
             #print(" state : 90")
             return "90"
          elif newangle > 55:
             
             #print(" state : 180")
             return "180"
          else:
             #print("state 135")
             return "180"
       if self.velocity.x <0 and self.velocity.y > 0:
          
          if newangle < 15 or (newangle > 55 and newangle < 60):
             #print(" state : 270")
             return "270"
          else:
             #print(" state : 225")
             return "180"
       if self.velocity.x <0 and self.velocity.y < 0:
         
          if newangle < 12 :
             #print(" state : 01")
             return "270"
          elif newangle < 50:
             #print(" state : 315")
             return "270"
          else: 
             return "0"
       if self.velocity.x >0 and self.velocity.y < 0:
          #print("should be here")
          if newangle >55: 
             #print(" state : 0")
             return "0"
          else:
             #print(" state : 45")
             return "90"
       


            
       
       
       
       




       

    def isselected(self):
        '''
        Returns the state of selection, or unselection
        '''
        return self.selected
      
    def kill(self):
        '''
        Self explanatory. Blood will be spilled
        '''
        self.dead  =True

    def isDead(self):

        '''
        Checks for deadness.
        '''
        return self.dead
              
