from ursina import *
from objects import ThreeD_Button,Laser

class Level(Entity):
    def __init__(self,base,next,player):
        super().__init__(model = None,position = (0,0,0))
        self.base = base
        self.base[0].set_level(self)
        for elem in self.base :
            elem.parent = self

        self.player = player
        self.followers = next
        for elem in self.followers:
            if type(elem) not in (list,tuple) :
                elem.disable()

            else :
                for elem in elem :
                    elem.disable()

    def next(self):
        if len(self.followers)>0 :
            if type(self.followers[0]) not in (list,tuple) :
                self.followers[0].enable()
                self.base.append(self.followers[0])
            else :
                for elem in self.followers[0] :
                    elem.enable()
                    self.base.append(elem)
            self.followers.pop(0)
            for elem in self.base:
                if type(elem) == ThreeD_Button:
                    if not elem.state :
                        elem.toggle()
        else :
            scene.clear()
            bg = Entity(parent=camera.ui, model='quad', scale_x=camera.aspect_ratio, color=color.black, z=1)
            bg.scale *= 400
            win = Text(parent = camera.ui,text=f'You Won using {self.player.deaths} lives !!', origin=(0,0), color=color.clear,scale =2)
            win.animate_color(color.white,duration = 1)
            create = Text(parent = camera.ui,text='Made by ano002 (Spike Model by NufNuf)', origin=(0,1.7), color=color.clear,scale =1)
            create.animate_color(color.white,duration = 1)
        
