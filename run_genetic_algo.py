import pygame
import sys
import bird_logic
import pipe_logic
import genetic_algo
import random
import numpy as np


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

PIPE_MIN_HEIGHT = 50
PIPE_GAP_SIZE = 150
PIPE_INTERVAL = 40
PIPE_WIDTH = 35

BIRD_SIZE = 25

POPULATION_SIZE = 20
MUTATION_RATE = 0.1
GENERATIONS = 100
INPUT_SIZE = 5


def run_generation(population):
    game_loop(population)
    # Sort the population based on fitness
    population.sort(key=lambda brd: brd.survival_time, reverse=True)
    print('blah')
    print([b.survival_time for b in population])
    elite = population[:int(0.2 * POPULATION_SIZE)]
    new_generation = elite.copy()
    # Generate offspring through crossover and mutation
    while len(new_generation) < POPULATION_SIZE:
        parent1 = random.choice(elite)
        parent2 = random.choice(elite)

        # Crossover
        child_network = genetic_algo.NeuralNetwork(
            input_size=len(parent1.neural_net.weights_input_hidden),
            hidden_size=len(parent1.neural_net.weights_hidden_output[0]),
            output_size=1
        )
        crossover_point = random.randint(0, len(parent1.neural_net.weights_input_hidden) - 1)

        # Inherit weights from parents
        #print("child:")
        #print(child_network.weights_input_hidden)
        #print("parent:")
        #print(parent1.neural_net.weights_input_hidden)
        child_network.weights_input_hidden = parent1.neural_net.weights_input_hidden.copy()
        child_network.weights_input_hidden[:crossover_point, :] = parent1.neural_net.weights_input_hidden[:crossover_point, :].copy()
        child_network.weights_input_hidden[crossover_point:, :] = parent2.neural_net.weights_input_hidden[crossover_point:, :].copy()

        crossover_point = random.randint(0, len(parent1.neural_net.weights_hidden_output) - 1)
        child_network.weights_hidden_output = parent1.neural_net.weights_hidden_output.copy()
        child_network.weights_hidden_output[:, :crossover_point] = parent1.neural_net.weights_hidden_output[:, :crossover_point]
        child_network.weights_hidden_output[:, crossover_point:] = parent2.neural_net.weights_hidden_output[:, crossover_point:]

        # Mutation
        for weight_matrix in [child_network.weights_input_hidden, child_network.weights_hidden_output]:
            if random.random() < MUTATION_RATE:
                mutation_indices = np.random.choice(np.arange(weight_matrix.size), size=1)
                mutation_values = np.random.uniform(-0.5, 0.5, size=1)
                np.put(weight_matrix, mutation_indices, mutation_values)
        # Create a new bird with the mutated neural network
        child = bird_logic.Bird(neural_net=child_network, 
                                screen_height=SCREEN_HEIGHT,
                                x=20,
                                y=SCREEN_HEIGHT//2,
                                size=BIRD_SIZE)
        new_generation.append(child)
    return new_generation

#def run_genetic_algo(population):
def run_genetic_algo():
    # inputs: x dist from pipes, y dist from top pipe, y dist from bottom pipe, velocity/acceleration
    hidden_size = 10  # Adjust as needed
    output_size = 1  # Output is binary (flap or not)

    population = [bird_logic.Bird(neural_net=genetic_algo.NeuralNetwork(INPUT_SIZE, 
                                                    hidden_size, 
                                                    output_size), 
                                                    screen_height=SCREEN_HEIGHT,
                                                    x=20,
                                                    y=SCREEN_HEIGHT//2,
                                                    size=BIRD_SIZE) 
                  for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        print(f"Generation {generation + 1}")
        population = run_generation(population)
    # Get the best bird from the final generation
    best_bird = max(population, key=lambda x: x.survival_time)
    print(f"Best bird's fitness: {best_bird.survival_time}")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
def game_loop(birds):
    pygame.display.set_caption("Flappy Bird")

# Set up colors
    black = (0, 0, 0)
    white = (255, 255, 255)

# Set up game loop
    clock = pygame.time.Clock()

    pipe_generator = pipe_logic.PipeGenerator(width=PIPE_WIDTH,
                                              length=400,
                                              speed=10,
                                              starting_x=SCREEN_WIDTH+30,
                                              #interval=PIPE_INTERVAL,
                                              interval=PIPE_INTERVAL,
                                              screen_height=SCREEN_HEIGHT,
                                              gap_size=PIPE_GAP_SIZE)
    ticks = 0
    gap_height = SCREEN_HEIGHT//2
    is_running = True
    num_dead = 0
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # bird.jump()
                    pass
        for bird in birds:
            if len(pipe_generator.pipes) >= 2:
                p1 = pipe_generator.pipes[0]
                p2 = pipe_generator.pipes[1]
                p1x, p1y = bird.get_pipe_dist(p1)
                p2x, p2y = bird.get_pipe_dist(p2)
                bird.jump(p1_y=p1y, p2_y = p2y, p_x = p1x)
            else:
                bird.jump(p1_y=50, p2_y=50, p_x=SCREEN_WIDTH)
            if bird.alive is True:
                bird.step()
        pipe_generator.clean_pipes()
        if ticks == pipe_generator.interval:
            print('interval met')
            gap_height_change = random.randint(-1*SCREEN_HEIGHT//2, SCREEN_HEIGHT//2)
            if gap_height_change > 0:
                # move the height down, but make sure it's still above PIPE_MIN_HEIGHT
                gap_height = min(gap_height + gap_height_change, SCREEN_HEIGHT - PIPE_MIN_HEIGHT - gap_height )
            elif gap_height_change < 0:
                # move the height up, but make sure its still below PIPE_MIN_HEIGHT
                gap_height = max(PIPE_MIN_HEIGHT, gap_height + gap_height_change)
            pipe_generator.generate_pipe_pair(gap_height)
            ticks = 0
        # Drawing code goes here
        screen.fill(black)
        # Draw your game elements here
        #print(pipe_generator.pipes)
        for pipe in pipe_generator.pipes:
            pipe.step()
            pygame.draw.rect(screen, white, (pipe.x, 
                                             pipe.y, 
                                             pipe.width, 
                                             pipe.length))
            for bird in birds:
                bird.check_collision(pipe)
                if bird.alive is False:
                    num_dead += 1
        for bird in birds:
            if bird.alive is True:
                pygame.draw.rect(screen, bird.color, (bird.x, bird.y, bird.size, bird.size))
        if num_dead >= len(birds):
            is_running = False
            return birds
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
        ticks += 1

# Quit Pygame
    pygame.quit()
run_genetic_algo()







