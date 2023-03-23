from moteur import *
from Laby import *
from button import *
from old.Affichage_sprite import *

# on initialise la taille (longueur d'un côté) du labyrinthe carré à 10 qui pourra être modifiée dans le menu du jeu
taille = 10
longueur = 10
hauteur = 10

longueur_fenetre = 700
hauteur_fenetre = 700

pygame.init()
screen = pygame.display.set_mode((longueur_fenetre, hauteur_fenetre))  # on définit les dimensions de la fenêtre du jeu
background = pygame.image.load('../assets/image.png')  # on charge les assets
# on veut que l'image de fond prenne toute la fenêtre
background = pygame.transform.scale(background, (longueur_fenetre, hauteur_fenetre))

pygame.display.set_caption("Labyrinthe")
font = pygame.font.SysFont("Times New Roman, Arial", 50)

running = True
debut = False
difficult = False
difficile = pygame.image.load('../assets/dark.png')


while running:

    screen.blit(background, (0, 0))
    screen.blit(play, play_rect)

    if taille < 50:
        screen.blit(up_width, up_width_rect)

    if taille > 5:
        screen.blit(down_width, down_width_rect)

    screen.blit(bas2, bas2_rect)

    font_taille = font.render('Taille  :' + str(taille), True, (0, 0, 0), (255, 255, 255))
    screen.blit(font_taille, (200, 120))

    if difficult:
        ombre = "OUI"
    else:
        ombre = "NON"
    display_dificulty = font.render('Mode difficile : ' + ombre, True, (0, 0, 0), (255, 255, 255))
    screen.blit(display_dificulty, (200, 200))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:

            if taille < 50:
                taille = click(event, up_width_rect, taille, 5)
            if taille > 5:
                taille = click(event, down_width_rect, taille, -5)
            if change_mod(event, bas2_rect, difficult) is not None:
                difficult = change_mod(event, bas2_rect, difficult)
            if play_rect.collidepoint(event.pos) and not taille == 0:
                debut = True
                maze = Laby(taille, taille)
                graphe = maze.creation()
                moteur = Moteur(graphe, 0, taille ** 2 - 1, difficult)
                add(moteur.taille, moteur.matrice, moteur.liste_aff)
        if event.type == pygame.QUIT:
            running = False
            debut = False

    pygame.display.flip()

    while debut:
        moteur.liste_aff.draw(screen)
        screen.blit(moteur.depart.image, (moteur.depart.rect.x, moteur.depart.rect.y))
        screen.blit(moteur.arrive.image, (moteur.arrive.rect.x, moteur.arrive.rect.y))

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                    debut = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_LEFT | pygame.K_q:
                            moteur.perso.test_emplacement(moteur.matrice, 'gauche')
                        case pygame.K_RIGHT | pygame.K_d:
                            moteur.perso.test_emplacement(moteur.matrice, 'droite')
                        case pygame.K_DOWN | pygame.K_s:
                            moteur.perso.test_emplacement(moteur.matrice, 'bas')
                        case pygame.K_UP | pygame.K_z:
                            moteur.perso.test_emplacement(moteur.matrice, 'haut')
                        case pygame.K_ESCAPE:
                            print(maze.solution(moteur.perso.position, graphe))

        screen.blit(moteur.perso.image, moteur.perso.rect)

        if moteur.difficile:
            # si on est en mode difficile, on affiche une ombre autour le personnage
            screen.blit(difficile, (moteur.perso.rect.x - difficile.get_width() // 2 + moteur.perso.rect.width // 2
                                    ,
                                    moteur.perso.rect.y - difficile.get_height() // 2 + moteur.perso.rect.height // 2))

        if moteur.perso.position == taille ** 2:
            running = False
            debut = False
            msg = font.render('You Win !', True, (255, 255, 255))
            # on veut que le message apparaisse au milieu de l'écran
            msg_rect = msg.get_rect(center=(350, 350))
            screen.blit(msg, msg_rect)

        pygame.display.flip()

        if not debut:
            pygame.time.wait(800)

pygame.quit()
