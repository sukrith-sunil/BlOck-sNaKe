import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640*2, 480*2
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BlOck sNaKe")

# Initialize the clock
clock = pygame.time.Clock()

# Snake variables
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = RIGHT
snake_growth = False

# Food variables
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Add a score variable
score = 0

#########################################################################
# Define a file to store high scores
HIGH_SCORE_FILE = "high_score.txt"

def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))
    except Exception as e:
        print(f"Error saving high score: {e}")

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            high_score = int(file.read())
            return high_score
    except FileNotFoundError:
        return 0
    except Exception as e:
        print(f"Error loading high score: {e}")
        return 0
##########################################################################
    


# High score variable
high_score = load_high_score()

# Menu state
MENU = 0
GAME = 1
game_state = MENU  # Initial game state is the menu
HIGH_SCORE_DISPLAY = 2
high_score_state = HIGH_SCORE_DISPLAY
# Menu items and selected index
menu_items = ["New Game", "High Score", "Exit"]
selected_item = 0

def handle_menu_events():
    global selected_item, game_state, high_score_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_item = (selected_item - 1) % len(menu_items)
            elif event.key == pygame.K_DOWN:
                selected_item = (selected_item + 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                if selected_item == 0:
                    start_new_game()
                elif selected_item == 1:
                    # Transition to the high score state
                    high_score_state = HIGH_SCORE_DISPLAY
                elif selected_item == 2:
                    pygame.quit()
                    sys.exit()


def start_new_game():
    global snake, snake_direction, snake_growth, score, food, game_state
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = RIGHT
    snake_growth = False
    score = 0
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    game_state = GAME


def handle_game_events():
    global snake_direction  # Declare snake_direction as global here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != DOWN:
                snake_direction = UP
            elif event.key == pygame.K_DOWN and snake_direction != UP:
                snake_direction = DOWN
            elif event.key == pygame.K_LEFT and snake_direction != RIGHT:
                snake_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake_direction != LEFT:
                snake_direction = RIGHT

def update_game():
    global snake, snake_direction, snake_growth, score, food, game_state

    # Move the snake
    new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])

    # Check for collisions with the walls
    if (
        new_head[0] < 0
        or new_head[0] >= GRID_WIDTH
        or new_head[1] < 0
        or new_head[1] >= GRID_HEIGHT
    ):
        game_state = MENU

    snake.insert(0, new_head)

    # Check for collisions with food
    if snake[0] == food:
        snake_growth = True
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        score += 10

    # Remove the last segment if not growing
    if not snake_growth:
        snake.pop()
    else:
        snake_growth = False

    # Check for collisions with itself
    if snake[0] in snake[1:]:
        game_state = MENU

def draw_game():
    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the food
    pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Display the score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()


#########################################################################
# Define a file to store high scores
HIGH_SCORE_FILE = "high_score.txt"

def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))
    except Exception as e:
        print(f"Error saving high score: {e}")

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            high_score = int(file.read())
            return high_score
    except FileNotFoundError:
        return 0
    except Exception as e:
        print(f"Error loading high score: {e}")
        return 0
##########################################################################
    
# Inside the main game loop:
while True:
    if game_state == MENU:
        handle_menu_events()
        # Clear the screen
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        menu_text = font.render("Snake Game Menu", True, WHITE)
        new_game_text = font.render("New Game", True, WHITE)
        high_score_text = font.render("High Score: " + str(high_score), True, WHITE)  # Display the high score here
        exit_text = font.render("Exit", True, WHITE)
        screen.blit(menu_text, (200, 100))
        screen.blit(new_game_text, (200, 200))
        screen.blit(high_score_text, (200, 250))
        screen.blit(exit_text, (200, 300))
        # Highlight the selected item
        selected_text = font.render(f"> {menu_items[selected_item]}", True, WHITE)
        screen.blit(selected_text, (180, 200 + selected_item * 50))
        pygame.display.flip()
        
    elif game_state == HIGH_SCORE_DISPLAY:
        # Clear the screen
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
        screen.blit(high_score_text, (200, 250))
        pygame.display.flip()
        
        # Handle events to return to the menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = MENU  # Return to the menu

    elif game_state == GAME:
        handle_game_events()
        update_game()
        if score > high_score:
            high_score = score  # Update the high score
            save_high_score(high_score)  # Save the new high score
        draw_game()
        clock.tick(10)
