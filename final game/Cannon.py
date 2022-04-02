from vector2D import Vector2
from physics import Distance,rad
from drawable import drawable
from Panel import panel
from character import Character
import os
import pygame



class cannon(Character):
    def __init__(self,side,xposition,yposition):
        if side ==1:
            path = os.path.join("images\Cannon", "90walking1.png")
        
        else:
            path = path = os.path.join("images\Cannon", "90walking1.png")

        super().__init__(path,xposition,yposition)
        self.shootcursor =1
        self.walkcursor =1
        self.shooting = False
        self.going = False
        self.imageres = self.image
        self.walkimage = self.image
        self.shootimage = self.image
        self.direction = "0"


        self.rangeimage = os.path.join("images\Rifleman","riflerangerect.png")
        self.verimage= os.path.join("images\Rifleman","uprange.png")

       ####Sensing the direction
      

        self.rangeup = panel(self.verimage,self.verimage,0,0)
        self.rangedown = panel(self.verimage,self.verimage,0,0)
        self.rangeright = panel(self.rangeimage,self.rangeimage,0,0)
        self.rangeleft = panel(self.rangeimage,self.rangeimage,0,0)
        self.collisionim =os.path.join("images\Rifleman","riflecollisionrect.png")
        self.collideim = panel(self.collisionim,self.collisionim,0,0)

        self.rangelst = [self.rangeup,self.rangedown,self.rangeright,self.rangeleft]


    def beginmoving(self,end,time):
      '''
      Initializes the go method with the appropriate end variable
      '''
      self.noshoottime = time
      self.going = True
      self.selected = False
      self.shooting = False
      self.start = list(self.position)
      start = self.start
      self.end = end
    def goshoot(yes=1,no=1,test=2):
        return None
    def shoot(self,yes=2,no=3,test=2,teswt =4):
        return None

    def draw(self,surface):

        self.updatecollide()
        self.updaterange()
        #self.rangeup.draw(surface)
        #pygame.draw.rect(surface,(0,0,255),self.getCollisionRect())

          

        #for item in self.rangelst:
             #item.draw(surface)
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
            self.walkimage = pygame.image.load(os.path.join("images\Cannon", direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()
              #Blit it here instead of the draw method for better clarity
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
       
      
         

        
    
