import sys

# The major, minor version numbers your require
MIN_VER = (3, 6)

if sys.version_info[:2] < MIN_VER:
    sys.exit(
        "This game requires Python {}.{}.".format(*MIN_VER)
    )

from ursina import * 
from objects import Spike,ThreeD_Button,Door,Laser,End
from player import Player
from world import Level

app = Ursina()

#Environment SETUP

brightness = 80
lights = [PointLight(position = (7,12,-15),color = color.rgb(*(min((brightness*1.5,255)) for _ in range(3)))),
            AmbientLight(color = color.rgb(*(brightness for _ in range(3))))]

Walls = [
    Entity(model = "cube",collider = "box",scale = (1,22),position = (11,-.5),texture = "wall",texture_scale = (0.5,11)),
    Entity(model = None,collider = "box",scale = (21,1),position = (0,11),texture_scale = (10.5,.5)),
    Entity(model = None,collider = "box",scale = (1,21),position = (-11,0),texture_scale = (0.5,10.5)),
    Entity(model = "cube",collider = "box",scale = (21,1),position = (0,-11),texture = "wall",texture_scale = (10.5,.5))
    ]

ground = Entity(model = "cube",scale = (22,1,22),rotation_x = -90,position = (.5,-.5,1),texture = "ground",texture_scale = (6,6))

#Player SETUP

player =Player("sphere", (0, 0), "sphere",texture = "bb8", controls="wasd",scale = 1)

#Camera SETUP

camera.orthographic = True
camera.fov = 30
camera.position = (-20,20,-35)
camera.look_at(ground)

#Level SETUP

doors = [Door((10,-9),player),Door((5,-5),player)]
small_walls =[Entity(model="cube",collider="box",scale = (5.5,1),position = (6.65,-9),texture = "wall",texture_scale = (2.5,.5)),
            Entity(model="cube",collider="box",scale = (1,5),position = (3.5,-6.9),texture = "wall",texture_scale = (.5,2.5)),
            Entity(model="cube",collider="box",scale = (5,1),position = (8,-5),texture = "wall",texture_scale = (2.5,.5))]
lasers = [Laser((8,-5.6),player,(0,-90,0),(0,.5,0),[]),Laser((-6,10.4),player,(0,-90,0),(0,.5,0),[])]
buttons = [ThreeD_Button((-10,7),player,doors=[doors[0]]),
            ThreeD_Button((10,9),player,doors=[*lasers,doors[1]])]
base = [End((10,-10),player)]

incoming=[Spike((9,-10),player),
        small_walls,
        [Spike((8,10),player),Spike((8,9),player),Spike((8,8),player),Spike((8,7),player),Spike((8.9,7),player),lasers[0],buttons[1]],
        [*doors,lasers[1],buttons[0],Spike((8,4.5),player),Spike((9,4.5),player),Spike((10,4.5),player)]]

level = Level(base = base,next= incoming,player =player)


app.run()
