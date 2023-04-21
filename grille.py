import random
from queue import PriorityQueue

class Node:
    def __init__(self, x, y, g_cost, h_cost):
        self.x = x
        self.y = y
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost

def heuristic(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

class Grille:
    def __init__(self, largeur, hauteur, densite_caisse=0.3, woodbox_count=1, caisse_ok_count=1,grass_count=20):
        self.largeur = largeur
        self.hauteur = hauteur
        self.densite_caisse = densite_caisse
        self.woodbox_count = woodbox_count
        self.caisse_ok_count = caisse_ok_count
        self.grass_count = grass_count
        self.contenu = self.creer_contenu()
        
    def est_solvable(self, personnage_x, personnage_y, sortie_x, sortie_y):
        hauteur = len(self.contenu)
        largeur = len(self.contenu[0])

        open_set = PriorityQueue()
        start_node = Node(personnage_x, personnage_y, 0, heuristic(personnage_x, personnage_y, sortie_x, sortie_y))
        open_set.put(start_node)
        came_from = {(personnage_x, personnage_y): start_node}

        while not open_set.empty():
            current = open_set.get()
            if current.x == sortie_x and current.y == sortie_y:
                return True

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x = current.x + dx
                y = current.y + dy

                if 0 <= x < largeur and 0 <= y < hauteur and self.contenu[y][x] != '#':
                    new_g_cost = current.g_cost + 1
                    if (x, y) not in came_from or new_g_cost < came_from[(x, y)].g_cost:
                        came_from[(x, y)] = current
                        h_cost = heuristic(x, y, sortie_x, sortie_y)
                        open_set.put(Node(x, y, new_g_cost, h_cost))

        return False


    def est_coin(self, contenu, x, y):
        haut_gauche = (contenu[y - 1][x] == '#' and contenu[y][x - 1] == '#')
        haut_droite = (contenu[y - 1][x] == '#' and contenu[y][x + 1] == '#')
        bas_gauche = (contenu[y + 1][x] == '#' and contenu[y][x - 1] == '#')
        bas_droite = (contenu[y + 1][x] == '#' and contenu[y][x + 1] == '#')

        return haut_gauche or haut_droite or bas_gauche or bas_droite
    
    def creer_contenu(self):
        while True:
            contenu = []
            for i in range(self.hauteur):
                ligne = []
                for j in range(self.largeur):
                    if i == 0 or i == self.hauteur - 1 or j == 0 or j == self.largeur - 1:
                        ligne.append('#')
                    else:
                        ligne.append('.')
                contenu.append(ligne)

        # Place the character
            while True:
                personnage_x = random.randint(1, self.largeur - 2)
                personnage_y = random.randint(1, self.hauteur - 2)
                if contenu[personnage_y][personnage_x] == '.':
                    contenu[personnage_y][personnage_x] = '@'
                    break

        # Add woodboxes
            for _ in range(self.woodbox_count):
                while True:
                    x = random.randint(1, self.largeur - 2)
                    y = random.randint(1, self.hauteur - 2)
                    if contenu[y][x] == '.':
                        contenu[y][x] = '$'
                        break
        # Add grass obstacles
            for _ in range(self.grass_count):
                while True:
                    x = random.randint(1, self.largeur - 2)
                    y = random.randint(1, self.hauteur - 2)
                    if contenu[y][x] == '.':
                        contenu[y][x] = 'G'
                        break
    

        # Add caisse_ok targets
            for _ in range(self.caisse_ok_count):
                while True:
                    sortie_x = random.randint(1, self.largeur - 2)
                    sortie_y = random.randint(1, self.hauteur - 2)
                    if contenu[sortie_y][sortie_x] == '.':
                        contenu[sortie_y][sortie_x] = '*'
                        break

            self.contenu = contenu
            if self.est_solvable(personnage_x, personnage_y, sortie_x, sortie_y):
                break

        return contenu


    def est_caisse_ok(self, x, y):
        return self.contenu[y][x] == '*'

    def est_mur(self, x, y):
        if self.contenu[y][x] == '#':
            return True
        else:
            return False

    def est_case(self, x, y):
        if self.contenu[y][x] == '.':
            return True
        else:
            return False

    def est_caisse(self, x, y):
        if self.contenu[y][x] == '$':
            return True
        else:
            return False

    def deplacer_caisse(self, x, y, dx, dy):
        new_x, new_y = x + dx, y + dy
        if self.est_case(new_x, new_y):
            self.contenu[new_y][new_x] = '$'
            self.contenu[y][x] = '.'
        elif self.est_caisse_ok(new_x, new_y):
            self.contenu[new_y][new_x] = '*'
            self.contenu[y][x] = '.'

    def get_position_personnage(self):
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if self.contenu[y][x] == '@':
                    return (x, y)
        return None

    # vérifier si toutes les caisses sont sur des cases cibles
    def toutes_caisses_ok(self):
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if self.contenu[y][x] == '$':
                    return False
        return True

    def est_grass(self, x, y):
        if self.contenu[y][x] == 'G':
            return True
        else:
            return False