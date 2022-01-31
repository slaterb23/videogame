import pygame
import os
import random
from vector2D import Vector2
from citizen import citizen
from resource import resource
from mouse import mouse

SCREEN_SIZE = (1200,1000)


def main():
   
   # initialize the pygame module
   pygame.init()
   pygame.mixer.init()
   # load and set the logo
   
   pygame.display.set_caption("The Uncivil Defense")
   
   screen = pygame.display.set_mode(list(SCREEN_SIZE))

   
   # Let's make a background so we can see if we're moving
   background = pygame.image.load(os.path.join("images", "grass6.jpg")).convert()
   collide = pygame.image.load(os.path.join("images", "citizencollisionrect.png")).convert()
   mouse1 =os.path.join("images", "mouse.png")
   goldpath = os.path.join("images", "gold.png")
   citizenpath = os.path.join("images", "citizen3.png")
#intialize necessary vectors,paths for movement of orb and screen
   position = Vector2(0,0)
   velocity = Vector2(0,0)
   offset = Vector2(0,0)
   #path = os.path.join("images", "sphere1.png")

   cursor = mouse(mouse1)
   #Orb = orb(path,velocity,position,offset)
   #Orb.draw()
     
   #Tick the clock
   gameClock = pygame.time.Clock()
   
   # define a variable to control the main loop
   RUNNING = True
   man = citizen(citizenpath,100,100)
   goldmine = resource(goldpath,100,100)
   touched = False
   # main loop
   while RUNNING:

     
      # Draw everything, adjust by offset
        screen.blit(background,list((0,0)))

        
        #screen.blit(collide,list(man.position))
        cursor.draw(screen)
        
        goldmine.draw(screen)
        man.draw(screen)
        man.mine(gameClock)
        #pygame.time.set_timer(man.mine(gameClock),100)
        #print("this is time" + str(pygame.time.get_ticks()/100))

        
        man.go(gameClock)

        print("this is gold pos :" + str((goldmine.position.x,goldmine.position.y)))
        print(" this is human pos : "+ str((man.position.x,man.position.y)))
        print("this is mousepos : "+str((pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])))
        
        
        
        
##      screen.blit(Orb.image, list(Orb.position-getOffset(Orb)))
##      Orb.update(WORLD_SIZE,gameClock)
      
      # Flip the display to the monitor
        pygame.display.flip()
      
      # event handling, gets all event from the eventqueue


        for event in pygame.event.get():
              #print("x :" + str(man.position.x-goldmine.position.y) + "y : " +str(man.position.y-goldmine.position.y))
              
            # only do something if the event is of type QUIT or ESCAPE is pressed

              rand = random.randint(0,1)
              if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
               # change the value to False, to exit the main loop
                 RUNNING = False
              if event.type == pygame.MOUSEBUTTONDOWN:

                 

                 
                 if man.isselected():

                    if cursor.getCollisionRect().colliderect(goldmine.getCollisionRect()):
                       #print("----------------selected ------------------------")
                       man.goMine()
                       man.mining = True
                       man.beginmoving(goldmine.getgatherspot())
                       
                    elif not (cursor.getCollisionRect().colliderect(goldmine.getCollisionRect())):
                       man.unmine()
                    
                       man.beginmoving(list(pygame.mouse.get_pos()))
                    
                 elif cursor.getCollisionRect().colliderect(man.getCollisionRect()):
                       #print("----------------selected ------------------------")
                       
                       
                    
                    
                       
                       man.select()
                 else:
                    
                       man.unselect()
                       print("test mine"+ str(man.mining))
                       
                 

              
                
                
              
               

      # Update time and position
        gameClock.tick(60)
        ticks = gameClock.get_time() / 1000
##      Orb.position += Orb.velocity * ticks

      # calculate offset
##      offset = Vector2(max(0,
##                           min(Orb.position.x + (Orb.image.get_width() // 2) - \
##                               (SCREEN_SIZE[0] // 2),
##                               WORLD_SIZE[0] - SCREEN_SIZE[0])),
##                       max(0,
##                           min(Orb.position.y + (Orb.image.get_height()// 2) - \
##                               (SCREEN_SIZE[1] // 2),
##                               WORLD_SIZE[1] - SCREEN_SIZE[1])))

      
      
      
      
  
      
   pygame.quit()

if __name__ == "__main__":
   main()
   
