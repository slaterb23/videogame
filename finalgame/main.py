
import pygame
import os
import random
from vector2D import Vector2
from citizen import citizen
from resource import resource
from mouse import mouse
from Building import building
from Panel import panel
from drawable import drawable
from ResourceRegister import resourceregister
import testgraph
from testgraph import astar, graphmap

SCREEN_SIZE = (1200,900)


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
   treepath = os.path.join("images","tree.png")

   panelpath = os.path.join("images", "panel.png")
   buttonpath = os.path.join("images", "citizenbutton.png")
   barrackbuttonpath =os.path.join("images\Buttons", "barracksbutton.png")
   riflemanbuttonpath = os.path.join("images\Buttons", "riflemanbutton.png")


   citizenpath = os.path.join("images", "citizen3.png")
   
   
   homepath =  "testbuilding"
   homepathdir = "images"
   homeselectedpath = "testbuildingse"
   homeselectpathdir = "images"
   barrackdir= "images\Buildings"
   barrackpath = "barracks"

   
   home = building(homeselectedpath,homeselectpathdir,homepath,homepathdir,400,390)
  
   barrackselected ="barrackselected"
   

   count = 0
   #testbarrack = drawable(os.path.join("images\Buildings", "barracks" + str(count) + ".png"),800,400)


   position = Vector2(0,0)
   velocity = Vector2(0,0)
   offset = Vector2(0,0)
   #path = os.path.join("images", "sphere1.png")

   cursor = mouse(mouse1)
   #Orb = orb(path,velocity,position,offset)
   #Orb.draw()

   citizenlst = []
   selectedcitizen= []
   buildinglst = []
   unbuiltlst = []
   selectedcitizenlst = []
   #Tick the clock
   gameClock = pygame.time.Clock()
   
   # define a variable to control the main loop
   RUNNING = True

   
   
   
   
   
   
   
   goldminespot = [(-28,-18), (9,-12),(25,-10)]

   #man = citizen(100,100)
   goldmine = resource(goldpath,600,100,goldminespot)
   tree = resource(treepath,400,100,[(45,70)])


   leftpanel = panel(panelpath,None,0,770)
   rightpanel = panel(panelpath,None,800,770)
   
   button = panel(buttonpath,citizenpath,0,770)
   barrackbutton =  panel(barrackbuttonpath,barrackbuttonpath,0,770)
   riflemanbutton = panel(riflemanbuttonpath,riflemanbuttonpath,0,770)
   touched = False

   
   #barrack = building(barrackselectedpath,barrackpathlst[0],800,390)
   board = graphmap(SCREEN_SIZE)
   register = resourceregister()
   
   
  
   # main loop
   while RUNNING:

      
        screen.fill((255,255,255))
     
      # Draw everything, adjust by offset
        screen.blit(background,list((0,0)))
        
      
        isbarrackselected = False
        #screen.blit(collide,list(man.position))
        cursor.draw(screen)
        leftpanel.draw(screen)
        rightpanel.draw(screen)
        register.draw(screen)

        button.draw(screen,home.isselected())
        if len(buildinglst) >0:
           for buildings in buildinglst:
              if buildings.isselected():
                 isbarrackselected = True

        riflemanbutton.draw(screen,isbarrackselected)

        
        goldmine.draw(screen)
        tree.draw(screen)

        #testbarrack.draw(screen)
        #barrack.draw(screen)
        selectedexists = False
        
        if len(buildinglst)>=1:
         for buildings in buildinglst:
               buildings.draw(screen)
               buildings.update()
        
        if len(citizenlst)>=1:
           #print(citizenlst)
           for citizen in citizenlst:
              citizen.mine(pygame.time,register)
              citizen.chop(pygame.time,register)
              citizen.go(gameClock)
              citizen.update(citizenlst)
              citizen.walk(pygame.time)
              citizen.draw(screen)
              citizen.build(pygame.time)
              if citizen.isselected():
                 selectedexists = True



         
        print("selected exists: " + str(isbarrackselected))
        if selectedexists:
           barrackbutton.draw(screen) 
              

             
           
           
        
        home.draw(screen)

        pygame.display.flip()

        
           
         
        for event in pygame.event.get():
          
              rand = random.randint(0,1)
              if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
               # change the value to False, to exit the main loop
                 RUNNING = False

               

              if event.type == pygame.KEYDOWN:
               
                 if count < 5:
                    count +=1
                 else:
                    count -=1
              
              if event.type == pygame.KEYUP:
                 rowlst  = []
                 for row in board.maze:
                    for pixel in row:
                       if pixel ==1:
                          if board.maze.index(row)  not in rowlst:
                              #print("THis is row " + str(board.maze.index(row))+ "   " +str(row))
                              rowlst.append(board.maze.index(row))

               
              if event.type == pygame.MOUSEBUTTONDOWN:
                 
                 if cursor.getCollisionRect().colliderect(leftpanel.getCollisionRect()) == False:
                        cursor.occupied = False
                        home.unselect()

                 if event.button ==1:
                     if cursor.getCollisionRect().colliderect(button.getCollisionRect()):
                        if home.isselected():

                           newcitizen = home.spawn("citizen")
                           newcitizen.beginmoving(list((home.flagx,home.flagy)))
                           citizenlst.append(newcitizen)
                           
                              
                        
                     for buildings in buildinglst:
                        if cursor.getCollisionRect().colliderect(buildings.getCollisionRect()):
                           if cursor.occupied ==False:
                              buildings.select()
                              cursor.occupied = True
                        if  not (cursor.getCollisionRect().colliderect(buildings.getCollisionRect())):
                           buildings.unselect()
                           cursor.occupied = False
                           
                     
                     if cursor.getCollisionRect().colliderect(home.getCollisionRect()):
                        if cursor.occupied ==False:
                           home.select()
                           cursor.occupied = True
                           if len(selectedcitizen) != 0:
                                 selectedcitizen.remove(selectedcitizen[len(selectedcitizen)-1])
                     for man in citizenlst: 
                        if cursor.getCollisionRect().colliderect(man.getCollisionRect()):
                                 #mouse is selecting the human
                                 if cursor.occupied == False:
                                    man.select()
                                    selectedcitizen.append(man)
                                    cursor.occupied = True

                        if man.isselected():
                           selectedcitizenlst =[]
                           selectedcitizenlst.append(man)
                           if cursor.getCollisionRect().colliderect(barrackbutton.getCollisionRect()):
                                 barracks = building(barrackselected,barrackdir,barrackpath,barrackdir,300,400,0)
                                 unbuiltlst.append(barracks)

                                 cursor.occupied = True

                        
                 if event.button ==3:
                     if len(unbuiltlst) >=1:
                        tobuild =  unbuiltlst[0]
                        builder = selectedcitizenlst[0]
                        tobuild.position.x = pygame.mouse.get_pos()[0]
                        tobuild.position.y =pygame.mouse.get_pos()[1]-tobuild.getHeight()
                        builder.gobuild(tobuild)
                        builder.beginmoving((tobuild.position.x-20, tobuild.position.y+tobuild.getHeight()-42))
                        
                        buildinglst.append(unbuiltlst[0])
                        
                     for man in citizenlst:

                     
                        if man.isselected():
                           
                           
                           cursor.occupied = True

                          

                           if cursor.getCollisionRect().colliderect(goldmine.getCollisionRect()):
                              #print("----------------selected ------------------------")
                              print(str(goldmine.occupied))
                              cursor.occupied = True
                              if goldmine.occupied ==False:
                                    #print("i am here")
                                    man.goMine(goldmine)
                                    man.mining = True
                                    goldmine.markandgogather(man)
                              
                           elif not (cursor.getCollisionRect().colliderect(goldmine.getCollisionRect())):
                              
                              man.unmine(goldmine)
                              cursor.occupied = False
                           
                              man.beginmoving(list(pygame.mouse.get_pos()))
                           if cursor.getCollisionRect().colliderect(tree.getCollisionRect()):
                              #print("----------------selected ------------------------")
                              print(str(goldmine.occupied))
                              cursor.occupied = True
                              if tree.occupied ==False:
                                    #print("i am here")
                                    man.goChop(tree)
                                    man.chopping= True
                                    tree.markandgogather(man)
                           elif not (cursor.getCollisionRect().colliderect(goldmine.getCollisionRect())):
                              
                              man.unchop(tree)
                              cursor.occupied = False
                              
                        
                                 
                        else:
                              cursor.occupied = False
                              unbuiltlst= []
                              man.unselect()
                              if len(selectedcitizen) != 0:
                                 selectedcitizen.remove(selectedcitizen[len(selectedcitizen)-1])
                        
                              
                    

              
                
                
              
               

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
   
