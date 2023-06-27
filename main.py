import pygame
import neat
import os
import pickle
import game

# import neat_functions


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

        is_running = True
        while is_running:
            # Main game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If the user has closed the window, stop running the game
                    is_running = False
                    break

                if event.type == pygame.MOUSEMOTION:
                    # If the mouse is moved, redraw the player's move
                    self.game.draw_player_move(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the mouse is clicked, register the player's move
                    self.game.player_move(event)
                    game_info = self.game.get_info()
                    print(
                        f"TURN: {1 - game_info.turn}, 3liners: {game_info.total_three_liners}, stopped: {game_info.block_four_liners}"
                    )

                # Redraw the game board and update the display
                self.game.draw()
                pygame.display.update()

                if self.game.game_over:
                    # If the game is over, wait for 3 seconds and then start a new game
                    pygame.time.wait(3000)
                    self.game.new_game()

    def test_ai(self, net):
        """
        Test the AI against a human player by passing a NEAT neural network
        """
        clock = pygame.time.Clock()
        is_running = True
        while is_running:
            clock.tick(60)
            self.game.draw()  # Drawing the initial state of the game board

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    break

            if self.game.turn == 0:
                if event.type == pygame.MOUSEMOTION:
                    # If the mouse is moved, redraw the player's move
                    self.game.draw_player_move(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the mouse is clicked, register the player's move
                    self.game.player_move(event)
            else:
                flat_board = self.board.flatten()
                output = net.activate((flat_board))
                decision = output.index(max(output))
                self.game.player_ai_move(decision)

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

        while run:
            # self.game.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            if self.game.turn == 0:
                # pygame.time.wait(1000)
                self.game.ai_move(net1, self.game.board)
            else:
                # pygame.time.wait(1000)
                self.game.ai_move(net2, self.game.board)

            game_info = self.game.get_info()

            # pygame.display.update()

            if (
                self.game.game_over
                or game_info.invalid_moves[0] + game_info.invalid_moves[1] > 2
            ):
                self.calculate_fitness(game_info)
                self.game.new_game()

                break

        return False

    def calculate_fitness(self, game_info):
        # print(
        #     f"winner: {game_info.winner}, total_turns: {game_info.total_turns}, 3liners: {game_info.total_three_liners}, 2liners: {game_info.total_two_liners}, block4: {game_info.block_four_liners}, invalid: {game_info.invalid_moves}"
        # )
        self.genome1.fitness += (
            game_info.winner[0]
            + game_info.total_turns / (self.game.ROWS * self.game.COLUMNS / 2) / 42
            + len(game_info.total_three_liners[0])
            + len(game_info.total_two_liners[0]) / 5
            + game_info.block_four_liners[0] * 2
            - game_info.invalid_moves[0]
        )
        self.genome2.fitness += (
            game_info.winner[1]
            + game_info.total_turns / (self.game.ROWS * self.game.COLUMNS / 2) / 42
            + len(game_info.total_three_liners[1])
            + len(game_info.total_two_liners[1]) / 5
            + game_info.block_four_liners[1] * 2
            - game_info.invalid_moves[1]
        )


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(15))

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

            force_quit = game.train_ai(genome1, genome2, config)
            if force_quit:
                quit()


def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    pygame.display.set_caption("Connect4")
    game.test_ai(winner_net)


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
    game = Connect()
    # game.main()

    # train genome
    run_neat(config)

    # test_best_network(config)
