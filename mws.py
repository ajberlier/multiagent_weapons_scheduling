import math
import turtle
import random

# TODO: pull this from system info so that it fits any screen full
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

wn = turtle.Screen()
wn.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
wn.title("Multi-agent Weapons Scheduling")
wn.bgcolor("black")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()

class Environment: 
    """
    Base class for the environment.
    """
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        # TODO: generate scenario from config file
        self.num_blue_agents = 1
        self.num_red_agents = 2
        self.end_of_battle = False

    def build_scenario(self):
        sprites.clear()
        # TODO: create blue agents with weapons
        # create blue agent sprite
        blue_agent = Agent(0, 0, "triangle", "blue", "blue")
        sprites.append(blue_agent)
        blue_agent.load_amm()
        

        # create red agents
        for _ in range(self.num_red_agents):
            x = random.randint(-self.width/2.0, self.width/2.0)
            y = random.randint(-self.height/2.0, self.height/2.0)
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            sprites.append(Agent(x, y, "triangle", "red", "red"))
            sprites[-1].dx = dx
            sprites[-1].dy = dy


    def render_border(self, pen):
        pen.color("white")
        pen.width(3)
        pen.penup()

        left = -self.width/2.0
        right = self.width/2.0
        top = self.height/2.0
        bottom = -self.height/2.0

        pen.goto(left, top)
        pen.pendown()
        pen.goto(right, top)
        pen.goto(right, bottom)
        pen.goto(left, bottom)
        pen.goto(left, top)
        pen.penup()
        

class Sprite:
    """
    Base class for all game objects.

    Attributes:
        x: x coordinate of the sprite
        y: y coordinate of the sprite
        shape: shape of the sprite
        color: color of the sprite
        dx: change in x +dx right, -dx left
        dy: change in y +dy up, -dy down
    """
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.heading = 0
        self.dx = 0
        self.dy = 0
        self.da = 0
        self.thrust = 0.0
        self.acceleration = 0.5
        self.health = 100
        self.max_health = 100
        self.max_fuel = 1000
        self.prox_fuse_radius = 20
        self.radar = 900
        self.state = "alive"

    def collision(self, other):
        if math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2) < self.prox_fuse_radius:
            return True
        else:
            return False

    def update(self):
        if self.state == "alive":
            self.heading += self.da
            self.heading %= 360
            self.dx += self.thrust * math.cos(math.radians(self.heading))
            self.dy += self.thrust * math.sin(math.radians(self.heading))
            self.x += self.dx
            self.y += self.dy

            # check for boarder collision
            self.boarder_check()

            # check health
            if self.health <= 0:
                self.state = "dead"

    def boarder_check(self):
        """
        Checks if the sprite is off the screen.
        """
        if self.x > env.width/2.0 - 10:
            self.x = env.width/2.0 - 10
            self.dx *= -1
        elif self.x < -env.width/2.0 + 10:
            self.x = -env.width/2.0 + 10
            self.dx *= -1
        if self.y > env.height/2.0 - 10:
            self.y = env.height/2.0 - 10
            self.dy *= -1
        elif self.y < -env.height/2.0 + 10:
            self.y = -env.height/2.0 + 10
            self.dy *= -1

    def render(self, pen):
        if self.state == "alive": 
            pen.goto(self.x, self.y)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.setheading(self.heading)
            pen.stamp()

            # render the health meter
            self.render_health_meter(pen)

    def render_health_meter(self, pen):
        """
        Draw health meter above sprite.
        """
        # go to the top of where the sprite is
        pen.goto(self.x - 10, self.y + 20)
        pen.width(3)
        # start drawing
        pen.pendown()
        pen.setheading(0)

        # draw the health bar
        if self.health/self.max_health < 0.3:
            pen.color("red")
        elif self.health/self.max_health < 0.7:
            pen.color("yellow")
        else:
            pen.color("green")

        pen.fd(20 * (self.health/self.max_health))
        if self.health != self.max_health:
            pen.color("grey")
            pen.fd(20 * ((self.max_health - self.health)/self.max_health))

        # stop drawing
        pen.penup()


class Agent(Sprite):
    """
    Agent class for all agent game objects. 
    """
    def __init__(self, x, y, shape, color, team):
        super().__init__(x, y, shape, color)
        self.team = team
        self.health = 100
        self.score = 0
        self.heading = 90
        self.da = 0
        self.num_aam = 4
        self.aam_loadout = []

    def rotate_left(self):
        self.da = 5

    def rotate_right(self):
        self.da = -5

    def stop_rotation(self):
        self.da = 0

    def accelerate(self):
        # TODO: make this a throttle position instead
        self.thrust += self.acceleration

    def decelerate(self):
        self.thrust = 0.0

    def load_amm(self):
        for _ in range(self.num_aam):
            aam = AAM(self.x, self.y, "triangle", "yellow", self.team)
            self.aam_loadout.append(aam)
            sprites.append(aam)

    def fire_aam(self):
        if len(self.aam_loadout) > 0:
            aam = self.aam_loadout.pop()
            aam.fire(self.x, self.y, self.heading, self.dx, self.dy)

    def render(self, pen):
        if self.state == "alive":
            pen.goto(self.x, self.y)
            pen.shape(self.shape)
            pen.shapesize(0.5, 1.0, None)
            pen.color(self.color)
            pen.setheading(self.heading)
            pen.stamp()

            # revert the size of the pen after drawing the agent
            pen.shapesize(1.0, 1.0, None)

            # render the health meter
            self.render_health_meter(pen)


class AAM(Agent):
    """
    Air-to-Air Missile (AAM) weapon game objects.
    """
    def __init__(self, x, y, shape, color, team):
        super().__init__(x, y, shape, color, team)
        self.team = team
        self.x = x
        self.y = y
        self.max_fuel = 300
        self.fuel = self.max_fuel
        self.thrust = 4.0
        self.prox_fuse_radius = 4
        # TODO: make this a function of probability of kill based on range
        self.damage = 50
        self.warmup_delay = 1

    def fire(self, x, y, heading, dx, dy):
        if self.state == "alive":
            self.state = "away"
            self.x = x
            self.y = y
            self.heading = heading
            self.dx = dx
            self.dy = dy
            
            # launch weapon
            self.dx = math.cos(math.radians(self.heading)) * self.thrust
            self.dy = math.sin(math.radians(self.heading)) * self.thrust

    def update(self):
        if self.state == "away":
            self.fuel -= self.thrust
            if self.fuel <= 0:
                self.state = "dead"
            self.heading += self.da
            self.heading %= 360
            self.x += self.dx
            self.y += self.dy

    def render(self, pen):
        if self.state == "away":
            pen.shapesize(0.2, 0.2, None)
            pen.goto(self.x, self.y)
            pen.setheading(self.heading)
            pen.color(self.color)
            pen.stamp()

# create environment
env = Environment()

# sprites list
sprites = []

# build scenario environment
env.build_scenario()

# keyboard bindings
blue_agent = sprites[0]
wn.listen()
wn.onkeypress(blue_agent.rotate_left, "Left")
wn.onkeypress(blue_agent.rotate_right, "Right")
wn.onkeyrelease(blue_agent.stop_rotation, "Left")
wn.onkeyrelease(blue_agent.stop_rotation, "Right")
# TODO: make this a throttle position instead with up and down arrows
wn.onkeypress(blue_agent.accelerate, "Up")
wn.onkeyrelease(blue_agent.decelerate, "Up")
# TODO: make this a weapon type selection as well
wn.onkeypress(blue_agent.fire_aam, "space")

# main loop
while True:
    # clear screen
    pen.clear()

    # render environment
    env.render_border(pen)

    # update sprites
    for sprite in sprites:
        sprite.update()

    # check for collisions
    for sprite1, sprite2 in zip(sprites, sprites[1:]):
        # FIXME: need to implement a warmup delay to prevent killing yourself on launch
        if sprite1.team != sprite2.team:
            if sprite1.state == "alive" and sprite2.state == "alive":
                if sprite1.collision(sprite2):
                    if isinstance(sprite1, Agent) and isinstance(sprite2, Agent):
                        sprite1.state = "dead"
                        sprite2.state = "dead"
                    elif isinstance(sprite1, AAM) and isinstance(sprite2, AAM):
                        sprite1.state = "dead"
                        sprite2.state = "dead"
                    elif (isinstance(sprite1, AAM) and isinstance(sprite2, Agent)):
                        sprite1.state = "dead"
                        sprite2.health -= sprite1.damage
                    elif isinstance(sprite1, Agent) and isinstance(sprite2, AAM):
                        sprite1.health -= sprite2.damage
                        sprite2.state = "dead"
                    
    # render sprites
    for sprite in sprites:
        sprite.render(pen)

    # check for end of battle
    if not any(sprite.team == "red" and sprite.state == "alive" for sprite in sprites):
        env.end_of_battle = True
        winner = "Blue Team"
    elif not any(sprite.team == "blue" and sprite.state == "alive" for sprite in sprites):
        env.end_of_battle = True
        winner = "Red Team"
    # TODO: if white is dead, REDFOR wins
    
    if env.end_of_battle == True:
        pen.color("white")
        pen.goto(0, 0)
        pen.write("End of Battle. {} Wins!".format(winner), align="center", font=("Courier", 24, "normal"))

    # update screen
    wn.update()