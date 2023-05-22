import random
import pygame


class Game:
    def __init__(self):
        pygame.init()

        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.DGREEN = (0, 128, 0)
        self.BLUE = (0, 0, 255)
        self.PURPLE = (128, 0, 128)
        self.GRID_GREEN_1 = (57, 181, 90)
        self.GRID_GREEN_2 = (30, 158, 64)
        self.SNAKE_BLUE = (27, 128, 183)

        # Variables
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.fps = 8
        self.block_size = 50
        self.font = pygame.font.SysFont(None, 25)

        # Initialisation de la fenêtre
        self.gameDisplay = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("DreamTeam • Snake")

        # Horloge
        self.clock = pygame.time.Clock()

        # Images et sons
        self.snake_heads = {
            "up": pygame.image.load("assets/img/up.png"),
            "down": pygame.image.load("assets/img/down.png"),
            "left": pygame.image.load("assets/img/left.png"),
            "right": pygame.image.load("assets/img/right.png")
        }
        self.apple = pygame.image.load("assets/img/apple.png")
        self.eat_sound = pygame.mixer.Sound("assets/sound/eat.ogg")
        self.death_sound = pygame.mixer.Sound("assets/sound/death.ogg")
        self.ambiance_sound = pygame.mixer.Sound("assets/sound/snakecharmer.mp3")
        self.start_ticks = pygame.time.get_ticks()

    # Fonction pour déssiner la grille
    def drawGrid(self):
        for x in range(0, self.SCREEN_WIDTH, self.block_size * 2):
            for y in range(0, self.SCREEN_HEIGHT, self.block_size * 2):
                rect1 = pygame.Rect(x, y, self.block_size, self.block_size)
                rect2 = pygame.Rect(x + self.block_size, y + self.block_size, self.block_size, self.block_size)
                pygame.draw.rect(self.gameDisplay, self.GRID_GREEN_2, rect1)
                pygame.draw.rect(self.gameDisplay, self.GRID_GREEN_2, rect2)

    # Fonction pour déssiner le serpent
    def snake(self, snake_list, lead_x, lead_y, position):
        snake_heads = {
            "up": pygame.transform.scale(self.snake_heads['up'], (self.block_size, self.block_size)),
            "down": pygame.transform.scale(self.snake_heads['down'], (self.block_size, self.block_size)),
            "left": pygame.transform.scale(self.snake_heads['left'], (self.block_size, self.block_size)),
            "right": pygame.transform.scale(self.snake_heads['right'], (self.block_size, self.block_size))
        }
        for XnY in snake_list[:-1]:
            pygame.draw.rect(self.gameDisplay, self.SNAKE_BLUE, [XnY[0], XnY[1], self.block_size, self.block_size])

        self.gameDisplay.blit(snake_heads[position], (lead_x, lead_y))

    # Fonction pour afficher un message à l'écran
    def message_to_screen(self, msg, color, x, y):
        screen_text = self.font.render(msg, True, color)
        self.gameDisplay.blit(screen_text, [x, y])

    # Fonction principale du jeu
    def gameLoop(self):

        # Variables
        game_exit = False
        game_over = False
        lead_x = self.SCREEN_WIDTH / 2
        lead_y = self.SCREEN_HEIGHT / 2
        lead_x_change = 0
        lead_y_change = 0
        snake_list = []
        snake_length = 1
        snake_position = "up"
        seconds = 0
        score = 0
        rand_apple_x = round(
            random.randrange(0, self.SCREEN_WIDTH - self.block_size) / self.block_size) * self.block_size
        rand_apple_y = round(
            random.randrange(0, self.SCREEN_HEIGHT - self.block_size) / self.block_size) * self.block_size

        start_ticks = pygame.time.get_ticks()

        # Activer la musique d'ambiance
        self.ambiance_sound.set_volume(0.3)
        self.ambiance_sound.play(loops=-1)

        while not game_exit:
            while game_over:
                # Ecran de fin de jeu
                self.gameDisplay.fill(self.BLACK)
                self.message_to_screen("Mort ! Appuyez sur C pour continuer ou sur Q pour quitter.", self.WHITE, 180,
                                       280)
                self.message_to_screen(''.join(["Votre score était: ", str(score)]), self.WHITE, 300, 325)
                self.message_to_screen(''.join(["Votre durée était: ", str(seconds)]), self.WHITE, 300, 350)
                pygame.display.update()

                # Gestion des événements de fin de partie
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            self.death_sound.stop()
                            self.gameLoop()
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
                        lead_x_change = -self.block_size
                        lead_y_change = 0
                        snake_position = "left"
                    elif event.key == pygame.K_RIGHT:
                        lead_x_change = self.block_size
                        lead_y_change = 0
                        snake_position = "right"
                    elif event.key == pygame.K_DOWN:
                        lead_y_change = self.block_size
                        lead_x_change = 0
                        snake_position = "down"
                    elif event.key == pygame.K_UP:
                        lead_y_change = -self.block_size
                        lead_x_change = 0
                        snake_position = "up"

            # Changement de position du serpent
            lead_x += lead_x_change
            lead_y += lead_y_change

            # Vérification si le serpent sort de l'écran
            if lead_x >= self.SCREEN_WIDTH or lead_x < 0 or lead_y >= self.SCREEN_HEIGHT or lead_y < 0:
                self.ambiance_sound.stop()
                pygame.mixer.Sound.play(self.death_sound)
                game_over = True

            # Affichage de l'écran de jeu
            self.gameDisplay.fill(self.GRID_GREEN_1)
            self.drawGrid()
            self.message_to_screen(''.join(["Score: ", str(score)]), self.WHITE, 10, 10)

            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            self.message_to_screen(''.join(["Durée: ", str(seconds)]), self.WHITE, 10, 30)

            # Affichage de la pomme
            apple_resized = pygame.transform.scale(self.apple, (self.block_size, self.block_size))
            self.gameDisplay.blit(apple_resized, (rand_apple_x, rand_apple_y))

            # Ajout de la tête du serpent dans la liste
            snake_head = [lead_x, lead_y]
            snake_list.append(snake_head)

            # Si le serpent a dépassé la longueur maximum
            if len(snake_list) > snake_length:
                del snake_list[0]

            # Vérification si le serpent se mord la queue
            for eachSegment in snake_list[:-1]:
                if eachSegment == snake_head:
                    self.ambiance_sound.stop()
                    pygame.mixer.Sound.play(self.death_sound)
                    game_over = True

            # Affichage du serpent
            self.snake(snake_list, lead_x, lead_y, snake_position)

            # Vérification si le serpent a mangé la pomme
            if lead_x == rand_apple_x and lead_y == rand_apple_y:
                pygame.mixer.Sound.play(self.eat_sound)
                rand_apple_x = round(
                    random.randrange(0, self.SCREEN_WIDTH - self.block_size) / self.block_size) * self.block_size
                rand_apple_y = round(
                    random.randrange(0, self.SCREEN_HEIGHT - self.block_size) / self.block_size) * self.block_size
                snake_length += 1
                score += 1
                self.message_to_screen(''.join(["Score: ", str(score)]), self.WHITE, 10, 10)

            pygame.display.update()

            self.clock.tick(self.fps)

    pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.gameLoop()
