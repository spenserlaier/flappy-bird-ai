import pygame
import sys
import bird_logic
import pipe_logic
import random


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up game loop
clock = pygame.time.Clock()
is_running = True
bird = bird_logic.Bird(x=20, y=20, size=25)

pipe_generator = pipe_logic.PipeGenerator(width=20,
                                          length=400,
                                          speed=10,
                                          starting_x=SCREEN_WIDTH+30,
                                          interval=30,
                                          screen_height=SCREEN_HEIGHT)
ticks = 0
reverse_pipe = False
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
        reverse_pipe = not reverse_pipe
        pipe_height = random.randint(40, SCREEN_HEIGHT-40)
        pipe_generator.generate_pipe_pair(pipe_height)
        ticks = 0



    # Drawing code goes here
    screen.fill(black)
    # Draw your game elements here
    pygame.draw.rect(screen, white, (bird.x, bird.y, bird.size, bird.size))
    for pipe in pipe_generator.pipes:
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
