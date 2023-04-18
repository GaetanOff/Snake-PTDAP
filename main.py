import random

import pygame

# Initialisation de Pygame
pygame.init()

# Constantes

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DGREEN = (0, 128, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GRID_GREEN_1 = (57, 181, 90)
GRID_GREEN_2 = (30, 158, 64)
SNAKE_BLUE = (27, 128, 183)

# Taille de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Images
APPLE = pygame.image.load("assets/img/apple.png")
HEAD_UP = pygame.image.load("assets/img/up.png")
HEAD_DOWN = pygame.image.load("assets/img/down.png")
HEAD_LEFT = pygame.image.load("assets/img/left.png")
HEAD_RIGHT = pygame.image.load("assets/img/right.png")

# Son
EAT_SOUND = pygame.mixer.Sound("assets/sound/eat.ogg")
DEATH_SOUND = pygame.mixer.Sound("assets/sound/death.ogg")
AMBIANCE_SOUND = pygame.mixer.Sound("assets/sound/snakecharmer.mp3")

# FPS
clock = pygame.time.Clock()
fps = 8
block_size = 50

# Police
font = pygame.font.SysFont(None, 25)

# Création de la fenêtre
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("GaetanDev • Snake")


# Fonction pour dessiner la grille
def drawGrid():
    for x in range(0, SCREEN_WIDTH, block_size * 2):
        for y in range(0, SCREEN_HEIGHT, block_size * 2):
            rect1 = pygame.Rect(x, y, block_size, block_size)
            rect2 = pygame.Rect(x + block_size, y + block_size, block_size, block_size)
            pygame.draw.rect(gameDisplay, GRID_GREEN_2, rect1)
            pygame.draw.rect(gameDisplay, GRID_GREEN_2, rect2)


# Fonction pour dessiner le serpent
def snake(snake_list, lead_x, lead_y, position):
    snake_heads = {
        "up": pygame.transform.scale(HEAD_UP, (block_size, block_size)),
        "down": pygame.transform.scale(HEAD_DOWN, (block_size, block_size)),
        "left": pygame.transform.scale(HEAD_LEFT, (block_size, block_size)),
        "right": pygame.transform.scale(HEAD_RIGHT, (block_size, block_size))
    }
    for XnY in snake_list[:-1]:
        pygame.draw.rect(gameDisplay, SNAKE_BLUE, [XnY[0], XnY[1], block_size, block_size])

    gameDisplay.blit(snake_heads[position], (lead_x, lead_y))


# Fonction pour afficher un message à l'écran
def message_to_screen(msg, color, x, y):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x, y])


# Fonction principale pour le jeu
def gameLoop():
    # Initialisation des variables
    game_exit = False
    game_over = False

    lead_x = SCREEN_WIDTH / 2
    lead_y = SCREEN_HEIGHT / 2
    lead_x_change = 0
    lead_y_change = 0

    snake_list = []
    snake_length = 1
    snake_position = "up"

    score = 0

    rand_apple_x = round(random.randrange(0, SCREEN_WIDTH - block_size) / block_size) * block_size
    rand_apple_y = round(random.randrange(0, SCREEN_HEIGHT - block_size) / block_size) * block_size

    start_ticks = pygame.time.get_ticks()

    AMBIANCE_SOUND.set_volume(0.3)
    AMBIANCE_SOUND.play(loops=-1)

    # Boucle principal
    while not game_exit:
        while game_over:

            # Ecran de fin de jeu
            gameDisplay.fill(BLACK)
            message_to_screen("Mort ! Appuyez sur C pour continuer ou sur Q pour quitter.", WHITE, 180, 280)
            message_to_screen(''.join(["Votre score était: ", str(score)]), WHITE, 300, 325)
            message_to_screen(''.join(["Votre durée était: ", str(seconds)]), WHITE, 300, 350)
            pygame.display.update()

            # Gestion des événements de fin de partie
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        DEATH_SOUND.stop()
                        gameLoop()
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                elif event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False

        # Gestion des événements de jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                    snake_position = "left"
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    snake_position = "right"
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                    snake_position = "down"
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                    snake_position = "up"

        # Changement de position du serpent
        lead_x += lead_x_change
        lead_y += lead_y_change

        # Vérification si le serpent sort de l'écran
        if lead_x >= SCREEN_WIDTH or lead_x < 0 or lead_y >= SCREEN_HEIGHT or lead_y < 0:
            AMBIANCE_SOUND.stop()
            pygame.mixer.Sound.play(DEATH_SOUND)
            game_over = True

        # Affichage de l'écran de jeu
        gameDisplay.fill(GRID_GREEN_1)
        drawGrid()
        message_to_screen(''.join(["Score: ", str(score)]), WHITE, 10, 10)

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        message_to_screen(''.join(["Durée: ", str(seconds)]), WHITE, 10, 30)

        # Affichage de la pomme
        apple_resized = pygame.transform.scale(APPLE, (block_size, block_size))
        gameDisplay.blit(apple_resized, (rand_apple_x, rand_apple_y))

        # Ajout de la tête du serpent dans la liste
        snake_head = [lead_x, lead_y]
        snake_list.append(snake_head)

        # Si le serpent a dépassé la longueur maximum
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Vérification si le serpent se mord la queue
        for eachSegment in snake_list[:-1]:
            if eachSegment == snake_head:
                AMBIANCE_SOUND.stop()
                pygame.mixer.Sound.play(DEATH_SOUND)
                game_over = True

        # Affichage du serpent
        snake(snake_list, lead_x, lead_y, snake_position)

        # Vérification si le serpent a mangé la pomme
        if lead_x == rand_apple_x and lead_y == rand_apple_y:
            pygame.mixer.Sound.play(EAT_SOUND)
            rand_apple_x = round(random.randrange(0, SCREEN_WIDTH - block_size) / block_size) * block_size
            rand_apple_y = round(random.randrange(0, SCREEN_HEIGHT - block_size) / block_size) * block_size
            snake_length += 1
            score += 1
            message_to_screen(''.join(["Score: ", str(score)]), WHITE, 10, 10)

        pygame.display.update()

        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    gameLoop()
