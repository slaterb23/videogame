from vector2D import Vector2
from physics import Distance,rad
from drawable import drawable
from Panel import panel
from character import Character
import os
import pygame
import math



class cannon(Character):
    def __init__(self,color,xposition,yposition):
        if color =="Green":
            self.color = "green"
            path = os.path.join("images\Cannon" +"\Green", "90walking1.png")
        
        else:
           self.color = "Red"
           path = path = os.path.join("images\Cannon\Red", "90walking1.png")

        super().__init__(path,xposition,yposition)
        self.shootcursor =1
        self.walkcursor =1
        self.shooting = False
        self.going = False
        self.imageres = self.image
        self.walkimage = self.image
        self.shootimage = self.image
        self.attack = 100
        self.HP = 1000
        self.frame = 2

        self.direction = "0"
        self.moving = True


        self.rangeimage = os.path.join("images\Cannon","riflerangerect.png")
        self.verimage= os.path.join("images\Cannon","uprange.png")

       ####Sensing the direction
      

        self.rangeup = panel(self.verimage,self.verimage,0,0)
        self.rangedown = panel(self.verimage,self.verimage,0,0)
        self.rangeright = panel(self.rangeimage,self.rangeimage,0,0)
        self.rangeleft = panel(self.rangeimage,self.rangeimage,0,0)
        self.collisionim =os.path.join("images\Rifleman","riflecollisionrect.png")
        self.collideim = panel(self.collisionim,self.collisionim,0,0)

        self.rangelst = [self.rangeup,self.rangedown,self.rangeright,self.rangeleft]


               
    def goshoot(self,target =None):
       self.target = target
       self.shooting = True
    def shoot(self,clock,projectilelst,enemylst,framerate = 2):
      ''''
      Walks the citizen as per the requested frame rate      
      '''
      
      time = clock.get_ticks()/1000

      

      frame =6

      distancedict = {}

      sortedenemy = []
      
      self.shootimage = self.image

      self.shooting = False
      for enemy in enemylst:
         xdiff = self.getPosition().x -enemy.getPosition().x
         ydiff = self.getPosition().y -enemy.getPosition().y
         xdiff= min(xdiff, 0.0001)
         angle = (abs(math.atan(ydiff/xdiff)))*180/(math.pi)
         
      
         for rect in self.rangelst:
            if enemy.getCollisionRect().colliderect(rect.getCollisionRect()):
               distance = Distance(list(enemy.getPosition()),list(self.getPosition()))
               self.shooting = True
               self.starttime = 0
               

               distancedict[distance]=enemy
               sortedenemy.append(distance)
        
         

      if self.shooting:
            sortedenemy.sort()
            


            target = distancedict[sortedenemy[0]]

            if target.getCollisionRect().colliderect(self.rangeup.getCollisionRect()):
               direction = "0"

            elif target.getCollisionRect().colliderect(self.rangedown.getCollisionRect()):

               direction = "180"

            elif target.getCollisionRect().colliderect(self.rangeleft.getCollisionRect()):
               direction = "270"

            elif target.getCollisionRect().colliderect(self.rangeright.getCollisionRect()):
               direction = "90"
            else:
               direction = "0"
     
            #rint("This is self direction ", self.direction, "this is angle " + str(angle))
            if self.color == "Red":
               self.shootimage = pygame.image.load(os.path.join("images\Cannon\Red", direction+"shooting"+str(max(1,round(self.shootcursor/frame)))+".png")).convert()
              #Blit it here instead of the draw method for better clarity
            else:
               self.shootimage = pygame.image.load(os.path.join("images\Cannon\Green", direction+"shooting"+str(max(1,round(self.shootcursor/frame)))+".png")).convert()
            
              #Blit it here instead of the draw method for better clarity
            self.shootimage.set_colorkey(self.image.get_at((0,0)))
            print("difference " + str(abs(time -self.starttime )))
            if abs(time -self.starttime) >0.01:
            #    # Update time every 2.1 ish seconds
               
               self.changetime(time)

               print("updating " + str(self.shootcursor) + "print this is max " + str(frame*16))
            
                       
               if self.shootcursor >16*frame:
                     # If the animation frame is greater than seven (only seven walking animation frames) then reset the cursor
                     self.shootcursor = 1
                  # change animation frame as per the animation cursor
               
                  
                     

               elif self.shootcursor <=16*frame:
                     #Move the Animatioon framecursor as long as it is below the frame amount
                     self.shootcursor +=1
            
                     
               if self.shootcursor == 14*frame:
                     
                     target.recvDamage(self.attack)

    def beginmoving(self,end):
      '''
      Initializes the go method with the appropriate end variable
      '''
    
      self.going = True
      #self.selected = False
      self.shooting = False
      self.start = list(self.position)
      start = self.start
      self.end = end
   

    def updaterange(self):
      cpointy = self.position.y +self.centery*self.getHeight()  
      cpointx = self.position.x +self.centerx*self.getWidth() 

      self.rangeup.position.x = cpointx-6
      self.rangeup.position.y = cpointy-300

      self.rangedown.position.x = cpointx-6
      self.rangedown.position.y = cpointy+60

      self.rangeleft.position.x = cpointx-330
      self.rangeleft.position.y = cpointy-8


      self.rangeright.position.x = cpointx+20
      self.rangeright.position.y = cpointy-12
    def draw(self,surface):

       

        self.updatecollide()
        self.updaterange()
        #self.rangeup.draw(surface)
        #pygame.draw.rect(surface,(0,0,255),self.getCollisionRect())

          

      #   for item in self.rangelst:
      #        item.draw(surface)
           #print("this is x, " , str(item.position.x))
        #"Length of range " + str(len(self.rangelst)))

        for item in self.sensorls:
           item.draw(surface)
        if [self.dead,self.shooting,self.going] == [False,False,False]:
      #its in a nothing state here, doing nothing
         
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))
         
        if self.selected == True:

           surface.blit(self.selectedim,[self.getPosition().x+16,self.getPosition().y-7])
         
           self.selectedim.set_colorkey(self.selectedim.get_at((0,0)))

         
        
        if self.shooting == True and self.going == True:
           self.shooting=False
           self.image = self.walkimage
           surface.blit(self.image, list(self.position))
           self.image.set_colorkey(self.image.get_at((0,0)))
         
        elif self.shooting ==True:
           self.image = self.shootimage
           surface.blit(self.image, list(self.position))
           self.image.set_colorkey(self.image.get_at((0,0)))



        if self.going == True and self.shooting == False:
         
         self.image = self.walkimage
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))



    def walk(self,clock,framerate = 5):
      ''''
      Walks the citizen as per the requested frame rate      
      '''
      
      frame =framerate

      maxframe = 4
      #Weird time, but trial and error shows 28 is best for walking
      time = clock.get_ticks()/28

      #print("this is time: " + str(time) + " starttime : " + str(self.starttime)) 
      if self.going ==True: 

                  
            direction = self.getAnglestate()
            self.direction = direction

            
            if self.getAnglestate() not in ("270","180","90","0"):
               direction = "0"
               self.direction = direction
            if self.color == "Red":
               self.walkimage = pygame.image.load(os.path.join("images\Cannon\Red", direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()
              #Blit it here instead of the draw method for better clarity
            else:
               self.walkimage = pygame.image.load(os.path.join("images\Cannon\Green", direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()

            self.walkimage.set_colorkey(self.image.get_at((0,0)))
            if (time -self.starttime > 0.7):

               # Update time every 2.1 ish seconds
               
               self.changetime(time)
            
                       
               if self.cursor >maxframe*frame:
                  # If the animation frame is greater than seven (only seven walking animation frames) then reset the cursor
                  self.cursor = 1
               # change animation frame as per the animation cursor
              
                 
                  

               if self.cursor <=maxframe*frame:
                  #Move the Animatioon framecursor as long as it is below the frame amount
                  self.cursor +=1
               if self.cursor >maxframe*frame:
                  self.cursor = 1
               
              
                  
          
      else:
         #If its not in a going state change the image to the defualt reserve image
         
         self.image = self.imageres

    def updaterange(self):
      cpointy = self.position.y +self.centery*self.getHeight()  
      cpointx = self.position.x +self.centerx*self.getWidth() 

      self.rangeup.position.x = cpointx-6
      self.rangeup.position.y = cpointy-300

      self.rangedown.position.x = cpointx-6
      self.rangedown.position.y = cpointy+60

      self.rangeleft.position.x = cpointx-330
      self.rangeleft.position.y = cpointy-8


      self.rangeright.position.x = cpointx+20
      self.rangeright.position.y = cpointy-12
    def updatecollide(self):

   
      cpointy = self.position.y +self.centery*self.getHeight()+19
      cpointx = self.position.x +self.centerx*self.getWidth()-8

      self.collideim.position.x = cpointx 
      self.collideim.position.y = cpointy - self.veradjust
       
      
         

        
    
