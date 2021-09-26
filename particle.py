from ursina import *
import time

class Particle(Entity):
    def __init__(self, pos, start, maxi, length, color=color.hsv(0, 0, 0.3), curve = curve.linear,loop=False,velocity = (0,0), **kwargs):
        super().__init__(model="cube",color=color, position=pos, scale=start)
        self.z = -.1
        self.start = time.time()
        self.velocity = velocity
        self.length = length
        for key, value in kwargs.items():
            try :
                setattr(self, key, value)
            except :
                print(key,value)

        self.animate_position((self.x+self.velocity[0]*self.length,self.y+self.velocity[1]*self.length),duration = self.length)
        self.animate_scale(maxi, duration=length,curve=curve, loop=loop)

        destroy(self,delay=self.length)
