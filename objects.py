from ursina import *
from particle import Particle
import random
import math
from ursina.shaders import unlit_shader

class Spike(Entity):
    def __init__(self, position,player):
        super().__init__(model="les_piques",position=position,color=color.dark_gray,rotation_x=-90,z=.5,origin=(-.5,0,-.5))
        self.collider=None
        self.player = player
    def update(self):
        if abs(self.player.y-self.y) < 1 and abs(self.player.x-self.x) < 1:
            for i in range(25):
                angle = 14.4 * i
                x = math.sin(math.radians(angle%360-180))*5
                y = math.cos(math.radians(angle%360-180))*5
                brightness=random.randint(30,160)
                Particle(model="cube",pos=self.player.position+(0,0,-.2), start=.1, maxi=.2, length=random.random()/2, color=color.rgb(
                    *(brightness for _ in range(3))), velocity=(x, y))
            self.player.kill()

class ThreeD_Button(Entity):
    def __init__(self, position,player,doors):
        super().__init__(model = None,position = position,rotation_x=-90,z=.4)
        self.z += .5
        self.base = Entity(model="cylinder",scale = .5,y=-.5, texture="white_cube",parent =self)
        self.button = Entity(model="cylinder",scale = .4, color=color.red,parent =self,y=-.2)
        self.player = player
        self.state = True
        self.touching = False
        self.doors = doors

    def toggle(self):
        self.button.animate("y",-.2*self.state-.2,curve=curve.linear,duration=.3)
        self.state = not self.state
        if self.state:
            for door in self.doors:
                door.close()
        else:
            for door in self.doors:
                door.open()

    def add(self,elem):
        self.doors.append(elem)

    def update(self):
        if distance_2d(self,self.player)<.8 :
            if not self.touching:
                self.touching = True
                self.toggle()
        else:
            self.touching = False

class Door(Entity):
    def __init__(self, position,player):
        super().__init__(model = "cube",texture="white_cube",position = position,collider = "box",scale =(1,.2,1))
        self.player = player

    def open(self):
        self.animate_scale(0)
        self.collider = None

    def close(self):
        self.animate_scale((1,.2,1)) 
        self.collider = BoxCollider(self)

class Laser(Entity):
    def __init__(self, position,player,rotation,origin,ignores):
        super().__init__(model = "cube",position = position,rotation = rotation,double_sided=True,color=color.rgba(255,0,0,80),shader=unlit_shader)
        self.player = player
        self.ignores = ignores
        ray = raycast(self.position,direction=self.rotation,ignore=ignores)
        self.active = True
        if ray.hit :
            self.origin=origin
            self.scale = Vec3(.1,.1,.1)+(Vec3(*(abs(val) for val in self.rotation/90))*ray.distance)
        self.saved_scale = self.scale

    def open(self):
        self.animate_scale(0)
        self.active = False

    def close(self):
        self.animate_scale(self.saved_scale) 
        self.active = True
    
    def update(self):
        if self.active :
            ray = raycast(self.position,direction=self.rotation,ignore=(self,))
            if ray.hit and self.player in ray.entities:
                self.player.kill()

class End(Entity):
    def __init__(self, position,player):
        super().__init__(model = "cube",position = position,scale =(1,1,.2),color = color.rgba(0,255,0,80))
        self.player = player
        self.z += .4

    def set_level(self,level):
        self.level = level

    def update(self):
        if abs(self.player.y-self.y) < 1 and abs(self.player.x-self.x) < 1:
            if hasattr(self,'level'):
                self.level.next()
                self.player.reset()
