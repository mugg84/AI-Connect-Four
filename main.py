import pygame
import neat
import os
import pickle
import game

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700


class Connect:
    def __init__(self):
        # Initializing the game screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Creating a new Game instance with the specified parameters
        self.game = game.Game(
            self.screen,
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

    def train_ai(self, genome1, genome2, config):
        """
        Train the AI by passing two NEAT neural networks and the NEAt config object.
        These AI's will play against eachother to determine their fitness.
        """
        run = True

        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1 = genome1
        self.genome2 = genome2
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            self.game.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            if self.game.turn == 0:
                game_info = self.game.ai_move(net1, genome1, self.game.board)
            else:
                game_info = self.game.ai_move(net2, genome2, self.game.board)

            pygame.display.update()

            if self.game.game_over or game_info.invalid_moves > 10:
                self.calculate_fitness(game_info)
                break

        return False

    def calculate_fitness(self, game_info):
        self.genome1.fitness += game_info.total_turns / 42
        self.genome2.fitness += game_info.total_turns / 42


# Create and initialize a NEAT population and run the genetic algorithm
def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(200))

    # Run the algorithm for up to 1000 generations and save the best genome
    winner = p.run(eval_genomes)

    with open("best.pickle", "wb") as f:
        # Save the best genome for future use
        pickle.dump(winner, f)


# Run each genome through the game until the fitness threshold is reached or the epoch limit is hit
def eval_genomes(genomes, config):
    pygame.display.set_caption("Connect 4")

    for i, (_genome_id1, genome1) in enumerate(genomes):
        genome1.fitness = 0
        for _genome_id2, genome2 in genomes[min(i + 1, len(genomes) - 1) :]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = Connect()

            force_quit = game.train_ai(genome1, genome2, config)
            if force_quit:
                quit()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    # Creating an instance of the Connect class and starting the game
    # game = Connect()
    # game.main()
    run_neat(config)
