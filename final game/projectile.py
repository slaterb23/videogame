from email.mime import image
import torch
from doctest import ELLIPSIS_MARKER
import pygame
import os
import math
import random
from vector2D import Vector2
from physics import Distance,rad
from drawable import drawable

class Projectile(drawable):

    def __init__(self,xposition,yposition,velocity = 300,angle = 90):
        path = os.path.join("images\Projectiles","riflebullet.png")
        self.dead = False
        self.angle = angle
        
        super().__init__(path,xposition,yposition)
        rad = angle*math.pi/180
        res = pygame.transform.rotate(self.image,270)
        self.image =res

        res = pygame.transform.rotate(self.image,int(angle))
        self.image = res

        if angle ==0:
            self.velocity.y = -velocity
            self.velocity.x = 0
            
            self.position.x += 27
            self.position.y += 10
        if angle == 180:
            self.velocity.y = velocity
            self.position.x += 32
            self.position.y += 10
        

        if rad !=0:
            self.velocity.x = math.cos(rad)*velocity
            self.velocity.x = math.sin(rad)*velocity
        
        
    
    
    def travel(self,time):
        oldpos = self.position
        newposy = oldpos.y + self.velocity.y*time.get_time()/1000
        newposx = oldpos.x +self.velocity.x*time.get_time()/1000
        self.position.x = newposx
        self.position.y = newposy
    def die(self):
        self.dead = True
        
    