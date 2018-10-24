import pygame
import random

display_width = 800
display_height = 600


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
yellow = (255, 255, 0)
sky_blue = (135, 206, 250)
BLOCK_SIZE = 10

FPS = 18


class GameSession(object):
    def __init__(self):
        """Loads the configuration for the current pygame session"""
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption('snake game')
        self.background_image = pygame.image.load("snake.png")
        self.pause_image = pygame.image.load("pause.jpg")

        self.font = pygame.font.SysFont(None, 35)
        self.lfont = pygame.font.SysFont(None, 75)
        self.clock = pygame.time.Clock()

    def pause_game(self):
        """Pauses game and shows holding screen"""
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            self.gameDisplay.fill(white)
            self.gameDisplay.blit(self.pause_image, [280, 35])
            self.message_to_screen("Paused", red, 20, 'L')
            self.message_to_screen("Press r for Resume and q for Quit", red, 90, 's')
            pygame.display.update()

    def update_score(self, points):
        """Renders the user's current points"""
        text = self.font.render("SCORE:" + str(points), True, black)
        self.gameDisplay.blit(text, [0, 0])

    def show_keyboard_shortcuts(self):
        """Show keyboard shortcuts on screen"""
        intro1 = True
        while intro1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.show_intro()
                        intro1 = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_h:
                        self.show_intro()
                        intro1 = False
                        self.gameDisplay.fill(white)
            self.message_to_screen("Shortcuts for snake game", green, -200, 'L')
            self.message_to_screen("Play -> p", black, -100, 's')
            self.message_to_screen("Quit -> q", black, -55, 's')
            self.message_to_screen("Pause -> b", black, 80, 's')
            self.message_to_screen("Resume -> r", black, 125, 's')
            self.message_to_screen("Back -> e", black, -10, 's')
            self.message_to_screen("Shortcuts -> s", black, 170, 's')
            self.message_to_screen("Home -> h", black, 35, 's')
            pygame.display.update()

    def show_intro(self):
        intro = True
        while intro:
            self.gameDisplay.fill(white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.gameloop()
                        intro = False
                    elif event.key == pygame.K_q:
                        intro = False
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_s:
                        self.show_keyboard_shortcuts()
                        intro = False
                        self.gameDisplay.blit(self.background_image, [85, 50])
            self.message_to_screen("Welcome to snake game", green, -200, 'L')
            self.message_to_screen("Press q for Quit", black, -100, 's')
            self.message_to_screen("Press p for Play", black, -50, 's')
            self.message_to_screen("Press s for Shortcuts", black, 0, 's')
            pygame.display.update()

    def text_objects(self, text, color, size):
        if size == "L":
            text_surface = self.lfont.render(text, True, color)
        else:
            text_surface = self.font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def message_to_screen(self, msg, color, y_displace, size):
        textsurf, textrect = self.text_objects(msg, color, size)
        textrect.center = (display_width / 2), (display_height / 2) + y_displace
        self.gameDisplay.blit(textsurf, textrect)

    def snake_create(self, block_size, snakelist):
        for XY in snakelist:
            pygame.draw.rect(self.gameDisplay, green, [XY[0], XY[1], block_size, block_size])

    def gameloop(self):
        game_exit = False
        game_over = False
        lead_x = display_width / 2
        lead_y = display_height / 2
        snakelist = []
        snakelength = 1
        lead_x_change = 0
        lead_y_change = 0
        randapple_x = round(random.randrange(0, display_width - BLOCK_SIZE) / 10.0) * 10.0
        randapple_y = round(random.randrange(0, display_height - BLOCK_SIZE) / 10.0) * 10.0
        while not game_exit:
            if game_over is True:
                self.message_to_screen("Game over", red, -200, 'L')
                self.message_to_screen("Press p for Play again!", black, -100, 's')
                self.message_to_screen("Press q for Quit!", black, -50, 's')
                self.message_to_screen("Press h for Home!", black, 0, 's')
                pygame.display.update()
            while game_over is True:

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_exit = True
                        game_over = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = False
                            game_exit = True
                        if event.key == pygame.K_h:
                            self.show_intro()
                        if event.key == pygame.K_p:
                            self.gameloop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        lead_x_change = -BLOCK_SIZE
                        lead_y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        lead_x_change = BLOCK_SIZE
                        lead_y_change = 0
                    elif event.key == pygame.K_UP:
                        lead_y_change = -BLOCK_SIZE
                        lead_x_change = 0
                    elif event.key == pygame.K_DOWN:
                        lead_y_change = BLOCK_SIZE
                        lead_x_change = 0
                    elif event.key == pygame.K_b:
                        self.pause_game()
            if lead_x <= 0 or lead_y <= 0 or lead_x >= display_width or lead_y >= display_height:
                game_over = True

            lead_x += lead_x_change
            lead_y += lead_y_change

            self.gameDisplay.fill(white)
            pygame.draw.rect(self.gameDisplay, red, [randapple_x, randapple_y, BLOCK_SIZE, BLOCK_SIZE])
            self.snake_create(BLOCK_SIZE, snakelist)
            self.update_score(snakelength - 1)
            pygame.display.update()

            snakehead = list()
            snakehead.append(lead_x)
            snakehead.append(lead_y)
            snakelist.append(snakehead)
            if snakelength < len(snakelist):
                del(snakelist[0])

            if lead_x == randapple_x and lead_y == randapple_y:
                randapple_x = round(random.randrange(0, display_width - BLOCK_SIZE) / 10.0) * 10.0
                randapple_y = round(random.randrange(0, display_height - BLOCK_SIZE) / 10.0) * 10.0
                snakelength += 1

                self.clock.tick(FPS)

        pygame.quit()
        quit()


if __name__ == '__main__':
    game_session = GameSession()
    game_session.show_intro()
