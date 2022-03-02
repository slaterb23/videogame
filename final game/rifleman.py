
import torch
from doctest import ELLIPSIS_MARKER
import pygame
import os
import math
import random
from vector2D import Vector2
from physics import Distance,rad
from projectile import Projectile


from character import Character
class Rifleman(Character):

    def __init___(path,self,xposition,yposition):

        super().__init__(path,xposition,yposition)
        path=  os.path.join("images\Rifleman\Walking","180walking1.png")
        self.walking = False
        self.imageres = self.image
        self.shooting = False
        self.shootingimage = self.imageres
        self.starttime =1
        self.shootcursor = 1
        self.cocksound = pygame.mixer.Sound(os.path.join("sound","cocking.wav"))
        self.shootsound = pygame.mixer.Sound(os.path.join("sound","rifleshooting.wav"))

    def quickshootfix(self):
       self.shooting = False
       self.shootcursor = 1
       self.cocksound = pygame.mixer.Sound(os.path.join("sound","cocking.wav"))
       self.shootsound = pygame.mixer.Sound(os.path.join("sound","rifleshooting.wav"))

    def draw(self,surface):
        if [self.dead,self.shooting,self.going] == [False,False,False]:
      #its in a nothing state here, doing nothing
         
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))
         
        if self.selected == True:

           surface.blit(self.selectedim,[self.getPosition().x+16,self.getPosition().y-7])
         
           self.selectedim.set_colorkey(self.selectedim.get_at((0,0)))

         
        
        if self.shooting == True:
           self.image = self.shootimage
           surface.blit(self.image, list(self.position))
           self.image.set_colorkey(self.image.get_at((0,0)))


        if self.going == True:
           self.shooting == False
        if self.shooting == True:
           self.going == False
        if self.going == True:
         self.image = self.walkimage
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))


         

   
    def goshoot(self,target =None):
       self.target = target
       self.shooting = True
    def shoot(self,clock,projectilelst,framerate = 5):
      ''''
      Walks the citizen as per the requested frame rate      
      '''
      
      frame =framerate

      #Weird time, but trial and error shows 28 is best for walking
      time = clock.get_ticks()/28

      #print("this is time: " + str(time) + " starttime : " + str(self.starttime)) 
      if self.shooting ==True: 

                  
            direction = "270"
            self.shootimage = pygame.image.load(os.path.join("images\Rifleman\Shooting", direction+"shooting"+str(max(1,round(self.shootcursor/frame)))+".png")).convert()
              #Blit it here instead of the draw method for better clarity
            self.shootimage.set_colorkey(self.image.get_at((0,0)))
            if (time -self.starttime > 0.7):
               # Update time every 2.1 ish seconds
               
               self.changetime(time)
            
                       
               if self.shootcursor >14*frame:
                  # If the animation frame is greater than seven (only seven walking animation frames) then reset the cursor
                  self.shootcursor = 1
               # change animation frame as per the animation cursor
              
                 
                  

               if self.shootcursor <=14*frame:
                  #Move the Animatioon framecursor as long as it is below the frame amount
                  self.shootcursor +=1
               if self.shootcursor >14*frame:
                  self.shootcursor = 1

               if self.shootcursor == 10*frame:
                  bullet = Projectile(self.position.x-10,self.position.y+10,300)
                  projectilelst.append(bullet)
                  self.shootsound.play()
               if self.shootcursor == 2*frame:
                  
                  self.cocksound.play()

               
               # if self.cursor in(5*frame,frame):
                  
               #    self.cursor += (round(frame/1.5))
              
                  
          
      else:
         #If its not in a going state change the image to the defualt reserve image
         
         self.image = self.imageres

    def walk(self,clock,framerate = 7):
      ''''
      Walks the citizen as per the requested frame rate      
      '''
      
      frame =framerate

      #Weird time, but trial and error shows 28 is best for walking
      time = clock.get_ticks()/28

      #print("this is time: " + str(time) + " starttime : " + str(self.starttime)) 
      if self.going ==True: 

                  
            direction = self.getAnglestate()
            if self.getAnglestate() not in ("270","180","90","0"):
               direction = "0"
            self.walkimage = pygame.image.load(os.path.join("images\Rifleman\Walking", direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()
              #Blit it here instead of the draw method for better clarity
            self.walkimage.set_colorkey(self.image.get_at((0,0)))
            if (time -self.starttime > 0.7):
               # Update time every 2.1 ish seconds
               
               self.changetime(time)
            
                       
               if self.cursor >7*frame:
                  # If the animation frame is greater than seven (only seven walking animation frames) then reset the cursor
                  self.cursor = 1
               # change animation frame as per the animation cursor
              
                 
                  

               if self.cursor <=7*frame:
                  #Move the Animatioon framecursor as long as it is below the frame amount
                  self.cursor +=1
               if self.cursor >7*frame:
                  self.cursor = 1
               if self.cursor in(5*frame,frame):
                  
                  self.cursor += (round(frame/1.5))
              
                  
          
      else:
         #If its not in a going state change the image to the defualt reserve image
         
         self.image = self.imageres
         
