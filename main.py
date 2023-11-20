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
