import pygame
import pygame.mixer

from grille import Grille
from personnage import Personnage
from score import Score



def init_level(level):
    woodbox_count = level  # Augmenter le nombre de woodboxes en fonction du niveau
    grille = Grille(largeur_grille, hauteur_grille, woodbox_count=woodbox_count)
    initial_position = grille.get_position_personnage()
    personnage = Personnage(initial_position[0], initial_position[1], image_personnage, grille)
    return grille, personnage

# Fonction pour obtenir le nom du joueur
def get_player_name():
    pygame.init()
    input_box = pygame.Rect(200, 200, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)
    screen = pygame.display.set_mode((640, 480))
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        welcome_text = font.render("Entrez votre nom:", True, (255, 255, 255))
        screen.blit(welcome_text, (200, 150))

        pygame.display.flip()

    return text


# def sauvegarder_score_db(player_name, level, score):
#     db = MySQLConnector(host="localhost", user="root", password="password", database="mydatabase")
#     db.connect()
#     query = f"INSERT INTO scores (player_name, level, score) VALUES ('{player_name}', {level}, {score})"
#     db.execute_query(query)


# Demander le nom du joueur
player_name = get_player_name()

# Charger les images
image_mur = pygame.image.load('mur.png')
image_case = pygame.image.load('case.png')
image_caisse = pygame.image.load('woodbox.png')
image_caisse_ok = pygame.image.load('teleport.png')
image_personnage = pygame.image.load('personnage.png')
image_grass = pygame.image.load('grass.png')

# Initialiser Pygame
pygame.init()
pygame.mixer.init()

# Créer l'objet Score
score_obj = Score()

# Définir les dimensions de la fenêtre du jeu
largeur_fenetre = 900
hauteur_fenetre = 480
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.mixer.music.load('ff7.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2) 

def display_player_info(fenetre, font, player_name, level, score):
    fenetre.fill((0, 0, 0), (700, 30, 200, 100))
    # Afficher le nouveau score
    info_text = f"Joueur: {player_name}\nNiveau: {level}"
    score_text = f"Score: {score}"
    info_lines = info_text.split('\n')
    line_height = font.get_linesize()
    for i, line in enumerate(info_lines):
        info_surface = font.render(line, True, (255, 255, 255))
        fenetre.blit(info_surface, (700, 30 + i * line_height))
    # Afficher le nouveau score
    score_surface = font.render(score_text, True, (255, 255, 255))
    fenetre.blit(score_surface, (700, 60 + len(info_lines) * line_height))
    
    # Ajouter les commandes
    commandes_text = "R : Reset"
    commandes_surface = font.render(commandes_text, True, (255,255,255))
    fenetre.blit(commandes_surface, (700, 200))




def afficher_ecran_accueil(fenetre, font):
    fenetre.fill((0, 0, 0))
    texte_titre = font.render("Bienvenue dans le jeu", True, (255, 255, 255))
    texte_jouer = font.render("Cliquez pour jouer", True, (255, 255, 255))
    fenetre.blit(texte_titre, (largeur_fenetre // 2 - texte_titre.get_width() // 2, hauteur_fenetre // 3))
    fenetre.blit(texte_jouer, (largeur_fenetre // 2 - texte_jouer.get_width() // 2, hauteur_fenetre // 2))
    pygame.display.flip()

def attendre_clic_jouer():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

font = pygame.font.Font(None, 36)
afficher_ecran_accueil(fenetre, font)
attendre_clic_jouer()

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
marge_x = 0
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
            elif grille.est_grass(x, y):
                fenetre.blit(image_grass, (marge_x + x * taille_case, marge_y + y * taille_case))
            else:
                fenetre.blit(image_grass, (marge_x + x * taille_case, marge_y + y * taille_case))


    # Afficher le personnage
    personnage.afficher(fenetre, taille_case, marge_x, marge_y)

    # Vérifier si toutes les caisses sont sur des cases cibles
    if grille.toutes_caisses_ok():
        # Augmenter le score
        pygame.mixer.music.pause()
        score_obj.increase_score(100) 
        musique_victoire = pygame.mixer.Sound('victoire.ogg')
        # pygame.mixer.music.load('victoire.ogg')
        musique_victoire.play()
        
        # Afficher le message de victoire
        fenetre.blit(victory_text, (largeur_fenetre // 2 - victory_text.get_width() // 2,
                                    hauteur_fenetre // 2 - victory_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(6000)  
        musique_victoire.stop()
        pygame.mixer.music.unpause()
        # Initialiser le niveau suivant
        level += 1
        grille, personnage = init_level(level)

    display_player_info(fenetre, font, player_name, level, score_obj.get_score())

    # Rafraîchir l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
pygame.mixer.music.stop()

