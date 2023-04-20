import random

class Grille:
    def __init__(self, largeur, hauteur, densite_caisse=0.3, woodbox_count=1, caisse_ok_count=1):
        self.largeur = largeur
        self.hauteur = hauteur
        self.densite_caisse = densite_caisse
        self.woodbox_count = woodbox_count
        self.caisse_ok_count = caisse_ok_count
        self.contenu = self.creer_contenu()
        
    def est_solvable(self, contenu, personnage_x, personnage_y):
        def dfs(x, y, visited):
            if x < 0 or x >= self.largeur or y < 0 or y >= self.hauteur or visited[y][x] or contenu[y][x] == '#':
                return False

            visited[y][x] = True

            if contenu[y][x] == '$':
                if self.est_coin(contenu, x, y):
                    return False
                else:
                    return True

            if dfs(x - 1, y, visited) or dfs(x + 1, y, visited) or dfs(x, y - 1, visited) or dfs(x, y + 1, visited):
                return True

            return False

        visited = [[False for _ in range(self.largeur)] for _ in range(self.hauteur)]

        return dfs(personnage_x, personnage_y, visited)

    def est_coin(self, contenu, x, y):
        haut_gauche = (contenu[y - 1][x] == '#' and contenu[y][x - 1] == '#')
        haut_droite = (contenu[y - 1][x] == '#' and contenu[y][x + 1] == '#')
        bas_gauche = (contenu[y + 1][x] == '#' and contenu[y][x - 1] == '#')
        bas_droite = (contenu[y + 1][x] == '#' and contenu[y][x + 1] == '#')

        return haut_gauche or haut_droite or bas_gauche or bas_droite
    
    
    def creer_contenu(self):
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
            x = random.randint(1, self.largeur - 2)
            y = random.randint(1, self.hauteur - 2)
            if contenu[y][x] == '.':
                contenu[y][x] = '@'
                break

    # Add woodboxes
        for _ in range(self.woodbox_count):
            while True:
                x = random.randint(1, self.largeur - 2)
                y = random.randint(1, self.hauteur - 2)
                if contenu[y][x] == '.':
                    contenu[y][x] = '$'
                    break

    # Add caisse_ok targets
        for _ in range(self.caisse_ok_count):
            while True:
                x = random.randint(1, self.largeur - 2)
                y = random.randint(1, self.hauteur - 2)
                if contenu[y][x] == '.':
                    contenu[y][x] = '*'
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

    # Ajouter une méthode pour vérifier si toutes les caisses sont sur des cases cibles
    def toutes_caisses_ok(self):
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if self.contenu[y][x] == '$':
                    return False
        return True
