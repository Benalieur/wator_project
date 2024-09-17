import random as rd
from datetime import datetime as dt

import pygame
from pygame.locals import *


# Classe représentant un poisson
class Fish:
    def __init__(self, x, y, grid, reproduction_time):
        """
        Initialise un poisson à une position aléatoire dans la grille.
        reproduction_time : nombre de chronons avant la reproduction
        """
        self.chronos = 0
        self.reproduction_time = reproduction_time
        self.x = x
        self.y = y
        self.grid = grid
        self.grid.set(self.x, self.y, 1)  # 1 représente un poisson

    def move(self):
        """
        Déplace le poisson de manière aléatoire et gère la reproduction.
        Si le poisson se déplace hors de la grille, il réapparaît de l'autre côté (effet tore).
        """
        self.chronos += 1
        direction = rd.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Haut, bas, droite, gauche
        new_x = (self.x + direction[0]) % self.grid.size  # Si on dépasse les limites, on réapparaît de l'autre côté
        new_y = (self.y + direction[1]) % self.grid.size

        if self.grid.get(new_x, new_y) == 0:  # Vérifie si la case est vide
            if self.chronos >= self.reproduction_time:  # Reproduction
                self.chronos = 0
                new_fish = Fish(self.x, self.y, self.grid, self.reproduction_time)  # Laisser un nouveau poisson
                self.grid.fishes.append(new_fish)  # Ajouter le nouveau poisson à la liste des poissons
            else:
                self.grid.set(self.x, self.y, 0)  # Efface l'ancienne position

            self.x, self.y = new_x, new_y
            self.grid.set(self.x, self.y, 1)  # Met à jour la nouvelle position


# Classe représentant un requin, hérite de la classe Fish
class Shark(Fish):
    def __init__(self, x, y, grid, reproduction_time, starvation_time):
        """
        Initialise un requin à une position donnée dans la grille.
        reproduction_time : nombre de chronons avant la reproduction
        starvation_time : nombre de chronons avant la mort par faim
        """
        super().__init__(x, y, grid, reproduction_time)
        self.starvation_time = starvation_time
        self.starvation_chronos = 0
        self.grid.set(self.x, self.y, 2)  # 2 représente un requin

    def move(self):
        """
        Déplace le requin de manière aléatoire, mange les poissons s'il y en a à côté, 
        gère la reproduction et la faim.
        """
        self.chronos += 1
        self.starvation_chronos += 1

        # Les directions possibles (haut, bas, droite, gauche)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        possible_moves = []

        # Recherche des poissons dans les cases adjacentes
        for direction in directions:
            new_x = (self.x + direction[0]) % self.grid.size
            new_y = (self.y + direction[1]) % self.grid.size
            if self.grid.get(new_x, new_y) == 1:  # Un poisson est là
                possible_moves.append((new_x, new_y))

        if possible_moves:
            # Mange un poisson
            new_x, new_y = rd.choice(possible_moves)
            self.grid.set(new_x, new_y, 0)  # Retire le poisson de la grille
            self.grid.fishes = [fish for fish in self.grid.fishes if not (fish.x == new_x and fish.y == new_y)]  # Retire le poisson mangé
            self.starvation_chronos = 0  # Réinitialise le chronos de famine
        else:
            # Si aucun poisson à proximité, on bouge normalement
            direction = rd.choice(directions)
            new_x = (self.x + direction[0]) % self.grid.size
            new_y = (self.y + direction[1]) % self.grid.size

        if self.grid.get(new_x, new_y) == 0:  # Si la case est vide
            if self.chronos >= self.reproduction_time:  # Reproduction
                self.chronos = 0
                new_shark = Shark(self.x, self.y, self.grid, self.reproduction_time, self.starvation_time)
                self.grid.sharks.append(new_shark)  # Ajoute le nouveau requin
            else:
                self.grid.set(self.x, self.y, 0)  # Efface l'ancienne position

            self.x, self.y = new_x, new_y
            self.grid.set(self.x, self.y, 2)  # Met à jour la nouvelle position pour le requin

        # Si le requin a faim depuis trop longtemps, il meurt
        if self.starvation_chronos >= self.starvation_time:
            self.grid.set(self.x, self.y, 0)  # Le requin disparaît de la grille
            self.grid.sharks = [shark for shark in self.grid.sharks if not (shark.x == self.x and shark.y == self.y)]  # Retire le requin


# Classe représentant la grille de la simulation
class Grid:
    def __init__(self, size):
        """
        Initialise une grille carrée avec une taille spécifiée (nombre de cellules).
        Chaque cellule de la grille est initialement vide (valeur 0).
        """
        self.size = size
        self.cell_size = 20  # Taille de chaque cellule en pixels
        self.grid = [[0 for x in range(size)] for y in range(size)]

        # Changer les paramètres pour modifier le nombre de poissons et de requins
        self.fishes = [Fish(rd.randint(0, self.size - 1), rd.randint(0, self.size - 1), self, 3) for _ in range(70)]
        self.sharks = [Shark(rd.randint(0, self.size - 1), rd.randint(0, self.size - 1), self, 18, 5) for _ in range(20)]


    def set(self, x, y, value):
        """
        Modifie la valeur d'une cellule de la grille à la position (x, y).
        """
        self.grid[y][x] = value

    def get(self, x, y):
        """
        Récupère la valeur de la cellule à la position (x, y).
        """
        return self.grid[y][x]

    def draw(self, screen, offset_x, offset_y):
        """
        Dessine la grille sur l'écran avec des lignes blanches entre chaque cellule.
        Les cellules avec la valeur 1 sont des poissons (blancs) et 2 sont des requins (rouges).
        L'offset_x et l'offset_y sont utilisés pour positionner la grille sur l'écran.
        """
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(offset_x + x * self.cell_size, offset_y + y * self.cell_size, self.cell_size, self.cell_size)
                if self.grid[y][x] == 1:  # Poisson
                    pygame.draw.rect(screen, (0, 255, 255), rect)
                elif self.grid[y][x] == 2:  # Requin
                    pygame.draw.rect(screen, (255, 0, 0), rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Dessine les lignes blanches


# Classe principale de l'application pygame
class App:
    def __init__(self):
        """
        Initialise l'application avec des paramètres supplémentaires pour la simulation Wa-Tor.
        """
        self.start_time = dt.now()
        self.final_time = None
        self.turn = 0
        self._running = True
        self._display_surf = None
        self.window_width = 900
        self.window_height = 600
        self.grid_size = 24
        self.grid = Grid(self.grid_size)  # Création de la grille
        self.grid_display_size = 600  # Taille d'affichage de la grille

    def on_loop(self):
        """
        Boucle principale de l'application, gérant le mouvement et la reproduction des poissons et des requins.
        """
        self.turn += 1
        if self.turn % 150 == 0:
            for fish in self.grid.fishes:
                fish.move()  # Déplace chaque poisson
            for shark in self.grid.sharks:
                shark.move() # Déplace chaque requin

    def on_init(self):
        """
        Initialise Pygame et la fenêtre de l'application.
        """
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.font = pygame.font.SysFont('Arial', 24)
 
    def on_event(self, event):
        """
        Gère les événements, en particulier la fermeture de la fenêtre.
        """
        if event.type == pygame.QUIT:
            self._running = False

    def on_render(self):
        """
        Met à jour l'affichage de la fenêtre et dessine la grille.
        """
        self._display_surf.fill((55, 55, 55))  # Remplissage de l'arrière-plan
        self.grid.draw(self._display_surf, 20, 40)  # Un petit offset pour l'ajuster dans la fenêtre

        # Affichage du temps écoulé
        elapsed_time = dt.now() - self.start_time
        # Format le temps écoulé en heures, minutes et secondes
        elapsed_time = f"{elapsed_time.seconds // 3600}h {elapsed_time.seconds % 3600 // 60}m {elapsed_time.seconds % 60}s"
        elapsed_text = self.font.render(f"Temps écoulé: {elapsed_time}", True, (255, 255, 255))
        self._display_surf.blit(elapsed_text, (550, 150))
        
        # Affichage des statistiques sur les poissons
        fish_count = len(self.grid.fishes)
        fish_text = self.font.render(f"Poissons: {fish_count}", True, (255, 255, 255))
        self._display_surf.blit(fish_text, (550, 200))  # Position à droite

        # Affichage des statistiques sur les requins
        shark_count = len(self.grid.sharks)
        shark_text = self.font.render(f"Requins: {shark_count}", True, (255, 255, 255))
        self._display_surf.blit(shark_text, (550, 250))

        # Si tous les poissons ou requins sont morts, affiche le temps final et arrête la simulation
        if (fish_count == 0 or shark_count == 0) and self.final_time is None:
            self.final_time = dt.now() - self.start_time
            self.final_time = f"{self.final_time.seconds // 3600}h {self.final_time.seconds % 3600 // 60}m {self.final_time.seconds % 60}s"
        if self.final_time is not None:
            final_text = self.font.render(f"Temps final: {self.final_time}", True, (255, 255, 255))
            self._display_surf.blit(final_text, (550, 400))
        
        pygame.display.flip()  # Met à jour l'affichage

    def on_cleanup(self):
        """
        Nettoie les ressources et quitte l'application.
        """
        pygame.quit()
 
    def on_execute(self):
        """
        Démarre l'exécution de l'application.
        """
        if self.on_init() == False:
            self._running = False
 
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


# Boucle d'exécution principale
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
