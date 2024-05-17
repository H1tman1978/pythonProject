import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Get display information
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bird settings
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
BIRD_X = SCREEN_WIDTH // 4
BIRD_Y = SCREEN_HEIGHT // 2
GRAVITY = 0.15
FLAP_STRENGTH = -4

# Pipe settings
PIPE_WIDTH = 50
PIPE_HEIGHT = 400
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # Milliseconds

# Set up the display in full screen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Flappy Bird Clone')

# Load bird image
bird_img = pygame.image.load('bird.png')
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))

# Load pipe image
pipe_img = pygame.image.load('pipe.png')
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, PIPE_HEIGHT))

# Font for scoring
font = pygame.font.Font(None, 36)


def main():
    clock = pygame.time.Clock()
    running = True

    bird_y = BIRD_Y
    bird_velocity = 0

    pipes = []
    last_pipe = pygame.time.get_ticks()
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = FLAP_STRENGTH

        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Add pipes
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > PIPE_FREQUENCY:
            pipe_y = random.randint(-PIPE_HEIGHT + 100, 0)
            pipes.append(pygame.Rect(SCREEN_WIDTH, pipe_y, PIPE_WIDTH, PIPE_HEIGHT))
            pipes.append(pygame.Rect(SCREEN_WIDTH, pipe_y + PIPE_HEIGHT + PIPE_GAP, PIPE_WIDTH, PIPE_HEIGHT))
            last_pipe = current_time

        # Move pipes
        for pipe in pipes:
            pipe.x -= 2

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

        # Check for collisions
        bird_rect = pygame.Rect(BIRD_X, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                running = False

        # Check for scoring
        for pipe in pipes:
            if pipe.x == BIRD_X:
                score += 0.5  # Since we have two pipes per gap, we increment by 0.5

        screen.fill(WHITE)  # Clear the screen
        screen.blit(bird_img, (BIRD_X, bird_y))  # Draw the bird

        for pipe in pipes:
            screen.blit(pipe_img, pipe.topleft)  # Draw the pipes

        # Draw score
        score_text = font.render(f"Score: {int(score)}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Maintain 60 frames per second

    # Game over screen
    game_over_text = font.render("Game Over", True, BLACK)
    score_text = font.render(f"Final Score: {int(score)}", True, BLACK)
    screen.blit(game_over_text, (
    SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text,
                (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()))
    pygame.display.flip()
    pygame.time.wait(3000)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
