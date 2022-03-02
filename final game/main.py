
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
from rifleman import Rifleman
from dummy import Dummy
SCREEN_SIZE = (1200,900)


def main():
   
   # initialize the pygame module
   pygame.init()
   pygame.mixer.init()
   # load and set the logo
   
   
   pygame.display.set_caption("The Uncivil Defense")
   
   screen = pygame.display.set_mode(list(SCREEN_SIZE))

   hurt = pygame.mixer.Sound(os.path.join("sound","hurt1.wav"))
   siren = pygame.mixer.Sound(os.path.join("sound","siren.wav"))
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
   alliedriflepath = os.path.join("images\Rifleman\Walking","180walking1.png")
   
   dummypath = os.path.join("images\Enemies\dummy", "dummy.png")

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
   allymilitary= []
   selectedcitizenlst = []
   projectilelst = []

   enemylst = []
   for enemy in enemylst:
      homepos = list(home.getPosition())
      enemy.beginmoving((homepos[0] + 50, homepos[1]+50))
   #Tick the clock
   gameClock = pygame.time.Clock()
   homepos = list(home.getPosition())
   # define a variable to control the main loop
   RUNNING = True

   timer = 0
   
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
   
   for enemy in enemylst:
      print(enemy.isDead())

   timer = 0
   oldtime = 0
   warn = False
   Warnfont =  pygame.font.SysFont("Arial",29)
   warningtxt = Warnfont.render( "WARNING ENEMY APPROACHING",False,(255,0,0) )
   # main loop
   while RUNNING:
        time = int(pygame.time.get_ticks()/1000)
        #print(time)
        
        screen.fill((255,255,255))
        if abs(timer -time) > 3 and timer != 0:
           warn = False

        print(str(time) + " THis is the timer " + str(timer))
        if (time)%60 ==0 and time != 0:
           timer = time
           warn = True
           siren.play()

           
           
           
           
        if (time)%65 ==0 and time != 0 and time != oldtime:
           oldtime = time
           newDummy = Dummy(dummypath,50,50)
           newDummy.beginmoving((homepos[0] + 50, homepos[1]+50))
           enemylst.append(newDummy)



        

        for bullet in projectilelst:
           for enemy in enemylst:
              if bullet.getCollisionRect().colliderect(enemy.getCollisionRect()):
                 enemy.recvDamage(4)
                 hurt.play()

      # Draw everything, adjust by offset
        screen.blit(background,list((0,0)))
        if warn == True:
           screen.blit(warningtxt,(800,60))
      
        isbarrackselected = False
        #screen.blit(collide,list(man.position))
        cursor.draw(screen)
        leftpanel.draw(screen)
        rightpanel.draw(screen)
        register.draw(screen)
        HPfont =  pygame.font.SysFont("Arial",40)
        homehp = HPfont.render( (" Castle Hitpoints :" + str(home.HP)),False,(0,0,0) )
        
        screen.blit(homehp,(470,800))
        button.draw(screen,home.isselected())

        if home.isDead():
           RUNNING = False
        if len(enemylst) > 0:
         for enemy in enemylst:
            enemy.draw(screen)
            enemy.go(gameClock)
            if enemy.isDead():
                print("remving")
                enemylst.remove(enemy)
            elif enemy.getCollisionRect().colliderect(home.getCollisionRect()):
               home.recvdamage(20)
               enemy.kill()
           
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
        
        if len(allymilitary)>=1:
           #rint(citizenlst)
           for soldier in allymilitary:
              soldier.shoot(pygame.time,projectilelst)
              soldier.go(gameClock)
              soldier.walk(pygame.time)
              
              soldier.draw(screen)
              
        for bullet in projectilelst:
           bullet.draw(screen)
           bullet.travel(gameClock)

              
        if len(citizenlst)>=1:
           #rint(citizenlst)
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



         
        #rint("selected exists: " + str(isbarrackselected))
        if selectedexists:
           barrackbutton.draw(screen) 
              

             
           
           
        
        home.draw(screen)

        pygame.display.flip()

        
           
         
        for event in pygame.event.get():
          
              rand = random.randint(0,1)

              if event.type == pygame.KEYDOWN:
                  tutorial = pygame.image.load(os.path.join("images", "axe1.png")).convert()
                  #screen.blit(tutorial,[500,500])
              if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
               # change the value to False, to exit the main loop
                 RUNNING = False

               

              if event.type == pygame.KEYDOWN:
                 for riflesold in allymilitary:
                    riflesold.goshoot()
               
                 
              
              if event.type == pygame.KEYUP:
                 for riflesold in allymilitary:
                    riflesold.shooting = False
               #   rowlst  = []
               #   for row in board.maze:
               #      for pixel in row:
               #         if pixel ==1:
               #            if board.maze.index(row)  not in rowlst:
               #                #print("THis is row " + str(board.maze.index(row))+ "   " +str(row))
               #                rowlst.append(board.maze.index(row))

               
              if event.type == pygame.MOUSEBUTTONDOWN:
                 
                 if cursor.getCollisionRect().colliderect(leftpanel.getCollisionRect()) == False:
                        cursor.occupied = False
                        home.unselect()
                  
                 for buildings in buildinglst:
                     if cursor.getCollisionRect().colliderect(leftpanel.getCollisionRect()) == False:
                           cursor.occupied = False
                           buildings.unselect()

                 if event.button ==1:
                     if cursor.getCollisionRect().colliderect(button.getCollisionRect()):
                        if home.isselected():

                           newcitizen = home.spawn("citizen")
                           randomx = random.randint(-200,-40)
                           randomy= random.randint(-200,-40)
                           newcitizen.beginmoving(list((home.getPosition().x+randomx,home.getPosition().x+randomy)))
                           citizenlst.append(newcitizen)
                           
                              
                        
                     for buildings in buildinglst:
                        # if cursor.getCollisionRect().colliderect(buildings.getCollisionRect()):
                        #    if cursor.occupied ==False:
                        #       buildings.select()
                        #       cursor.occupied = True
                        if buildings.isselected():
                           if cursor.getCollisionRect().colliderect(riflemanbutton.getCollisionRect()):
                              riflesoldier = buildings.spawn("rifleman")
                              riflesoldier.quickshootfix()
                              randomx = random.randint(-80,-40)
                              randomy= random.randint(-100,-40)
                              riflesoldier.beginmoving([randomx+buildings.getPosition().x,randomy + buildings.getPosition().y])
                              allymilitary.append(riflesoldier)
                        
                        
                           
                     for buildings in buildinglst:
                        if cursor.getCollisionRect().colliderect(buildings.getCollisionRect()):
                           if cursor.occupied ==False:
                              buildings.select()
                              cursor.occupied = True
                     
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

                     for soldier in allymilitary:
                        if cursor.getCollisionRect().colliderect(soldier.getCollisionRect()):
                                 #mouse is selecting the human
                                 if cursor.occupied == False:
                                    soldier.select()
                                    #selectedcitizen.append(man)
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
                        
                     for soldier in allymilitary:
                        if soldier.isselected():
                           cursor.occupied = True

                        #IF not in a shooting state:
                           soldier.beginmoving(list(pygame.mouse.get_pos()))
                        else:
                           soldier.unselect()
                           cursor.occupied = False
                           
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
   
