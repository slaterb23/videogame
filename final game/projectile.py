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

    def __init__(self,xposition,yposition,velocity = 100):
        path = os.path.join("images\Projectiles","riflebullet.png")
        self.dead = False
        
        super().__init__(path,xposition,yposition)
        self.velocity.x = -velocity
    
    def travel(self,time):
        oldpos = self.position
        newposy = oldpos.y + self.velocity.y*time.get_time()/1000
        newposx = oldpos.x +self.velocity.x*time.get_time()/1000
        self.position.x = newposx
        self.position.y = newposy
        
    