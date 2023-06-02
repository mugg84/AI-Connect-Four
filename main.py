import pygame
import neat
import game

pygame.init()
BACKGROUND_COLOR = (0, 0, 0)
ROWS = 6
COLUMS = 7
SQUARE = BORDER = 100
RADIUS = int(SQUARE / 2 - 10)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
BLACK = 0, 0, 0
BLUE = 0, 0, 255
RED = 255, 0, 0
YELLOW = 255, 215, 0


class Connect:
    def __init__(self):
        # Initializing the game screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Creating a new Game instance with the specified parameters
        self.game = game.Game(
            self.screen, ROWS, COLUMS, SQUARE, BORDER, RADIUS, BLACK, BLUE, RED, YELLOW
        )

    def main(self):
        self.game.draw()  # Drawing the initial state of the game board

        isRunning = True
        while isRunning:
            # Main game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If the user has closed the window, stop running the game
                    isRunning = False
                    break

                if event.type == pygame.MOUSEMOTION:
                    # If the mouse is moved, redraw the player's move
                    self.game.draw_player_move(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the mouse is clicked, register the player's move
                    self.game.player_move(event)

                # Redraw the game board and update the display
                self.game.draw()
                pygame.display.update()

                if self.game.game_over:
                    # If the game is over, wait for 3 seconds and then start a new game
                    pygame.time.wait(3000)
                    self.game.new_game()


if __name__ == "__main__":
    # Creating an instance of the Connect class and starting the game
    game = Connect()
    game.main()
