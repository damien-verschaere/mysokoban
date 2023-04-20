class Personnage:
    def __init__(self, x, y, image, grille):
        self.x = x
        self.y = y
        self.image = image
        self.grille = grille

    def deplacer(self, direction):
        dx, dy = 0, 0
        if direction == 'gauche':
            dx = -1
        elif direction == 'droite':
            dx = 1
        elif direction == 'haut':
            dy = -1
        elif direction == 'bas':
            dy = 1

        new_x, new_y = self.x + dx, self.y + dy
        if self.grille.est_case(new_x, new_y) or self.grille.est_caisse_ok(new_x, new_y):
            self.x, self.y = new_x, new_y
        elif self.grille.est_caisse(new_x, new_y):
            new_caisse_x, new_caisse_y = new_x + dx, new_y + dy
            if self.grille.est_case(new_caisse_x, new_caisse_y):
                self.grille.deplacer_caisse(new_x, new_y, dx, dy)
                self.x, self.y = new_x, new_y
            elif self.grille.est_caisse_ok(new_caisse_x, new_caisse_y):
                self.grille.deplacer_caisse(new_x, new_y, dx, dy)
                self.grille.contenu[new_y][new_x] = '.'
                self.x, self.y = new_x, new_y

    def afficher(self, fenetre, taille_case, marge_x, marge_y):
        fenetre.blit(self.image, (marge_x + self.x*taille_case, marge_y + self.y*taille_case))
