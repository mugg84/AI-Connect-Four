import pygame
import neat
import pickle
import main


# Create and initialize a NEAT population and run the genetic algorithm
def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(50))

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
            game = main.Connect()

            force_quit = game.train_ai(genome1, genome2, config)
            if force_quit:
                quit()
