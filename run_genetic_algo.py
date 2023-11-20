import pygame
import sys
import bird_logic
import pipe_logic
import genetic_algo
import random


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

PIPE_MIN_HEIGHT = 50
PIPE_GAP_SIZE = 150
PIPE_INTERVAL = 40
PIPE_WIDTH = 35

BIRD_SIZE = 25

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up game loop
clock = pygame.time.Clock()
is_running = True
bird = bird_logic.Bird(x=20, y=20, size=BIRD_SIZE, screen_height=SCREEN_HEIGHT)

pipe_generator = pipe_logic.PipeGenerator(width=PIPE_WIDTH,
                                          length=400,
                                          speed=10,
                                          starting_x=SCREEN_WIDTH+30,
                                          interval=PIPE_INTERVAL,
                                          screen_height=SCREEN_HEIGHT,
                                          gap_size=PIPE_GAP_SIZE)
ticks = 0
gap_height = SCREEN_HEIGHT//2
def run_generation(population):
    for bird in population:
        # game logic
        bobjones = 3
        pass
    # Sort the population based on fitness
    population.sort(key=lambda brd: brd.x, reverse=True)

    elite = population[:int(0.2 * POPULATION_SIZE)]
    new_generation = elite.copy()

    # Generate offspring through crossover and mutation
    while len(new_generation) < POPULATION_SIZE:
        parent1 = random.choice(elite)
        parent2 = random.choice(elite)

        # Crossover
        child_network = genetic_algo.NeuralNetwork(
            input_size=len(parent1.neural_network.weights_input_hidden),
            hidden_size=len(parent1.neural_network.weights_hidden_output[0]),
            output_size=1
        )
        crossover_point = random.randint(0, len(parent1.neural_network.weights_input_hidden) - 1)

        # Inherit weights from parents
        child_network.weights_input_hidden[:crossover_point, :] = parent1.neural_network.weights_input_hidden[:crossover_point, :]
        child_network.weights_input_hidden[crossover_point:, :] = parent2.neural_network.weights_input_hidden[crossover_point:, :]

        crossover_point = random.randint(0, len(parent1.neural_network.weights_hidden_output) - 1)
        child_network.weights_hidden_output[:, :crossover_point] = parent1.neural_network.weights_hidden_output[:, :crossover_point]
        child_network.weights_hidden_output[:, crossover_point:] = parent2.neural_network.weights_hidden_output[:, crossover_point:]

        # Mutation
        for weight_matrix in [child_network.weights_input_hidden, child_network.weights_hidden_output]:
            if random.random() < MUTATION_RATE:
                mutation_indices = np.random.choice(np.arange(weight_matrix.size), size=1)
                mutation_values = np.random.uniform(-0.5, 0.5, size=1)
                np.put(weight_matrix, mutation_indices, mutation_values)
        # Create a new bird with the mutated neural network
        child = bird_logic.Bird(neural_network=child_network, screen_height=SCREEN_HEIGHT)
        new_generation.append(child)
    return new_generation

def run_genetic_algo(population):
    input_size =  4# Set the size based on your game inputs
    # inputs: x dist from pipes, y dist from top pipe, y dist from bottom pipe, velocity/acceleration
    hidden_size = 10  # Adjust as needed
    output_size = 1  # Output is binary (flap or not)

    population = [Bird(neural_network=NeuralNetwork(input_size, 
                                                    hidden_size, 
                                                    output_size), 
                       screen_height=SCREEN_HEIGHT) 
                  for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        print(f"Generation {generation + 1}")
        population = run_generation(population)
    # Get the best bird from the final generation
    best_bird = max(population, key=lambda x: x.fitness)
    print(f"Best bird's fitness: {best_bird.fitness}")


while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
    pipe_generator.clean_pipes()
    bird.step()
    if ticks == pipe_generator.interval:
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
    pygame.draw.rect(screen, white, (bird.x, bird.y, bird.size, bird.size))
    for pipe in pipe_generator.pipes:
        bird.check_collision(pipe)
        pipe.step()
        pygame.draw.rect(screen, white, (pipe.x, 
                                         pipe.y, 
                                         pipe.width, 
                                         pipe.length))


    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
    ticks += 1

# Quit Pygame
pygame.quit()
sys.exit()

