import random as rd
from datetime import datetime as dt

import pygame
from pygame.locals import *


# Classe représentant un poisson dans la grille
class Fish:
    def __init__(self, x, y, grid, reproduction_time):
        """
        Initialise un poisson dans la grille à une position donnée (x, y).
        Le poisson a un temps de reproduction donné.
        
        x, y : Position du poisson dans la grille.
        grid : La grille sur laquelle le poisson évolue.
        reproduction_time : Le nombre de tours avant que le poisson puisse se reproduire.
        """
        self.chronos = 0  # Chronomètre pour suivre le temps écoulé depuis la dernière reproduction
        self.reproduction_time = reproduction_time  # Temps nécessaire avant reproduction
        self.x = x  # Position x du poisson
        self.y = y  # Position y du poisson
        self.grid = grid  # Référence à la grille
        self.grid.set(self.x, self.y, 1)  # Indique dans la grille que cette position contient un poisson (1)

    def move(self):
        """
        Déplace le poisson de manière aléatoire dans la grille et gère la reproduction.
        Le déplacement est torique : si le poisson dépasse la bordure, il réapparaît de l'autre côté.
        Si le temps de reproduction est atteint, un nouveau poisson est créé à l'ancienne position.
        """
        self.chronos += 1  # Incrémenter le compteur de chronos
        # Choisir une direction aléatoire : (0, 1) bas, (0, -1) haut, (1, 0) droite, (-1, 0) gauche
        direction = rd.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        # Calculer la nouvelle position (avec effet tore)
        new_x = (self.x + direction[0]) % self.grid.size
        new_y = (self.y + direction[1]) % self.grid.size

        if self.grid.get(new_x, new_y) == 0:  # Vérifier si la nouvelle case est vide
            if self.chronos >= self.reproduction_time:  # Si le temps de reproduction est atteint
                self.chronos = 0  # Réinitialiser le chronos
                # Créer un nouveau poisson à l'ancienne position
                new_fish = Fish(self.x, self.y, self.grid, self.reproduction_time)
                self.grid.fishes.append(new_fish)  # Ajouter le nouveau poisson à la liste des poissons
            else:
                # Sinon, libérer l'ancienne position (en mettant 0)
                self.grid.set(self.x, self.y, 0)

            # Mettre à jour la position du poisson
            self.x, self.y = new_x, new_y
            self.grid.set(self.x, self.y, 1)  # Mettre à jour la nouvelle position dans la grille

# Classe représentant un requin, hérite des caractéristiques de Fish
class Shark(Fish):
    def __init__(self, x, y, grid, reproduction_time, starvation_time):
        """
        Initialise un requin à la position (x, y) dans la grille.
        Le requin peut mourir de faim s'il ne mange pas de poisson après un certain temps.

        x, y : Position du requin dans la grille.
        grid : La grille sur laquelle le requin évolue.
        reproduction_time : Le nombre de tours avant la reproduction.
        starvation_time : Le nombre de tours avant que le requin meure de faim.
        """
        super().__init__(x, y, grid, reproduction_time)  # Appeler le constructeur de Fish pour initialiser les attributs communs
        self.starvation_time = starvation_time  # Temps avant que le requin ne meure de faim
        self.starvation_chronos = 0  # Chronomètre pour suivre le temps depuis le dernier repas
        self.grid.set(self.x, self.y, 2)  # Indique dans la grille que cette position contient un requin (2)

    def move(self):
        """
        Déplace le requin de manière aléatoire et lui permet de manger les poissons à proximité.
        Gère la reproduction et la mort par faim.
        """
        self.chronos += 1  # Incrémenter le chronomètre pour la reproduction
        self.starvation_chronos += 1  # Incrémenter le chronomètre pour la famine

        # Directions possibles pour se déplacer : haut, bas, droite, gauche
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        possible_moves = []

        # Chercher des poissons à proximité
        for direction in directions:
            new_x = (self.x + direction[0]) % self.grid.size
            new_y = (self.y + direction[1]) % self.grid.size
            if self.grid.get(new_x, new_y) == 1:  # S'il y a un poisson
                possible_moves.append((new_x, new_y))  # Ajouter cette case à la liste des mouvements possibles

        if possible_moves:  # Si des poissons sont trouvés
            # Choisir un poisson à manger
            new_x, new_y = rd.choice(possible_moves)
            self.grid.set(new_x, new_y, 0)  # Supprimer le poisson de la grille
            # Supprimer le poisson mangé de la liste des poissons
            self.grid.fishes = [fish for fish in self.grid.fishes if not (fish.x == new_x and fish.y == new_y)]
            self.starvation_chronos = 0  # Réinitialiser le chronomètre de famine après avoir mangé
        else:
            # Sinon, se déplacer de manière aléatoire
            direction = rd.choice(directions)
            new_x = (self.x + direction[0]) % self.grid.size
            new_y = (self.y + direction[1]) % self.grid.size

        if self.grid.get(new_x, new_y) == 0:  # Si la nouvelle position est vide
            if self.chronos >= self.reproduction_time:  # Si le temps de reproduction est atteint
                self.chronos = 0  # Réinitialiser le chronos
                # Créer un nouveau requin à l'ancienne position
                new_shark = Shark(self.x, self.y, self.grid, self.reproduction_time, self.starvation_time)
                self.grid.sharks.append(new_shark)  # Ajouter le nouveau requin à la liste
            else:
                self.grid.set(self.x, self.y, 0)  # Libérer l'ancienne position

            # Mettre à jour la position du requin
            self.x, self.y = new_x, new_y
            self.grid.set(self.x, self.y, 2)  # Mettre à jour la nouvelle position dans la grille

        # Si le requin n'a pas mangé depuis trop longtemps, il meurt
        if self.starvation_chronos >= self.starvation_time:
            self.grid.set(self.x, self.y, 0)  # Le requin disparaît de la grille
            # Supprimer le requin mort de la liste des requins
            self.grid.sharks = [shark for shark in self.grid.sharks if not (shark.x == self.x and shark.y == self.y)]


# Classe représentant la grille de la simulation
class Grid:
    def __init__(self, size):
        """
        Initialise une grille carrée de la taille spécifiée.
        Chaque case de la grille peut contenir un poisson, un requin ou être vide (valeur 0).

        size : Taille de la grille (nombre de cellules de chaque côté).
        """
        self.size = size  # Taille de la grille (ex : 24x24)
        self.cell_size = 20  # Taille visuelle de chaque cellule en pixels
        # Initialiser la grille avec des cases vides (toutes à 0)
        self.grid = [[0 for x in range(size)] for y in range(size)]

        # Créer 70 poissons et les placer aléatoirement sur la grille
        self.fishes = [Fish(rd.randint(0, self.size - 1), rd.randint(0, self.size - 1), self, 3) for _ in range(70)]
        # Créer 20 requins et les placer aléatoirement sur la grille
        self.sharks = [Shark(rd.randint(0, self.size - 1), rd.randint(0, self.size - 1), self, 18, 5) for _ in range(20)]

    def set(self, x, y, value):
        """
        Met à jour la valeur d'une cellule dans la grille à la position (x, y).
        value : 0 pour vide, 1 pour poisson, 2 pour requin.
        """
        self.grid[y][x] = value

    def get(self, x, y):
        """
        Récupère la valeur d'une cellule dans la grille à la position (x, y).
        """
        return self.grid[y][x]

    def draw(self, screen, offset_x, offset_y):
        """
        Dessine la grille sur l'écran avec des cellules représentant les poissons, les requins et les cases vides.
        screen : L'écran pygame sur lequel dessiner.
        offset_x, offset_y : Position du coin supérieur gauche de la grille à l'écran.
        """
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(offset_x + x * self.cell_size, offset_y + y * self.cell_size, self.cell_size, self.cell_size)
                if self.grid[y][x] == 1:  # Si un poisson est présent
                    pygame.draw.rect(screen, (0, 255, 255), rect)  # Dessiner le poisson en cyan
                elif self.grid[y][x] == 2:  # Si un requin est présent
                    pygame.draw.rect(screen, (255, 0, 0), rect)  # Dessiner le requin en rouge
                pygame.draw.rect(screen, (150, 150, 150), rect, 1)  # Dessiner les lignes blanches de la grille


# Classe principale de l'application pygame
class App:
    def __init__(self):
        """
        Initialise l'application de simulation Wa-Tor avec une grille et une interface graphique.
        """
        self.start_time = dt.now()  # Enregistre le temps de départ de la simulation
        self.final_time = None  # Temps final de la simulation, s'il est nécessaire d'afficher
        self.turn = 0  # Nombre de tours effectués dans la simulation
        self._running = True  # Flag indiquant si l'application est en cours d'exécution
        self._display_surf = None  # Surface d'affichage Pygame
        self.window_width = 900  # Largeur de la fenêtre Pygame
        self.window_height = 600  # Hauteur de la fenêtre Pygame
        self.grid_size = 24  # Taille de la grille (24x24)
        self.grid = Grid(self.grid_size)  # Créer la grille
        self.grid_display_size = 600  # Taille visuelle de la grille à l'écran
        self.on_init()  # Initialisation de l'application

    def on_loop(self):
        """
        Boucle principale de la simulation : gère le mouvement des poissons et des requins.
        """
        self.turn += 1  # Incrémenter le nombre de tours
        # Toutes les 150 itérations, déplacer les poissons et les requins
        if self.turn % 150 == 0:
            for fish in self.grid.fishes:
                fish.move()  # Déplacer chaque poisson
            for shark in self.grid.sharks:
                shark.move()  # Déplacer chaque requin

    def on_init(self):
        """
        Initialise Pygame et les paramètres d'affichage.
        """
        pygame.init()  # Initialiser les modules Pygame
        # Créer une fenêtre de taille spécifiée
        self._display_surf = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True  # Démarre l'application
        self.font = pygame.font.SysFont('Arial', 24)  # Charger une police de texte
        self.on_execute()

    def on_event(self, event):
        """
        Gère les événements utilisateurs (comme fermer la fenêtre).
        """
        if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
            self._running = False  # Arrêter l'application

    def on_render(self):
        """
        Met à jour l'affichage à chaque tour de la simulation.
        """
        self._display_surf.fill((55, 55, 55))  # Remplir l'arrière-plan en gris foncé
        # Dessiner la grille à la position (20, 40) dans la fenêtre
        self.grid.draw(self._display_surf, 20, 40)

        # Calculer et afficher le temps écoulé
        elapsed_time = dt.now() - self.start_time
        elapsed_time = f"{elapsed_time.seconds // 3600}h {elapsed_time.seconds % 3600 // 60}m {elapsed_time.seconds % 60}s"
        elapsed_text = self.font.render(f"Temps écoulé: {elapsed_time}", True, (255, 255, 255))
        self._display_surf.blit(elapsed_text, (550, 150))

        # Afficher le nombre de poissons restant
        fish_count = len(self.grid.fishes)
        fish_text = self.font.render(f"Poissons: {fish_count}", True, (255, 255, 255))
        self._display_surf.blit(fish_text, (550, 200))

        # Afficher le nombre de requins restant
        shark_count = len(self.grid.sharks)
        shark_text = self.font.render(f"Requins: {shark_count}", True, (255, 255, 255))
        self._display_surf.blit(shark_text, (550, 250))

        # Si tous les poissons ou requins sont morts, afficher le temps final
        if (fish_count == 0 or shark_count == 0) and self.final_time is None:
            self.final_time = dt.now() - self.start_time
            self.final_time = f"{self.final_time.seconds // 3600}h {self.final_time.seconds % 3600 // 60}m {self.final_time.seconds % 60}s"
        if self.final_time is not None:
            final_text = self.font.render(f"Temps final: {self.final_time}", True, (255, 255, 255))
            self._display_surf.blit(final_text, (550, 400))

        pygame.display.flip()  # Mettre à jour l'affichage

    def on_cleanup(self):
        """
        Nettoie et ferme l'application.
        """
        pygame.quit()

    def on_execute(self):
        """
        Démarre l'exécution de l'application (boucle principale).
        """
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)  # Gérer les événements
            self.on_loop()  # Boucle de simulation
            self.on_render()  # Mise à jour de l'affichage
        self.on_cleanup()  # Nettoyage à la fin

# Boucle d'exécution principale
if __name__ == "__main__" :
    App()
