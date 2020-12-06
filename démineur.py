
# BOUKHELIFA ALI
# Université Paris 8
# Janvier 2019


import numpy as np
import pygame


class Table(object):
    """Table sous-jacente du Démineur"""
    def __init__(self, size, num_bomb):
        self.size = size
        # Table sous-jacente du Démineur
        self.grid = np.zeros((size, size))

        # Table de visibilité du Démineur
        # 2: flagged, 1: not visible, 0: visible
        self.visibility = np.ones((size, size))
        self.visited = []

        self.add_bombs(num_bomb)
        self.compute_adjacency()

    def add_bombs(self, num_bomb):
        """ajoute les bombes dans la grille"""

        # vérifie que les positions sont unique
        while True:
            # supprime les duplicata
            pos = set(tuple(np.random.randint(low=0, high=self.size, size=2)) for _ in range(num_bomb))

            if len(pos) == num_bomb:
                break

        for x, y in pos:
            self.grid[x][y] = 9

    def compute_adjacency(self):
        """met a jour les valeurS des caseS selon le nombre de bombe adjacente"""

        # valeur relative des caseS adjacenteS
        adj = [-1, 0, 1]

        def bound(i): return min(max(i, 0), self.size-1)

        # parcourir la grille
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x, y] != 9:

                    visited = []
                    # voisin de notre case
                    for i in adj:
                        for j in adj:
                            u, v = self.bound(x+i), self.bound(y+j)

                            if self.grid[u, v] == 9 and (u, v) not in visited:
                                visited.append((u, v))

                                # mise a jour de la case concerné
                                self.grid[x, y] += 1

    def uncover(self, x, y):
        """Découvre une case et si elle est nulle découvre les cases nulle adjacente"""
        self.visibility[x, y] = 0

        if self.grid[x, y] == 0:
            # liste des cases vides deja visitées
            self.visited.append((x, y))

            # voisin de notre case
            adj = [(0, 1), (1, 0), (-1, 0), (0, -1)]

            for i, j in adj:
                u, v = self.bound(x+i), self.bound(y+j)

                if self.grid[u, v] == 0 and (u, v) not in self.visited:
                    self.uncover(u, v)

    def bound(self, i):
        return min(max(i, 0), self.size-1)


def game(size, bombs):

    # intialise pygame
    pygame.init()

    # nom des images a importer
    img = ["grey", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "flag"]

    # importation des images
    images = {i: pygame.image.load(i+".jpg") for i in img}

    # créer la grille
    table = Table(size, bombs)

    # création de la fenetre
    screen = pygame.display.set_mode((size * 40, size * 40))
    pygame.display.set_caption('Ali Démineur')

    end_game = False

    # logique du jeu
    while True:

        # updating the display
        for x in range(size):
            for y in range(size):
                # si la case n'est pas visible
                if table.visibility[x, y] == 1:
                    screen.blit(images["grey"], (x * 40, y * 40))

                # si elle est flaguée
                elif table.visibility[x, y] == 2:
                    screen.blit(images["flag"], (x * 40, y * 40))

                else:
                    value = int(table.grid[x, y])
                    screen.blit(images[str(value)], (x * 40, y * 40))

        for event in pygame.event.get():

            # clique sur exit
            if event.type == pygame.QUIT:
                pygame.quit()

            # clique sur R
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.quit()
                    # réinitialise
                    table.visited = []

                    # lance un nouveau jeu
                    game(size, bombs)

            # clique de souris gauche
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not end_game:
                # retrouve la position du clique
                position = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))

                # détermine la case cliquée
                x, y = [i // 40 for i in position[:2]]

                # si elle flagué, attendre l'evenement suivant
                if table.visibility[x, y] == 2:
                    break

                if table.grid[x, y] == 9:
                    end_game = True
                    table.visibility[x, y] = 0

                    # afficher les autre bombe
                    for i in range(size):
                        for j in range(size):
                            if table.grid[i, j] == 9:
                                table.uncover(i, j)

                    print("Game Over")

                else:
                    table.uncover(x, y)

            # clique de souris gauche
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not end_game:
                # retrouve la position du clique
                position = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))

                # détermine la case cliquée
                x, y = [i // 40 for i in position[:2]]

                if table.visibility[x, y] == 1:
                    table.visibility[x, y] = 2

                elif table.visibility[x, y] == 2:
                    table.visibility[x, y] = 1

            num = 0
            for x in range(size):
                for y in range(size):
                    if table.visibility[x, y] == 1:
                        num += 1
            if num == bombs:
                print("You win")

                # afficher les autre bombe
                for x in range(size):
                    for y in range(size):
                        if table.grid[x, y] == 9:
                            table.uncover(x, y)

                end_game = True

        pygame.display.update()


if __name__ == '__main__':
    
    print("Appuyer sur 'R' pour rejouer")
    print("Vous allez choisir la taille de votre table. Elle sera égale à n * n")
    size = int(input("Entrer une valeur pour n: "))
    bombs = (size * size) // 7
    game(size, bombs)
