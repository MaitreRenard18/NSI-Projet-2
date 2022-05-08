#Imports
from math import floor
import pygame
import random
import os
import sys

#Initialisation
pygame.init()
screen = pygame.display.set_mode((1056, 832)) #Créer la fenêtre
pygame.display.set_caption('Terrario') #Renomme la fenêtre

#Chargement des textures
textures = {}
for file in os.listdir("{}\Textures".format(os.getcwd())): #Récupère toute les fichiers se trouvant dans le dossier textures
    if file.endswith(".png"): #Vérifie qu'il sagit d'un png
        file_name = file.replace(".png", "").lower() #Créer un nom en minuscule sans le png
        
        path = "{}\Textures\{}".format(os.getcwd(), file) #Récupère l'emplacement du ficher
        image = pygame.image.load(path) #Charge l'image

        textures[file_name] = image #Ajoute une l'image dans le dictionnaire texture

#Class carte
class map:
    def __init__(self, width, height): #Prend en paramètre une largeur et une hauter
        self.width = width
        self.height = height

        self.tiles = [] #Liste ou les "tuiles" sont stockées sous le format [x][y]
        self.generate() #Appelle la fonction generate qui genère la carte
    
    def generate(self):
        print("Génération des tuiles.")

        for x in range(self.width - 1):
            sys.stdout.write('\r') #Affiche la progression dans la console
            sys.stdout.write("{}%".format(floor((x / (self.width - 1)) * 100) + 1))
            sys.stdout.flush()

            self.tiles.append([]) #Ajoute un tableau dans "tiles" qui represente une colone

            for y in range(self.height): #Pour chaques lignes dans la colone, des tuiles sont générées en fonction du numéro de ligne
                if y == 0:
                    self.tiles[x].append("air")

                elif y == 1:
                    self.tiles[x].append("grass")

                elif y == 2:
                    self.tiles[x].append("dirt")

                elif y == 3:
                    self.tiles[x].append(random.choice(["dirt", "dirt", "stone"])) #Une chance sur 3 qu'il s'agisse de pierre

                elif y == 4:
                    self.tiles[x].append(random.choice(["dirt", "stone"]))

                elif y < 8:
                    self.tiles[x].append("stone")

                elif y < 12:
                    choices = ["stone" for _ in range(16)] #Initialise un tableau avec 16 pierres
                    choices.append("coal") #Ajoute une tuile de charbon

                    self.tiles[x].append(random.choice(choices)) #Choisi une tuile parmit "choices" (1 chance sur 17 qu'il sagit d'un mineraix de charbon)

                elif y < 64:
                    choices = ["stone" for _ in range(32)]
                    choices.append("coal")
                    choices.append("coal")
                    choices.append("iron")

                    self.tiles[x].append(random.choice(choices))

                elif y < 256:
                    choices = ["stone" for _ in range(64)]
                    choices.append("iron")
                    choices.append("iron")
                    choices.append("gold")

                    self.tiles[x].append(random.choice(choices))

                elif y < 512:
                    choices = ["stone" for _ in range(128)]
                    choices.append("gold")
                    choices.append("gold")
                    choices.append("diamond")

                    self.tiles[x].append(random.choice(choices))

                elif y < 750:
                    choices = ["stone" for _ in range(128)]
                    choices.append("diamond")
                    choices.append("diamond")
                    choices.append("ruby")

                    self.tiles[x].append(random.choice(choices))
        
        print("\nGénération des grottes.")
        for i in range(750): #Génère 750 grottes
            sys.stdout.write('\r') #Affiche la progression dans la console
            sys.stdout.write("{}%".format(floor((i / 750) * 100) + 1))
            sys.stdout.flush()

            max_size = random.randint(32, 64) #Prend une taille aléatoire en 32 et 64 tuiles
            self.dig((random.randint(0, self.width), random.randint(4, self.height)), max_size) #Appelle la fonction dig qui génère une grotte

        for x in range(self.width - 1):
            self.tiles[x][0] = "air" #Ajoute une couche d'air à la surface
            self.tiles[x][-3] = random.choice(["stone", "bedrock"]) #Génère de la "bedrock" au fond de la carte
            self.tiles[x][-2] = random.choice(["stone", "bedrock", "bedrock"])
            self.tiles[x][-1] = "bedrock"

        print("\nGénération terminée.")

    def dig(self, position, max_size, size = 0): #Prend en paramètre une position (tuple), une taille max, et une taille actuelle (Qui augmente de 1 à chaque appelle)
        x, y = position

        if size == max_size or x > len(self.tiles) - 1 or y > len(self.tiles[x]) - 1: #Si la grotte à attend sa taille max. ou que les bordure de la map ont été atteinte, arrêter la génération
            return

        size += 1 #Augmente la taille
        self.tiles[x][y] = "cave" #Met une tuille de "grotte" a l'emplacement x, y

        choises = [] #Initialise un tableau ou les possiblités d'extension de la grotte seront stocker
        if x + 1 < len(self.tiles) and self.tiles[x + 1][y] != "cave": #Verifie si la grotte peut s'éttendre à droite
            choises.append((x + 1, y))

        if x - 1 >= 0 and self.tiles[x - 1][y] != "cave": #A droite
            choises.append((x - 1, y))

        if y + 1 < len(self.tiles[x]) and self.tiles[x][y + 1] != "cave": #En bas
            choises.append((x, y + 1))

        if y - 1 >= 0 and self.tiles[x][y - 1] != "cave": #En haut
            choises.append((x, y - 1))
        
        if len(choises) == 0: #Vérifie que la grotte peut s'éttendre
            return

        branch = [1 for _ in range(9)]
        branch.append(2)
        branch = random.choice(branch) #Choisie en combien de "branches" la grotte va s'éttendre (1 chance sur 10 qu'il y ait 2 embranchements)

        for _ in range(branch): #Appelle plusieurs fois la fonction dig en fonction du nombre d'embranchements
            self.dig(random.choice(choises), max_size, size)

    def render(self, offset): #Fonction qui affiche la carte, en prennant en paramètre la position de la camera
        screen.fill((145, 226, 255)) #Met le fond en bleu pour simuler du ciel 

        screensize = screen.get_size() #Récupère la taille de l'écran pour regarder combien de tuiles peuvent être afficher en même temps
        x_tile_number = screensize[0] // 32 + (screensize[0] % 32 > 0) 
        y_tile_number = screensize[1] // 32 + (screensize[1] % 32 > 0)

        for x in range(offset[0], offset[0] + x_tile_number): #Pour chaques colones visibles sur l'écran
            for y in range(offset[1], offset[1] + y_tile_number): #Pour chaques lignes visibles sur l'écran
                x_index = None if x < 0 or x > len(self.tiles) - 1 else x #Vérifie que la colone existe
                y_index = None if y < 0 or y > len(self.tiles[0]) - 1 else y #Vérifie que la ligne existe
                
                if x_index != None and y_index != None: #Si la colone et la ligne existent
                    texture = textures[self.tiles[x_index][y_index]] #Récupère la texture dans "tiles"
                    screen.blit(pygame.transform.scale(texture, (32, 32)), (x * 32 - offset[0] * 32, y * 32 - offset[1] * 32)) #Et l'affiche sur l'écran

#Class joueur
class player:
    def __init__(self, map): #Prend en paramètre la carte sur lequel le joueur se trouve
        self.position = (map.width // 2, 0) #Prend comme position de depart x le milieu de la carte et y la surface
        self.speed = 1
        
        self.map = map
        self.texture = "drill_base_right" #Texture par défaut de la foreuse

    def get_camera_offset(self): #Retourne la position de la caméra, c'est à dire le bord supérieur gauche de l'écran, pour permettre au drill d'être afficher au centre (Et non pas en haut à gauche)
        screensize = screen.get_size() #Récupère la taille de l'écran pour calculer la position du bord (Position par rapport à map.tiles)
        x = floor(self.position[0]) - (screensize[0] // 32) // 2
        y = floor(self.position[1]) - (screensize[1] // 32) // 2

        return (x, y)

    def tick(self): #Fonction appeller à chaque "Frame"
        screensize = screen.get_size()
        screen.blit(pygame.transform.scale(textures[self.texture], (32, 32)), (screensize[0] // 2 - 16, screensize[1] // 2)) #Affiche la foreuse au centre de l'écran

        if self.texture == "drill_base_right": #Affiche la pointe de la foreuse
            screen.blit(pygame.transform.scale(textures["drill_right"], (32, 32)), (screensize[0] // 2 - 16 + 32, screensize[1] // 2))
        elif self.texture == "drill_base_left":
            screen.blit(pygame.transform.scale(textures["drill_left"], (32, 32)), (screensize[0] // 2 - 16 - 32, screensize[1] // 2))
        elif self.texture == "drill_base_up":
            screen.blit(pygame.transform.scale(textures["drill_up"], (32, 32)), (screensize[0] // 2 - 16, screensize[1] // 2  - 32))
        else:
            screen.blit(pygame.transform.scale(textures["drill_down"], (32, 32)), (screensize[0] // 2 - 16, screensize[1] // 2  + 32))

        x, y = floor(self.position[0]), floor(self.position[1]) #Position de la foreuse

        if self.map.tiles[x][y] != "scaffolding" and self.map.tiles[x][y] != "cave" and y != 0: #Si la foreuse se trouve en souterrain et n'est pas sur un échafaudage affiche une texture de grotte
            self.map.tiles[x][y] = "cave"

        if self.map.tiles[x][y + 1] == "cave": #Si la foreuse se trouve au dessus du vide, la faire tomber
            screen.blit(pygame.transform.scale(textures["parachute"], (32, 32)), (screensize[0] // 2 - 16, screensize[1] // 2 - 32)) #Affiche une texture de parachute quand elle tombe
            self.position = (x, self.position[1] + .15) #Diminue sa position
            return #Arrête l'execution de la fonction pour empecher le mouvement

        keys = pygame.key.get_pressed() #Récupère les boutons actuellement pressés
        if keys[pygame.K_RIGHT] and self.map.tiles[x + 1][y] != "bedrock": #Si droite est présser et qu'il n'y a pas de "bedrock" aller a droite
            self.position = (self.position[0] + self.speed * .1, y)
            self.texture = "drill_base_right" #Change la texture pour afficher celler qui vas à droite
            return

        if keys[pygame.K_LEFT] and self.map.tiles[x - 1][y] != "bedrock": #Idem
            self.position = (self.position[0] - self.speed * .1, y)
            self.texture = "drill_base_left"
            return

        if keys[pygame.K_UP] and self.map.tiles[x][y - 1] != "bedrock" and y > 0: #Idem mais vérifie également si la foreuse se trouve a la surface
            self.position = (self.position[0], self.position[1] - self.speed * .1)
            self.texture = "drill_base_up"

            if floor(self.position[1]) == y - 1:
                self.map.tiles[x][y] = "scaffolding"
            
            return

        if keys[pygame.K_DOWN] and self.map.tiles[x][y + 1] != "bedrock": #Idem
            self.position = (x, self.position[1] + self.speed * .1)
            self.texture = "drill_base_down"
            return

#Boucle principal
clock = pygame.time.Clock() #Créer une "clock" qui permet de limiter la vitesse d'excution maximal grace à la fonction tick()
level = map(1024, 1024) #Créer une carte de 1024 * 1024
drill = player(level) #Créer le joueur ayant comme paramètre la carte

running = True
while running: #Boucle principal qui execute toutes les fonctions à chaques frames
    clock.tick(60) 

    level.render(drill.get_camera_offset()) #Affiche la carte avec une position de camera obtenue grace à fonction get_camera_offset()
    drill.tick() #"Met a jour" la foreuse

    pygame.display.flip() #met à jour l'affichage

    for event in pygame.event.get(): #Petmet d'arrêter la boucle (Et donc le jeu si la fenêtre est fermée)
        if event.type == pygame.QUIT:
            running = False
