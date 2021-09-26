from ursina import * 


class Player(Entity):
    def __init__(self, model, position, collider,texture, scale = (1, 1, 1), SPEED = 2, velocity = (0, 0), controls = "wasd", **kwargs):
        super().__init__(
            model = model, 
            position = position,
            scale = scale,
            collider = collider,
            texture = texture
        )

        self.velocity_x, self.velocity_y = velocity
        self.SPEED = SPEED
        self.controls = controls
        self.deaths = 0
        self.death_counter = Text(text=f"Deaths : {self.deaths}", position=(-.85,.475), parent = camera.ui)
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except:
                print(key, value)


    def update(self):


        x_movement = (-held_keys[self.controls[1]] + held_keys[self.controls[3]]) * time.dt * 6 * self.SPEED
        y_movement = (held_keys[self.controls[0]] - held_keys[self.controls[2]]) * time.dt * 6 * self.SPEED

        self.rotation_x -= y_movement*62
        self.rotation_y -= x_movement*62

        if x_movement != 0:
            direction = (1, 0)
            if x_movement < 0:
                direction = (-1, 0)
            xRay = boxcast(origin=self.world_position, direction=direction,
                            distance=self.scale_x / 2 + abs(x_movement), ignore=[self, ])
            if not xRay.hit:
                self.x += x_movement

        if y_movement != 0:
            direction = (0, 1)
            if y_movement < 0:
                direction = (0, -1)
            yRay = boxcast(origin=self.world_position, direction=direction,
                            distance=self.scale_y / 2 + abs(y_movement), ignore=[self, ])
            if not yRay.hit:
                self.y += y_movement
        
    def reset(self):
        self.position = (0,0)
        self.rotation = (0,0,0)

    def kill(self):
        self.reset()
        self.deaths += 1
        self.death_counter.text=f"Deaths : {self.deaths}"
