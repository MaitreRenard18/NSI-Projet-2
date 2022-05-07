#Imports
from math import floor
import pygame
import random
import os

#Initialisation
pygame.init()
screen = pygame.display.set_mode((1056, 832))
pygame.display.set_caption('Minecraft Ultimate HD Deluxe Definitive Edition')

#Textures
textures = {}
for file in os.listdir("{}\Textures".format(os.getcwd())):
    if file.endswith(".png"):
        file_name = file.replace(".png", "").lower()
        
        path = "{}\Textures\{}".format(os.getcwd(), file)
        image = pygame.transform.scale(pygame.image.load(path), (32, 32))

        textures[file_name] = image

#Carte
class map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tiles = []
        self.generate()
    
    def generate(self):
        for x in range(self.width):
            self.tiles.append([])

            for y in range(self.height):
                if y == 0:
                    self.tiles[x].append("grass")
                elif y == 1:
                    self.tiles[x].append("dirt")
                elif y < 4:
                    self.tiles[x].append(random.choice(["dirt", "stone"]))
                elif y < 8:
                    self.tiles[x].append("stone")
                else:
                    choices = ["stone" for _ in range(12)]
                    choices.append("coal")

                    self.tiles[x].append(random.choice(choices))

    def render(self, offset):
        screen.fill((145, 226, 255))

        screensize = screen.get_size()
        x_tile_number = screensize[0] // 32 + (screensize[0] % 32 > 0)
        y_tile_number = screensize[1] // 32 + (screensize[1] % 32 > 0)

        for x in range(offset[0], offset[0] + x_tile_number):
            for y in range(offset[1], offset[1] + y_tile_number):
                x_index = None if x < 0 or x > self.width - 1 else x
                y_index = None if y < 0 or y > self.height - 1 else y
                
                if x_index != None and y_index != None:
                    texture = textures[self.tiles[x_index][y_index]]
                    screen.blit(texture, (x * 32 + -offset[0] * 32, y * 32 + -offset[1] * 32))

#Grottes
def dig(position, map, n):
    if n == 0:
        return
    else:
        n -= 1

    x = position[0]
    y = position[1]

    screen.blit(textures["cave"] , (x * 32, y * 32))
    map[x][y] = "cave"
    pygame.display.flip()

    choises = []

    if x + 1 < len(map) and map[x + 1][y] != "cave":
        choises.append((x + 1, y))

    if x - 1 >= 0 and map[x - 1][y] != "cave":
        choises.append((x - 1, y))

    if y + 1 < len(map[x]) and map[x][y + 1] != "cave":
        choises.append((x, y + 1))

    if y - 1 >= 0 and map[x][y - 1] != "cave":
        choises.append((x, y - 1))
    
    try :
        node = [1 for _ in range(9)]
        node.append(2)
        node = random.choice(node)

        for _ in range(node):
            dig(random.choice(choises), map, n)
    except:
        return

#Joueur
class player:
    def __init__(self, map):
        self.position = (map.width // 2, -1)
        self.speed = 1
        
        self.map = map
        self.texture = "drill_base_right"

    def get_camera_offset(self):
        screensize = screen.get_size()
        x = floor(self.position[0]) - (screensize[0] // 32) // 2
        y = floor(self.position[1]) - (screensize[1] // 32) // 2

        return (x, y)

    def tick(self):
        screensize = screen.get_size()
        screen.blit(textures[self.texture] , (screensize[0] // 2 - 16, screensize[1] // 2))

        self.map.tiles[floor(self.position[0])][floor(self.position[1])] = "cave"

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.position = (self.position[0] + self.speed * .1, self.position[1])
            self.texture = "drill_base_right"
            return

        if keys[pygame.K_LEFT]:
            self.position = (self.position[0] - self.speed * .1, self.position[1])
            self.texture = "drill_base_left"
            return

        if keys[pygame.K_UP] and self.position[1] > -1:
            self.position = (self.position[0], self.position[1] - self.speed * .1)
            self.texture = "drill_base_up"
            return

        if keys[pygame.K_DOWN]:
            self.position = (self.position[0], self.position[1] + self.speed * .1)
            self.texture = "drill_base_down"
            return

#Game loop
clock = pygame.time.Clock()

print("Génération du monde")
level = map(256, 256)

print("Génération des grottes")
for _ in range(32):
    dig((random.randint(0, len(level.tiles)), random.randint(4, len(level.tiles[0]))), level.tiles, 32)

print("Génération terminée")

drill = player(level)

running = True
while running:
    clock.tick(60)

    level.render(drill.get_camera_offset())
    drill.tick()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False