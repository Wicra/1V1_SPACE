import pygame
import sys
import random

#creation de l'animation 
class AnimateSprite1(pygame.sprite.Sprite):
    def __init__(self, sprite_name):
        super().__init__()
        self.image = pygame.image.load(f'Joueur1/{sprite_name}1.gif')
        self.current_image = 0
        self.images = animations.get(sprite_name)
    
    def animate(self):
        self.current_image += 1
        if self.current_image >= len(self.images):
            self.current_image = 0
        
        self.image = self.images[self.current_image]
        pygame.time.delay(50)  # Ajouter une pause de 100 millisecondes entre chaque image

def load_animation_images(sprite_name):
    images = []
    path = f"Joueur1/{sprite_name}"

    for num in range(1,11):
        image_path = path + str(num) +'.gif'
        images.append(pygame.image.load(image_path))
    return images

animations = {
    'frame':load_animation_images('frame')
}

#creation de l'animation 
class AnimateSprite2(pygame.sprite.Sprite):

    def __init__(self, sprite_nom):
        super().__init__()
        self.image2 = pygame.image.load(f'Joueur2/{sprite_nom}1.gif')
        self.current_image2 = 0
        self.images2 = animations2.get(sprite_nom)
    
    def animate2(self):
        self.current_image2 += 1
        if self.current_image2 >= len(self.images2):
            self.current_image2 = 0
        
        self.image2 = self.images2[self.current_image2]
        pygame.time.delay(50)  # Ajouter une pause de 100 millisecondes entre chaque image

def load_animation_images2(sprite_nom):
    images2 = []
    path2 = f"Joueur2/{sprite_nom}"

    for num in range(1,8):
        image_path2 = path2 + str(num) +'.gif'
        images2.append(pygame.image.load(image_path2))
    return images2

animations2 = {
    'Frame':load_animation_images2('Frame')
}

# Initialisation de Pygame
pygame.init()
Joueur1= AnimateSprite1('frame')
Joueur2= AnimateSprite2('Frame')

#nom de joueur 
nom_joueur1 = ""
nom_joueur2 = ""
horloge = pygame.time.Clock()

# Dimensions de la fenêtre de jeu
largeur = 1300
hauteur = 800

# Couleurs (RGB)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
VIOLET = (148, 0, 211)
ROSE = (245,86,77,96)
BLEU = (43,64,255,100)
OR = (218, 165, 32)

# Dimensions et vitesse des joueurs
joueur_taille = 80
joueur_vitesse_1 = 15
joueur_vitesse_2 = 15
joueur_boost_vitesse = 5

# Barre de vie
vie_largeur = 0  # Largeur de la barre de vie (divisée par 2)
vie_hauteur = 0 # Hauteur de la barre de vie

# Vitesse des balles
balle_vitesse = 120

# Temps d'apparition du boost et de soin
temps_apparition_boost = 10000  # 10 secondes
temps_apparition_soins = 10000  # 10 secondes

# Création de la fenêtre de jeu
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("QWELD ARENA")

# Chargement des images
image_menu = pygame.image.load("Img/menu.png").convert()  # Image de l'écran de menu
image_fond_jeu = pygame.image.load("Img/fond_jeu.jpg").convert()  # Image de fond du jeu
image_soins = pygame.image.load("Img/soins.png").convert()
image_boost = pygame.image.load("Img/boost.png").convert()
image_bal1 =  pygame.image.load("Img/image_bal1.png").convert()
image_bal2 =  pygame.image.load("Img/image_bal2.png").convert()

# Image de fond du jeu
image_menu = pygame.transform.scale(image_menu, (largeur, hauteur))  # Redimensionner l'image du menu
image_fond_jeu = pygame.transform.scale(image_fond_jeu, (largeur, hauteur))  # Redimensionner l'image de fond du jeu
image_soins = pygame.transform.scale(image_soins, (20, 20))
image_boost = pygame.transform.scale(image_boost, (20, 20))
image_bal1 = pygame.transform.scale(image_bal1, (15, 15))
image_bal2 = pygame.transform.scale(image_bal2, (15, 15))

# Charger la police TrueType
font1 = pygame.font.Font("font.ttf", 100)  # Remplacez "chemin/vers/votre/police.ttf" par le chemin absolu ou relatif de votre police et "taille_police" par la taille de police souhaitée
font2 = pygame.font.Font("font.ttf", 30)  
font3 = pygame.font.Font("font.ttf", 20)  

# Position initiale des joueurs
joueur1_x = 50
joueur1_y = hauteur // 2 - joueur_taille // 2
joueur2_x = largeur - 50 - joueur_taille
joueur2_y = hauteur // 2 - joueur_taille // 2

# Vie des joueurs
vie_joueur1 = 100
vie_joueur2 = 100

# defaite
joueur1_perdu = False
joueur2_perdu = False

# Score
score_joueur1 = 0
score_joueur2 = 0

# Boost
boost_x = None
boost_y = None
boost_actif = False
boost_temps = pygame.time.get_ticks()

# Soin
soins_x = None
soins_y = None
soins_actif = False
soins_temps = pygame.time.get_ticks()

# Création de la police de texte
police = pygame.font.SysFont(None, 30)

# Listes des balles
balles_joueur1 = []
balles_joueur2 = []

# Chargement des sons
son_balle = pygame.mixer.Sound("Music/ball_sound.wav")
son_fond = pygame.mixer.Sound("Music/music_fond.mp3")
son_boost = pygame.mixer.Sound("Music/son_boost.wav")
son_soins = pygame.mixer.Sound("Music/son_soins.wav")
son_defaite = pygame.mixer.Sound("Music/son_defaite.wav")
son_tir_ironman = pygame.mixer.Sound("Music/son_tir_Ironman.mp3")
son_menu = pygame.mixer.Sound("Music/music_menu.mp3")

# Variables pour gérer les attaques des joueurs
tir_joueur1 = False
tir_joueur2 = False

# État du jeu
en_jeu = False

def afficher_menu():
    global en_jeu
    # Affichage du menu avec l'image de fond
    fenetre.blit(image_menu, (0, 0))

    #texte_jouer_pyxel = pyxel.text(10, 10, "Bonjour, Pyxel !", 7)  # Dessine le texte à la position (10, 10) avec la couleur d'index 7

    # Texte "Jouer"
    texte_jouer = font1.render("JOUER", True, BLANC)
    rect_jouer = texte_jouer.get_rect(center=(largeur // 2, hauteur // 2 - 50))
    fenetre.blit(texte_jouer, rect_jouer)

    # Texte "Quitter"
    texte_quitter = font2.render("QUITTER", True, BLANC)
    rect_quitter = texte_quitter.get_rect(center=(largeur // 2, hauteur // 2 + 110))
    fenetre.blit(texte_quitter, rect_quitter)

    # Rafraîchissement de l'écran
    pygame.display.flip()

    # Boucle du menu
    while not en_jeu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if rect_jouer.collidepoint(mouse_pos):
                    # Démarrage du jeu
                    en_jeu = True

                elif rect_quitter.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Rafraîchissement de l'écran
        pygame.display.flip()

def demarrer_jeu():
    global en_jeu, joueur1_x, joueur1_y, joueur2_x, joueur2_y, vie_joueur1, vie_joueur2, score_joueur1, score_joueur2
    en_jeu = True
    joueur1_x = 50
    joueur1_y = hauteur // 2 - joueur_taille // 2
    joueur2_x = largeur - 50 - joueur_taille
    joueur2_y = hauteur // 2 - joueur_taille // 2
    vie_joueur1 = 100
    vie_joueur2 = 100
    score_joueur1 = 0
    score_joueur2 = 0
    
    #pygame.mixer.music.stop()  # Arrêter la musique du menu
    #son_fond.play(loops=-1)  # Jouer la musique de fond en boucle

def gerer_clic_menu(pos_clic):
    pos_texte_jouer, pos_texte_quitter = afficher_menu()
    if pos_texte_jouer.collidepoint(pos_clic):
        demarrer_jeu()
    elif pos_texte_quitter.collidepoint(pos_clic):
        pygame.quit()
        sys.exit()

# Fonction pour dessiner les joueurs
def dessiner_joueurs():
    fenetre.blit(Joueur1.image, (joueur1_x, joueur1_y))
    fenetre.blit(Joueur2.image2, (joueur2_x, joueur2_y))

# Fonction pour dessiner les balles
def dessiner_balles():
    for balle in balles_joueur1:
        fenetre.blit(image_bal1,(balle[0], balle[1]))
        #pygame.draw.rect(fenetre, BLEU, (balle[0], balle[1],7, 5))
    for balle in balles_joueur2:
        fenetre.blit(image_bal2,(balle[0], balle[1]))

# Fonction pour dessiner la barre de vie
def dessiner_barre_vie():
    pygame.draw.rect(fenetre, BLEU, (joueur1_x , joueur1_y - vie_hauteur , vie_largeur, vie_hauteur))
    pygame.draw.rect(fenetre, ROUGE, (joueur2_x + joueur_taille - vie_largeur, joueur2_y - vie_hauteur, vie_largeur, vie_hauteur))

# Fonction pour dessiner le boost
def dessiner_boost():
    if boost_actif:
        fenetre.blit(image_boost, (boost_x, boost_y))
     
# Fonction pour dessiner le soin
def dessiner_soins():
    if soins_actif:
        fenetre.blit(image_soins, (soins_x, soins_y))

# Fonction pour afficher la fenêtre de demande de nom de joueur
def afficher_demande_nom():
    son_menu.play()
    son_menu.set_volume(0.5)
    global nom_joueur1, nom_joueur2
    demande_nom = True  # Variable pour contrôler la boucle de demande de nom
    joueur_actuel = 1  # Variable pour suivre le joueur actuel

    while demande_nom:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if joueur_actuel == 1:
                        joueur_actuel = 2
                    elif joueur_actuel == 2:
                        demande_nom = False  # Sortir de la boucle de demande de nom pour passer au joueur 2
                        afficher_menu()
                elif event.key == pygame.K_BACKSPACE:
                    if joueur_actuel == 1:
                        nom_joueur1 = nom_joueur1[:-1]
                    elif joueur_actuel == 2:
                        nom_joueur2 = nom_joueur2[:-1]
                else:
                    if joueur_actuel == 1 and len(nom_joueur1) < 20:
                        nom_joueur1 += event.unicode
                    elif joueur_actuel == 2 and len(nom_joueur2) < 20:
                        nom_joueur2 += event.unicode

        # Effacement de l'écran
        fenetre.blit(image_menu, (0, 0))

        # Affichage des textes de demande de nom
        texte_titre = font1.render("QWELD ARENA", True, BLANC)
        rect_titre= texte_titre.get_rect(topleft=(( largeur /2) - 250 , (hauteur /2) -100 ))
        fenetre.blit(texte_titre, rect_titre)

        texte_demande = font2.render("Veuillez entrer ", True, BLANC)
        rect_demande= texte_demande.get_rect(topleft=(( largeur /2) - 90 , (hauteur /2)  ))
        fenetre.blit(texte_demande, rect_demande)

        texte_joueur1 = font3.render("Pseudo :", True, BLANC)
        rect_joueur1 = texte_joueur1.get_rect(topleft=(( largeur /2) - 200 , (hauteur /2) + 50 ))
        fenetre.blit(texte_joueur1, rect_joueur1)

        texte_joueur2 = font3.render("Pseudo :", True, BLANC)
        rect_joueur2 = texte_joueur2.get_rect(topleft=(( largeur /2) + 90 , (hauteur /2) + 50))
        fenetre.blit(texte_joueur2, rect_joueur2)

        # Affichage des noms entrés
        texte_nom_joueur1 = font3.render(nom_joueur1, True, BLANC)
        texte_nom_joueur2 = font3.render(nom_joueur2, True, BLANC)
        rect_nom_joueur1 = texte_nom_joueur1.get_rect(topleft=( ( largeur /2) - 100 , (hauteur /2) + 50 ))
        rect_nom_joueur2 = texte_nom_joueur2.get_rect(topleft=(( largeur /2) + 200 , (hauteur /2) + 50 ))
        fenetre.blit(texte_nom_joueur1, rect_nom_joueur1)
        fenetre.blit(texte_nom_joueur2, rect_nom_joueur2)

        # Rafraîchissement de l'écran
        pygame.display.flip()

def bloquer_joueur():
    global joueur1_x, joueur2_x
    # Largeur maximale atteignable par les joueurs
    largeur_max = largeur // 2 - joueur_taille //2

    # Vérifier si le joueur 1 dépasse la moitié de la largeur
    if joueur1_x > largeur_max:
        joueur1_x = largeur_max
    
    # Vérifier si le joueur 2 dépasse la moitié de la largeur
    if joueur2_x < largeur_max:
        joueur2_x = largeur_max

# Boucle principale du jeu
while True:
    if not en_jeu:
        afficher_demande_nom()
        if nom_joueur1 != "" and nom_joueur2 != "" :
            afficher_menu()
            
    else:   
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_SPACE:
                    tir_joueur1 = True
                elif evenement.key == pygame.K_RETURN:
                    tir_joueur2 = True
            elif evenement.type == pygame.KEYUP:
                if evenement.key == pygame.K_SPACE:
                    tir_joueur1 = False
                elif evenement.key == pygame.K_RETURN:
                    tir_joueur2 = False
            elif evenement.type == pygame.MOUSEBUTTONUP:
                pos_souris = pygame.mouse.get_pos()
                if not en_jeu:
                    gerer_clic_menu(pos_souris)

        #metre a jour le code
        Joueur1.animate()
        Joueur2.animate2()
    
        # Effacement de l'écran
        fenetre.blit(image_fond_jeu, (0, 0))
    
        # Affichage des joueurs
        dessiner_joueurs()

        # Déplacement du joueur 1
        touches = pygame.key.get_pressed()
        if touches[pygame.K_UP] and joueur2_y > 0:
            joueur2_y -= joueur_vitesse_2
        if touches[pygame.K_DOWN] and joueur1_y < hauteur - joueur_taille:
            joueur2_y += joueur_vitesse_2
        if touches[pygame.K_LEFT] and joueur2_x > 0:
            joueur2_x -= joueur_vitesse_2
        if touches[pygame.K_RIGHT] and joueur2_x < largeur - joueur_taille:
            joueur2_x += joueur_vitesse_2

        # Déplacement du joueur 2
        touches = pygame.key.get_pressed()
        if touches[pygame.K_z] and joueur1_y > 0:
            joueur1_y -= joueur_vitesse_1
        if touches[pygame.K_s] and joueur1_y < hauteur - joueur_taille:
            joueur1_y += joueur_vitesse_1
        if touches[pygame.K_q] and joueur1_x > 0:
            joueur1_x -= joueur_vitesse_1
        if touches[pygame.K_d] and joueur1_x < largeur - joueur_taille:
            joueur1_x += joueur_vitesse_1
        bloquer_joueur()

        # Lancement des attaques du joueur 1
        if tir_joueur1:
            balle = pygame.Rect(joueur1_x + joueur_taille + 18 , joueur1_y + joueur_taille - 50, 5, 5)
            balles_joueur1.append(balle)
            tir_joueur1 = False  # Réinitialiser le tir du joueur 1
            son_balle.play()  # Jouer le son de balle

        # Lancement des attaques du joueur 2
        if tir_joueur2:
            balle = pygame.Rect(joueur2_x - 5, joueur2_y + joueur_taille // 2, 5, 5)
            balles_joueur2.append(balle)
            tir_joueur2 = False  # Réinitialiser le tir du joueur 2
            son_tir_ironman.play()  # Jouer le son de balle

        # Affichage des balles
        dessiner_balles()

        # Déplacement des balles
        for balle in balles_joueur1:
            balle[0] += balle_vitesse
        for balle in balles_joueur2:
            balle[0] -= balle_vitesse

        # Suppression des balles qui sortent de l'écran
        balles_joueur1 = [balle for balle in balles_joueur1 if balle[0] < largeur]
        balles_joueur2 = [balle for balle in balles_joueur2 if balle[0] > 0]

        # Affichage de la barre de vie
        dessiner_barre_vie()

        # Vérification des collisions
        for balle in balles_joueur1:
            if joueur2_x <= balle[0] <= joueur2_x + joueur_taille:
                if joueur2_y <= balle[1] <= joueur2_y + joueur_taille:
                    if vie_joueur2 > 0:
                        balles_joueur1.remove(balle)
                        vie_joueur2 -= 20
                    
                    else:            
                        joueur1_perdu = True

        for balle in balles_joueur2:
            if joueur1_x <= balle[0] <= joueur1_x + joueur_taille:
                if joueur1_y <= balle[1] <= joueur1_y + joueur_taille:
                    if vie_joueur1 > 0:
                        balles_joueur2.remove(balle)
                        vie_joueur1 -= 20
                    
                    else:
                        joueur2_perdu = True

        #mise a jour du score
        if vie_joueur1 <=0:
            score_joueur2 += 1
            vie_joueur1 = 100
            son_defaite.play()

        elif vie_joueur2 <= 0:
            score_joueur1 += 1
            vie_joueur2 = 100
            son_defaite.play()
            
        # Ecrant de defaite
        if score_joueur1 == 5 :
            fenetre.blit(image_menu, (0, 0))
            texte_defaite = font2.render("VOUS AVEZ GANER "+ nom_joueur1 , True, OR)
            rect_defaite = texte_defaite.get_rect(center=(largeur // 2, hauteur // 2))
            fenetre.blit(texte_defaite, rect_defaite)
            pygame.display.flip()
            pygame.time.delay(8000)  # Attente de 3 secondes
            joueur1_perdu = False  # Réinitialisation de l'état de défaite
            joueur2_perdu = False  # Réinitialisation de l'état de défaite
            
            afficher_demande_nom()
            demarrer_jeu()  # Redémarrage du jeu

        elif score_joueur2 == 5:
            fenetre.blit(image_menu, (0, 0))
            texte_defaite = font2.render(" VOUS AVEZ GAGNER " + nom_joueur2, True, OR)
            rect_defaite = texte_defaite.get_rect(center=(largeur // 2, hauteur // 2))
            fenetre.blit(texte_defaite, rect_defaite)
            pygame.display.flip()
            pygame.time.delay(8000)  # Attente de 3 secondes
            joueur1_perdu = False  # Réinitialisation de l'état de défaite
            joueur2_perdu = False  # Réinitialisation de l'état de défaite
            
            afficher_demande_nom()
            demarrer_jeu()  # Redémarrage du jeu

        # Affichage du boost
        dessiner_boost()
        # Affichage du soins
        dessiner_soins()

        # Vérification de la collision avec le boost
        if boost_actif and joueur1_x <= boost_x <= joueur1_x + joueur_taille and joueur1_y <= boost_y <= joueur1_y + joueur_taille:
            son_boost.play()
            joueur_vitesse_1 += 5
            boost_actif = False
        if boost_actif and joueur2_x <= boost_x <= joueur2_x + joueur_taille and joueur2_y <= boost_y <= joueur2_y + joueur_taille:
            son_boost.play()
            joueur_vitesse_2 += 5
            boost_actif = False
        
        # vérification de la collision avec le soins
        if soins_actif and joueur1_x <= soins_x <= joueur1_x + joueur_taille and joueur1_y <= soins_y <= joueur1_y + joueur_taille:
            son_soins.play()
            vie_joueur1 += 50
            soins_actif = False
        if soins_actif and joueur2_x <= soins_x <= joueur2_x + joueur_taille and joueur2_y <= soins_y <= joueur2_y + joueur_taille:
            son_soins.play()
            vie_joueur2 += 50
            soins_actif = False

        # Gestion de l'apparition du boost
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - boost_temps >= temps_apparition_boost:
            boost_x = random.randint(joueur_taille, largeur - joueur_taille)
            boost_y = random.randint(0, hauteur - joueur_taille)
            boost_actif = True
            boost_temps = temps_actuel
        
        # Gestion de l'apparition du soins
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - soins_temps >= temps_apparition_soins:
            soins_x = random.randint(joueur_taille, largeur - joueur_taille)
            soins_y = random.randint(0, hauteur - joueur_taille)
            soins_actif = True
            soins_temps = temps_actuel

        # Affichage du score
        texte_score = font2.render("SCORE: {} - {}".format(score_joueur1, score_joueur2), True, BLANC)
        fenetre.blit(texte_score, (largeur // 2 - texte_score.get_width() // 2, 10))

        # Affichage de la vie des joueurs
        texte_vie_joueur1 = font3.render(format(vie_joueur1), True, BLEU)
        fenetre.blit(texte_vie_joueur1, (joueur1_x, joueur1_y - vie_hauteur - texte_vie_joueur1.get_height()))
        texte_vie_joueur2 = font3.render(format(vie_joueur2), True, ROUGE)
        fenetre.blit(texte_vie_joueur2, (joueur2_x, joueur2_y - vie_hauteur - texte_vie_joueur2.get_height()))

        # Rafraîchissement de l'écran
        pygame.display.flip()

        # Limitation de la vitesse de rafraîchissement de l'écran
        horloge.tick(60)
