import math
import turtle
import random
import itertools

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
        """
        Build the scenario based on the config files.
        """

        sprites.clear()
        # create blue agent sprite
        blue_agent = Agent(0, 0, "blue")
        sprites.append(blue_agent)
        # TODO: load multiple different weapon types based on config file
        blue_agent.load_amm()
        
        # create red agents
        for _ in range(self.num_red_agents):
            x = random.randint(-self.width/2.0, self.width/2.0)
            y = random.randint(-self.height/2.0, self.height/2.0)
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            sprites.append(Agent(x, y,"red"))
            sprites[-1].dx = dx
            sprites[-1].dy = dy


    def render_border(self, pen):
        """
        Render the game border to establish the boundaries of the game.
        """
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
        self.thrust = 0.1
        self.acceleration = 0.5
        self.health = 100
        self.max_health = 100
        self.max_fuel = 1000
        self.radar = 900
        self.alive = True
        self.state = "ready"

    def collision(self, other, radius=0):
        """
        Check if two sprites have collided, based on a collision radius.
        """
        dist = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        if dist <= radius:
            return True
        else:
            return False

    def update(self):
        """
        Update the sprite step.
        """
        if self.alive:
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
                self.alive = False

    def boarder_check(self):
        """
        Checks if the sprite is off the screen.
        """
        if self.x > env.width/2.0 - 10:
            self.x = env.width/2.0 - 10
            self.dx *= -0.1
        elif self.x < -env.width/2.0 + 10:
            self.x = -env.width/2.0 + 10
            self.dx *= -0.1
        if self.y > env.height/2.0 - 10:
            self.y = env.height/2.0 - 10
            self.dy *= -0.1
        elif self.y < -env.height/2.0 + 10:
            self.y = -env.height/2.0 + 10
            self.dy *= -0.1

    def render(self, pen):
        """
        Draw the sprite.
        """
        if self.alive: 
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
    def __init__(self, x, y, team):
        super().__init__(x, y, "triangle", team)
        self.team = team
        self.health = 100
        self.score = 0
        self.heading = 90
        self.da = 0
        self.num_aam = 50
        self.aam_loadout = []

    def rotate_left(self):
        """
        Rotate the agent to the left.
        """
        self.da = 5

    def rotate_right(self):
        """
        Rotate the agent to the right.
        """
        self.da = -5

    def stop_rotation(self):
        """
        Stop rotating the agent.
        """
        self.da = 0

    def accelerate(self):
        """
        Increase agent thrust.
        """
        # TODO: make this a throttle position instead
        self.thrust += self.acceleration

    def decelerate(self):
        """
        Decrease agent thrust.
        """
        self.thrust = 0.0

    def load_amm(self):
        """
        Add the agent's air-to-air missile (AAM) loadout.
        """
        for _ in range(self.num_aam):
            aam = AAM(self.x, self.y, self.team)
            self.aam_loadout.append(aam)
            sprites.append(aam)

    def fire_aam(self):
        """
        Fire an air-to-air missile (AAM) if there is one available.
        """
        if len(self.aam_loadout) > 0:
            aam = self.aam_loadout.pop()
            aam.fire(self.x, self.y, self.heading, self.dx, self.dy)

    def render(self, pen):
        """
        Draw the agent
        """
        if self.alive:
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
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.team = team
        self.x = x
        self.y = y
        self.max_fuel = 500
        self.fuel = self.max_fuel
        self.thrust = 1.0
        self.prox_fuse_radius = 4
        # TODO: make this a function of probability of kill based on range
        self.damage = 50
        self.warmup_delay = 10
        self.prox_fuse_radius = 20

    def fire(self, x, y, heading, dx, dy):
        """
        Seperate the AAM from the agent and give it thrust.
        """
        if self.alive:
            self.state = "away"
            self.x = x
            self.y = y
            self.heading = heading
            self.dx = dx
            self.dy = dy
            
            # launch weapon
            self.dx = self.thrust * math.cos(math.radians(self.heading))
            self.dy = self.thrust * math.sin(math.radians(self.heading))

    def update(self):
        """
        Update the AAM step.
        """
        if self.state == "away":
            self.fuel -= self.thrust
            if self.fuel <= 0:
                self.alive = False
            self.dx += self.thrust * math.cos(math.radians(self.heading))
            self.dy += self.thrust * math.sin(math.radians(self.heading))
            self.x += self.dx
            self.y += self.dy
            

    def render(self, pen):
        """
        Draw the AAM.
        """
        if self.state == "away":
            pen.shape(self.shape)
            pen.shapesize(0.1, 0.2, None)
            pen.goto(self.x, self.y)
            pen.setheading(self.heading)
            pen.color(self.color)
            pen.stamp()
    
    
class GNC():
    """
    Guidance, Navigation, and Control (GNC).
    """
    # FIXME: do this all properly when i have time with velocity and acceleration
    def __init__(self):
        pass

    def clos(agent, target):
        """
        Basic Command to Line of Sight (CLOS) guidance law.
        """
        # set heading to target
        heading = math.degrees(math.atan2(target.y - agent.y, target.x - agent.x))

        return heading


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
        if sprite.team == "red" and sprite.alive:
            sprite.heading = GNC.clos(sprite, blue_agent)
            sprite.thrust = 0.05
        sprite.update()

    # check for collisions
    for sprite1, sprite2 in itertools.combinations(sprites, 2):
        # FIXME: need to implement a warmup delay to prevent killing yourself on launch
        if sprite1.team != sprite2.team and sprite1.alive and sprite2.alive:
            if isinstance(sprite1, Agent) and isinstance(sprite2, Agent) and sprite1.collision(sprite2):
                    sprite1.alive = False
                    sprite2.alive = False
            elif isinstance(sprite1, AAM) and isinstance(sprite2, AAM) and sprite1.collision(sprite2, sprite1.prox_fuse_radius):
                    sprite1.alive = False
                    sprite2.alive = False
            elif isinstance(sprite1, AAM) and isinstance(sprite2, Agent) and sprite1.collision(sprite2, sprite1.prox_fuse_radius):
                sprite1.alive = False
                sprite2.health -= sprite1.damage
            elif isinstance(sprite1, Agent) and isinstance(sprite2, AAM) and sprite1.collision(sprite2, sprite2.prox_fuse_radius):
                sprite1.health -= sprite2.damage
                sprite2.alive = False
                    
    # render sprites
    for sprite in sprites:
        sprite.render(pen)

    # check for end of battle
    if not any(sprite.team == "red" and sprite.alive for sprite in sprites):
        env.end_of_battle = True
        winner = "Blue Team"
    elif not any(sprite.team == "blue" and sprite.alive for sprite in sprites):
        env.end_of_battle = True
        winner = "Red Team"
    # TODO: if white is dead, REDFOR wins
    
    if env.end_of_battle == True:
        pen.color("white")
        pen.goto(0, 0)
        pen.write("End of Battle. {} Wins!".format(winner), align="center", font=("Courier", 24, "normal"))

    # update screen
    wn.update()