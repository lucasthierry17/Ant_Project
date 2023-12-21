import pygame
import sys
import random

def initialize_game():
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # sets up the screen
    pygame.display.set_caption("Food Sources")

    font = pygame.font.Font(None, 36)
    text = font.render("nest", True, (255, 255, 255)) # white Text

    nest_rect = pygame.Rect((100, 30, 50, 50))
    fixed_food_sources = 3
    fixed_food_rects = [pygame.Rect(random.randint(50, 750), random.randint(50, 550), 30, 30) for i in range(fixed_food_sources)]
    random_food_sources = []

    return screen, text, nest_rect, fixed_food_rects, random_food_sources

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # for the exit
            return False
    return True

def update_game_state(random_food_sources):
    current_time = pygame.time.get_ticks()

    for food_source in random_food_sources:
        elapsed_time = current_time - food_source["start_time"]
        food_source["size"] = max(15 - elapsed_time // 100, 0)

    # Add a new random food source every 20 seconds
    if current_time % 20000 == 0:
        random_food_sources.append({"position": (random.randint(25, 750), random.randint(25, 550)),
                                    "start_time": current_time,
                                    "size": 15})


def render_display(screen, text, nest_rect, fixed_food_rects, random_food_sources):
    screen.fill((0, 0, 0)) # fills the screen in black 

    # Draw the nest
    pygame.draw.rect(screen, (255, 0, 0), nest_rect)

    # Draw the fixed food sources
    for food_rect in fixed_food_rects:
        pygame.draw.circle(screen, (144, 238, 144), food_rect.center, 15)

    # Draw the random food sources
    for food_source in random_food_sources:
        pygame.draw.circle(screen, (0, 0, 255), food_source["position"], food_source["size"])

    # Center the text inside the nest
    text_rect = text.get_rect(center=nest_rect.center)

    # Blit the text surface onto the screen
    screen.blit(text, text_rect)

    pygame.display.flip()

def main():
    screen, text, nest_rect, fixed_food_rects, random_food_sources = initialize_game()

    run = True
    while run:
        run = handle_events()
        update_game_state(random_food_sources)
        render_display(screen, text, nest_rect, fixed_food_rects, random_food_sources)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
