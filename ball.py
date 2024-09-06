import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Controlled Ball with Continuous Moving Obstacles')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Ball properties
ball_pos = [width // 2, height // 2]
ball_vel = [0, 0]  # initial velocity
ball_radius = 20
ball_speed = 5

# Block properties
block_width = 100
block_height = 20
blocks = []

# Background properties
background_scroll = 0
background_speed = 2

# Scoring
score = 0
high_score = 0
score_increment = 1

# Load high score from file
high_score_file = "high_score.txt"
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as file:
        high_score = int(file.read())

# Main loop
running = True
game_over = False
clock = pygame.time.Clock()
block_timer = 0

def display_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render('Game Over', True, red)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds

def save_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        with open(high_score_file, "w") as file:
            file.write(str(high_score))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ball_vel[0] = -ball_speed
        elif keys[pygame.K_RIGHT]:
            ball_vel[0] = ball_speed
        else:
            ball_vel[0] = 0

        if keys[pygame.K_UP]:
            ball_vel[1] = -ball_speed
        elif keys[pygame.K_DOWN]:
            ball_vel[1] = ball_speed
        else:
            ball_vel[1] = 0

        # Move the ball
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        # Scroll the background
        background_scroll += background_speed

        # Generate new blocks periodically
        block_timer += 1
        if block_timer > 60:  # Adjust this value to change block generation frequency
            block_x = width
            block_y = random.randint(0, height - block_height)
            blocks.append(pygame.Rect(block_x, block_y, block_width, block_height))
            block_timer = 0

        # Move the blocks with the background scroll
        for block in blocks:
            block.x -= background_speed

        # Remove blocks that are out of the screen
        blocks = [block for block in blocks if block.right > 0]

        # Collision with blocks
        ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)
        for block in blocks:
            if ball_rect.colliderect(block):
                game_over = True
                display_game_over()
                save_high_score(score)

        # Fill the screen with white
        screen.fill(white)

        # Draw the blocks
        for block in blocks:
            pygame.draw.rect(screen, blue, block)

        # Draw the ball
        pygame.draw.circle(screen, red, ball_pos, ball_radius)

        # Increment and display score
        score += score_increment
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, black)
        screen.blit(score_text, (10, 10))

        # Display high score
        high_score_text = font.render(f'High Score: {high_score}', True, black)
        screen.blit(high_score_text, (width - 200, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
