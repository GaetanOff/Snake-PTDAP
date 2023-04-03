import pygame
import random

# Initialisation de Pygame
pygame.init()

# Constantes

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Taille de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# FPS
clock = pygame.time.Clock()
fps = 8
block_size = 50

# Police
font = pygame.font.SysFont(None, 25)


# Fonction pour dessiner le serpent
def snake(block_size, snakeList, lead_x, lead_y):
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, PURPLE, [XnY[0], XnY[1], block_size, block_size])
    pygame.draw.rect(gameDisplay, RED, [lead_x, lead_y, block_size, block_size])


# Fonction pour afficher un message à l'écran
def message_to_screen(msg, color, x, y):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x, y])


gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("GaetanDev • Snake")


# Fonction principale pour le jeu
def gameLoop():
    # Initialisation des variables
    gameExit = False
    gameOver = False

    lead_x = SCREEN_WIDTH / 2
    lead_y = SCREEN_HEIGHT / 2
    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    score = 0

    randAppleX = round(random.randrange(0, SCREEN_WIDTH - block_size) / block_size) * block_size
    randAppleY = round(random.randrange(0, SCREEN_HEIGHT - block_size) / block_size) * block_size

    start_ticks = pygame.time.get_ticks()

    # Boucle principal
    while not gameExit:
        while gameOver:

            # Ecran de fin de jeu
            gameDisplay.fill(RED)
            message_to_screen("Mort ! Appuyez sur C pour continuer ou sur Q pour quitter.", WHITE, 180, 280)
            message_to_screen(''.join(["Votre score était: ", str(score)]), WHITE, 300, 325)
            pygame.display.update()

            # Gestion des événements de fin de partie
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameLoop()
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                elif event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False

        # Gestion des événements de jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0

        # Changement de position du serpent
        lead_x += lead_x_change
        lead_y += lead_y_change

        # Vérification si le serpent sort de l'écran
        if lead_x >= SCREEN_WIDTH or lead_x < 0 or lead_y >= SCREEN_HEIGHT or lead_y < 0:
            gameOver = True

        # Affichage de l'écran de jeu
        gameDisplay.fill(WHITE)
        message_to_screen(''.join(["Score: ", str(score)]), BLACK, 10, 10)

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        message_to_screen(''.join(["Durée: ", str(seconds)]), BLACK, 10, 30)

        # Affichage de la pomme
        pygame.draw.rect(gameDisplay, BLACK, [randAppleX, randAppleY, block_size, block_size])

        # Ajout de la tête du serpent dans la liste
        snakeHead = [lead_x, lead_y]
        snakeList.append(snakeHead)

        # Si le serpent a dépassé la longueur maximum
        if len(snakeList) > snakeLength:
            del snakeList[0]

        # Vérification si le serpent se mord la queue
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        # Affichage du serpent
        snake(block_size, snakeList, lead_x, lead_y)

        # Vérification si le serpent a mangé la pomme
        if lead_x == randAppleX and lead_y == randAppleY:
            randAppleX = round(random.randrange(0, SCREEN_WIDTH - block_size) / block_size) * block_size
            randAppleY = round(random.randrange(0, SCREEN_HEIGHT - block_size) / block_size) * block_size
            snakeLength += 1
            score += 1
            message_to_screen(''.join(["Score: ", str(score)]), BLACK, 10, 10)

        pygame.display.update()

        clock.tick(fps)

    pygame.quit()


gameLoop()
