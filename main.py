import pygame
import math
import numpy as np
import neat

pygame.init()
BACKGROUND_COLOR = (0, 0, 0)
ROWS = 6
COLUMS = 7
SQUARE = 100
RADIUS = int(SQUARE / 2 - 10)
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
BLUE = 0, 0, 255
BLACK = 0, 0, 0
FPS = 60


class Connect:
    def __init__(self):
        # Initializing the game screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def main(self):
        def create_board():
            # Creating the board using a 2D numpy array
            board = np.zeros((ROWS, COLUMS))
            return board

        def check_if_valid(board, col):
            # Checking if the selected column is empty at the top
            if board[0][col] == 0:
                return True
            else:
                return False

        def drop_token(board, col, player_number):
            # Dropping the player's token in the selected column
            for row in range(ROWS - 1, -1, -1):
                if board[row][col] == 0:
                    board[row][col] = player_number
                    break

        def check_if_winner(board):
            # Checking if there is a winner
            directions = [(1, -1), (1, 0), (1, 1), (0, 1)]

            for row in range(ROWS):
                for col in range(COLUMS):
                    for dr, dc in directions:
                        try:
                            if (
                                board[row][col]
                                == board[row + dr][col + dc]
                                == board[row + dr * 2][col + dc * 2]
                                == board[row + dr * 3][col + dc * 3]
                                != 0
                            ):
                                return True
                        except IndexError:
                            pass
            return False

        def draw(board):
            for row in range(ROWS):
                for col in range(COLUMS):
                    pygame.draw.rect(
                        self.screen,
                        BLUE,
                        (col * SQUARE, row * SQUARE + SQUARE, SQUARE, SQUARE),
                    )
                    pygame.draw.circle(
                        self.screen,
                        BLACK,
                        (
                            int(col * SQUARE + SQUARE / 2),
                            int(row * SQUARE + SQUARE + SQUARE / 2),
                        ),
                        RADIUS,
                    )
                    pygame.display.update()

        board = create_board()
        draw(board)
        turn = 0
        isRunning = True

        while isRunning:
            # Main game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if turn == 0:
                        col = int(input("Player one move"))
                        if check_if_valid(board, col):
                            drop_token(board, col, 1)
                        else:
                            print("Wrong move, try again")
                            turn += 1

                    else:
                        col = int(input("Player two move"))
                        if check_if_valid(board, col):
                            drop_token(board, col, 2)
                        else:
                            print("Wrong move, try again")
                            turn += 1

                    if check_if_winner(board):
                        print(f"Player{turn + 1} wins")
                        isRunning = False

                    turn += 1
                    turn %= 2

    #     def main(self):
    #         """
    #         Start and manage the main game loop for a single player game.
    #         """

    #         # Initialize game display and start music
    #         pygame.display.set_caption("Arkanoid")
    #         pygame.mixer.music.play(-1)
    #         clock = pygame.time.Clock()

    #         # Main game loop
    #         running = True

    #         while running:
    #             clock.tick(FPS)
    #             self.screen.blit(self.image, (0, 0))

    #             # Event handling loop
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     pygame.mixer.music.stop()
    #                     running = False
    #                     break

    #             # Update game state and display
    #             self.game.draw()
    #             self.game.loop()

    #             # Key press handling for player input
    #             keys = pygame.key.get_pressed()
    #             if keys[pygame.K_LEFT]:
    #                 self.game.move_paddle(0)
    #             if keys[pygame.K_RIGHT]:
    #                 self.game.move_paddle(1)

    #             pygame.display.update()

    #     def train_ai(self, genome, config):
    #         """
    #         Train the AI using NEAT.
    #         """

    #         # Game loop for AI training
    #         running = True

    #         clock = pygame.time.Clock()

    #         # Create a feed-forward neural network for the current genome
    #         net = neat.nn.FeedForwardNetwork.create(genome, config)
    #         self.genome = genome

    #         while running:
    #             # for real-time visualization, comment it out
    #             # clock.tick(60)

    #             # comment these two lines to increase training speed
    #             self.screen.blit(self.image, (0, 0))
    #             self.game.draw()

    #             # Event handling loop
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     return True

    #             # Update game state and record last scoring time if a collision occurred
    #             game_info = self.game.loop(True)

    #             if game_info.collision_occurred:

    #             # Decide AI move based on current game state
    #             self.move_ai_paddle(net)

    #             pygame.display.update()

    #             # Calculate time since last score

    #             # Terminate current session if no score in 10 seconds

    #             if (
    #                 self.ball.y + self.ball.height // 2 >= SCREEN_HEIGHT + self.ball.height
    #                 or game_info.score == 550
    #             ):
    #                 # Calculate and record fitness of the genome
    #                 self.calculate_fitness(game_info.score, game_info.ball_hit)
    #                 break
    #         return False

    #     def move_ai_paddle(self, net):
    #         # Normalize game state data for the AI's decision-making process
    #         paddle_x_normalized = self.paddle.x / SCREEN_WIDTH
    #         ball_x_normalized = self.ball.x / SCREEN_WIDTH
    #         ball_y_normalized = self.ball.y / SCREEN_HEIGHT
    #         distance_x_ball_paddle = abs(paddle_x_normalized - ball_x_normalized)

    #         # Determine the AI's move based on the network's output
    #         output = net.activate(
    #             (
    #                 paddle_x_normalized,
    #                 ball_x_normalized,
    #                 ball_y_normalized,
    #                 distance_x_ball_paddle,
    #             )
    #         )
    #         decision = output.index(max(output))

    #         valid = True

    #         if decision == 0:  # AI does nothing
    #             pass
    #         elif decision == 1:  # AI moves paddle to the left
    #             valid = self.game.move_paddle(0)
    #         else:  # AI moves paddle to the right
    #             valid = self.game.move_paddle(1)

    #         # Penalize the genome if the AI tries to move outside the screen borders
    #         if not valid:
    #             self.genome.fitness -= 1

    #     def calculate_fitness(self, score, ball_hit):
    #         # Reward the genome for hitting the ball and achieving high scores
    #         # Penalize low scoring genomes and highly reward high scoring genomes
    #         if score <= 30:
    #             self.genome.fitness += ball_hit / 20
    #             self.genome.fitness += score / 20
    #         else:
    #             self.genome.fitness += ball_hit / 10
    #             self.genome.fitness += score / 10

    #         # Adjust for possible random points at the beginnig of the game
    #         self.genome.fitness -= 1

    #         if score > 150:
    #             self.genome.fitness += 20
    #         if score > 400:
    #             self.genome.fitness += 40
    #         if score == 550:
    #             self.genome.fitness += 60

    #         self.game.reset_game()

    # # Run each genome through the game until the fitness threshold is reached or the epoch limit is hit
    # def eval_genomes(genomes, config):
    #     pygame.display.set_caption("Ark")

    #     for _, genome in genomes:
    #         genome.fitness = 0 if genome.fitness is None else genome.fitness

    #         force_quit = ark.train_ai(genome, config)
    #         if force_quit:
    #             quit()

    # # Create and initialize a NEAT population and run the genetic algorithm
    # def run_neat(config):
    #     p = neat.Population(config)
    #     p.add_reporter(neat.StdOutReporter(True))
    #     stats = neat.StatisticsReporter()
    #     p.add_reporter(stats)
    #     p.add_reporter(neat.Checkpointer(50))

    #     # Run the algorithm for up to 1000 generations and save the best genome
    #     winner = p.run(eval_genomes)

    #     with open("best.pickle", "wb") as f:
    #         # Save the best genome for future use
    #         pickle.dump(winner, f)

    # if __name__ == "__main__":
    #     # Determine path to configuration file
    #     local_dir = os.path.dirname(__file__)
    #     config_path = os.path.join(local_dir, "config.txt")

    #     # Load the configuration
    #     config = neat.Config(
    #         neat.DefaultGenome,
    #         neat.DefaultReproduction,
    #         neat.DefaultSpeciesSet,
    #         neat.DefaultStagnation,
    #         config_path,
    #     )
    #

    #     # Uncomment the following lines to run the game, train the AI, or test the AI respectively:
    #     # run game as player


game = Connect()
game.main()


#     # train the AI
#     run_neat(config)

#     # test the AI
#     # test_best_network(config)
