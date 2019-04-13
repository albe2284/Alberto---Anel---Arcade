import os.path
import arcade
import math
import random

"""Sprites fra: https://www.kenney.nl/assets/space-shooter-redux"""

"""Vi definere og ændre variablerne til vores spil, når vi skal execute "Arcade" funktionen der starter spillet. """

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800
SCREEN_TITLE = "Spaceships vs Astroids"

""" Vi laver en loop, hvor vi finder alle billederne/mapperne 
som skal importers ind, de bliver gemt i en array (Billeder)"""

BilledeMappe = os.listdir("sprites")
Billeder = {}
for x in BilledeMappe:
    BilledeMappe2 = os.listdir("sprites/" + x)
    for y in BilledeMappe2:
        if y[-3:].lower() == "png":
            Billeder[y.format(x)] = ("sprites/" + x + "/" + y)
        elif y == 'Meteors':
            BilledeMappe3 = os.listdir("sprites/" + x + "/Meteors")
            for d in BilledeMappe3:
                Billeder[d.format(x)] = ("sprites/" + x + "/" + y +"/"+ d)

class playerone:
    def __init__(self, change_y, posX, posY, angle):
        self.position_x = posX
        self.position_y = posY
        self.change_y = change_y
        self.angle = angle
        self.speed = 0
        self.drag = 0.05
        self.SpeedStatus = 0
        for x in Billeder:
            if x == "playerShip1_red.png":
                self.sprite = arcade.load_texture(Billeder[x])
                break

    def draw(self):
        arcade.draw_texture_rectangle(self.position_x, self.position_y, 40,
                                      40, self.sprite, self.angle)

    def update(self, test, anglechange):
        self.angle += anglechange
        angle_rad = math.radians(self.angle)
        self.position_y += test * math.cos(angle_rad)
        self.position_x += -test * math.sin(angle_rad)
        if test == 0 and (self.SpeedStatus > 0.5 or self.SpeedStatus < -0.5):
            if self.SpeedStatus < 0:
                self.SpeedStatus += self.drag
            else:
                self.SpeedStatus -= self.drag

            self.position_y += self.SpeedStatus * math.cos(angle_rad)
            self.position_x += -self.SpeedStatus * math.sin(angle_rad)
        else:
            self.SpeedStatus = test




class Sten:
    def __init__(self, ):
        self.big = []
        self.spawns = []
        self.xSpawn = []
        self.ySpawn = []
        self.Sten = []
        self.StenDirection = []
        self.StenSpeed = []
        for x in Billeder:
            if x[:3] == "Big":
                self.big.append(arcade.load_texture(Billeder[x]))

        for x in range(5):
            self.xSpawn.append(random.randint(100, 700))
            self.ySpawn.append(random.randint(100, 700))
            self.spawns.append(random.choice(self.big))
            self.StenDirection.append(random.randint(0, 360))
            self.StenSpeed.append(random.randint(1, 3))


    def draw(self):
        for x in range(5):
            self.Sten.append(arcade.draw_texture_rectangle(self.xSpawn[x], self.ySpawn[x], 100,
                                        100, self.spawns[x]))

    def update(self):
        for x in range(5):
            angle_rad = math.radians(self.StenDirection[x])
            self.xSpawn[x] += self.StenSpeed[x] * math.cos(angle_rad)
            self.ySpawn[x] += -self.StenSpeed[x] * math.sin(angle_rad)







class game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = None
        self.MenuStatus = "MainMenu"
        self.SPEED = 0
        self.ROTATION = 0
        self.position_x2 = 395
        self.position_y2 = 50
        self.angleRotation = 0
        self.drag = 0
        self.player1 = playerone(self.ROTATION, self.position_x2, self.position_y2, self.angleRotation)
        self.Sten = Sten()

    def setup(self):
        for x in Billeder:
            if x == "BG1.png":
                self.background = arcade.load_texture(Billeder[x])
                break

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH,
                                      SCREEN_HEIGHT, self.background)

        self.player1.draw()
        self.Sten.draw()

    def update(self, delta_time: 1):
        self.player1.update(self.SPEED, self.angleRotation)
        self.Sten.update()


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.SPEED = 3
        elif symbol == arcade.key.DOWN:
            self.SPEED = -3
        elif symbol == arcade.key.LEFT:
            self.angleRotation = 3
        elif symbol == arcade.key.RIGHT:
            self.angleRotation = -3

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.SPEED = 0
            self.player1.update(self.SPEED, self.angleRotation)
        elif symbol == arcade.key.DOWN:
            self.SPEED = 0
            self.player1.update(self.SPEED, self.angleRotation)
        elif symbol == arcade.key.LEFT:
            self.angleRotation = 0
        elif symbol == arcade.key.RIGHT:
            self.angleRotation = 0




window = game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
