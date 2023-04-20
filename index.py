import pygame
import pygame.mixer
from grille import Grille
from personnage import Personnage

def init_level(level):
    woodbox_count = level  # Augmenter le nombre de woodboxes en fonction du niveau
    grille = Grille(largeur_grille, hauteur_grille, woodbox_count=woodbox_count)
    initial_position = grille.get_position_personnage()
    personnage = Personnage(initial_position[0], initial_position[1], image_personnage, grille)
    return grille, personnage


# Charger les images
image_mur = pygame.image.load('mur.png')
image_case = pygame.image.load('case.png')
image_caisse = pygame.image.load('woodbox.png')
image_caisse_ok = pygame.image.load('teleport.png')
image_personnage = pygame.image.load('personnage.png')

# Initialiser Pygame
pygame.init()
pygame.mixer.init()

# Définir les dimensions de la fenêtre du jeu
largeur_fenetre = 640
hauteur_fenetre = 480
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.mixer.music.load('jammin.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5) 

# Générer une grille de jeu aléatoire
largeur_grille = 20
hauteur_grille = 15

# Initialiser le niveau
level = 1
grille, personnage = init_level(level)

# Définir la taille de chaque case
taille_case = min(largeur_fenetre // largeur_grille, hauteur_fenetre // hauteur_grille)

# Définir les dimensions de la grille de jeu
grille_largeur = taille_case * largeur_grille
grille_hauteur = taille_case * hauteur_grille

# Centrer la grille de jeu dans la fenêtre
marge_x = (largeur_fenetre - grille_largeur) // 2
marge_y = (hauteur_fenetre - grille_hauteur) // 2

# Ajouter un message de victoire
font = pygame.font.Font(None, 36)
victory_text = font.render("Vous avez gagné !", True, (255, 255, 255))

# Boucle principale du jeu
while True:
    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                personnage.deplacer('gauche')
            elif event.key == pygame.K_RIGHT:
                personnage.deplacer('droite')
            elif event.key == pygame.K_UP:
                personnage.deplacer('haut')
            elif event.key == pygame.K_DOWN:
                personnage.deplacer('bas')
            elif event.key == pygame.K_r:  # Ajout de la touche 'r' pour reset
                grille, personnage = init_level(level)  # Réinitialiser le niveau

        # Dessiner la grille de jeu
    for x in range(largeur_grille):
        for y in range(hauteur_grille):
            if grille.est_mur(x, y):
                fenetre.blit(image_mur, (marge_x + x * taille_case, marge_y + y * taille_case))
            elif grille.est_case(x, y):
                fenetre.blit(image_case, (marge_x + x * taille_case, marge_y + y * taille_case))
            elif grille.est_caisse(x, y):
                fenetre.blit(image_caisse, (marge_x + x * taille_case, marge_y + y * taille_case))
            elif grille.est_caisse_ok(x, y):
                fenetre.blit(image_caisse_ok, (marge_x + x * taille_case, marge_y + y * taille_case))

    # Afficher le personnage
    personnage.afficher(fenetre, taille_case, marge_x, marge_y)

    # Vérifier si toutes les caisses sont sur des cases cibles
    if grille.toutes_caisses_ok():
        # Afficher le message de victoire
        fenetre.blit(victory_text, (largeur_fenetre // 2 - victory_text.get_width() // 2,
                                    hauteur_fenetre // 2 - victory_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(3000)  # Attendre 3 secondes avant de passer au niveau suivant

        # Initialiser le niveau suivant
        level += 1
        grille, personnage = init_level(level)

    # Rafraîchir l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
pygame.mixer.music.stop()
