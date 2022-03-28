from vector2D import Vector2
from physics import Distance,rad
from drawable import drawable
from Panel import panel
from character import Character


class Cannon(Character):
    def __init__(self,path,xposition,ypositon):
        super().__init__(path,xposition,yposition)
        self.shootcursor =1
        self.walkcursor =1
        self.shooting = False
        self.going = False
        
    
