import pygame
import time

clock = pygame.time.Clock()

class StartMenu:
    def __init__(self) -> None:
        """
        Initialize the StartMenu object with default settings.
        """
        self.screen_width = 750
        self.screen_height = 450
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.num_ants = ''
        self.speed = ''
        self.initialize_start_menu()
        self.game_state = "start_menu"
        # # Cursor variables
        # self.ants_cursor = 0
        self.ants_box_active = False
        # self.speed_cursor = 0 
        self.speed_box_active = False



    def initialize_start_menu(self):
        """
        Initialize fonts, texts, and other elements for the start menu.
        """
         # initialize font and size (for header and Start button)
        self.font = pygame.font.SysFont('Impact', 40)
        self.title = self.font.render('Ant Search Simulation', True, (0, 255, 0)) # title in green
        self.start_button = self.font.render('Start', True, (255, 255, 255)) # start button in white
        self.start_button_rect = self.start_button.get_rect(center=(self.screen_width/2, self.screen_height - 80)) # invisible rectangle to hover over and click start button
                
        # smaller font size
        self.settings_font = pygame.font.SysFont('Impact', 25)
        self.ants_text = self.settings_font.render('Number of Ants', True, (255, 255, 255)) # heading of the ants input box
        self.speed_text = self.settings_font.render('Speed', True, (255, 255, 255)) # heading of the speed input 

        # font for the text in the input box
        self.textbox_font = pygame.font.SysFont('Arial', min(25, int(0.8 * self.ants_text.get_height())))

        self.value_range_font = pygame.font.SysFont('Arial', 15)
        self.value_range_ants = self.value_range_font.render('Please select a value between 0 and 5000', True, (255, 255, 255))
        self.value_range_speed = self.value_range_font.render('Please select a float value between 0.1 and 3', True, (255, 255, 255))



    def draw(self):
        """
        Draw the start menu on the screen.
        """
        self.screen.fill((0, 0, 0)) # background black
       
        mouse_x, mouse_y = pygame.mouse.get_pos() 
        start_button_hovered = self.start_button_rect.collidepoint(mouse_x, mouse_y) # if mouse is hovering over the Start button

        # Change the color of the Start button based on mouse hover
        if start_button_hovered:
            self.start_button = self.font.render('Start', True, (0, 255, 0)) # make it green
        else:
            self.start_button = self.font.render('Start', True, (255, 255, 255)) # leave it white

        # draw title, start button and heading of the input box
        self.screen.blit(self.title, (self.screen_width/2 - self.title.get_width()/2, self.screen_height - (self.screen_height - 50)))
        self.screen.blit(self.start_button, (self.screen_width/2 - self.start_button.get_width()/2, self.screen_height - 100))
        self.screen.blit(self.ants_text, (self.screen_width/2 - self.ants_text.get_width()/2, self.screen_height - 320))
        self.screen.blit(self.speed_text,(self.screen_width/2 - self.speed_text.get_width()/2, self.screen_height - 230))

        white_text = (255,255,255)
    
        # input box for the user to type in the number of ants
        self.ants_box = pygame.Rect(self.screen_width / 2 - self.ants_text.get_width() / 2, self.screen_height - 270, self.ants_text.get_width(), self.ants_text.get_height())

        # input box for the speed of the ants
        self.speed_box = pygame.Rect(self.screen_width / 2 - self.ants_text.get_width() / 2, self.screen_height - 180, self.ants_text.get_width(), self.ants_text.get_height())

        # text cursor for both input boxes
        self.ants_cursor = pygame.Rect(0, 0, 2, int(0.75 * self.ants_text.get_height()))
        self.speed_cursor = pygame.Rect(0, 0, 2, int(0.75 * self.speed_text.get_height()))

        pygame.draw.rect(self.screen, white_text, self.ants_box, 2)         
        text_surface_ants = self.textbox_font.render(self.num_ants, True, white_text)
        width = max(200, text_surface_ants.get_width()+10)
        self.ants_box.w = width

        # if user has clicked on the input box 
        if self.ants_box_active:
            # cursor gets placed at the right side of the input
            self.ants_cursor.topleft = (self.ants_box.x + self.ants_text.get_width() / 2 + text_surface_ants.get_width() / 2, self.ants_box.y + 5)

            # cursor blinks
            if time.time() % 1 > 0.5:
                pygame.draw.rect(self.screen, (255, 255, 255), self.ants_cursor)


        pygame.draw.rect(self.screen, white_text, self.speed_box, 2)
        text_surface_speed = self.textbox_font.render(self.speed, True, white_text)
        width = max(200, text_surface_speed.get_width()+10)
        self.speed_box.w = width

        # if user has clicked on the speed input box 
        if self.speed_box_active:
            # cursor gets placed at the right side of the input
            self.speed_cursor.topleft = (self.ants_box.x + self.ants_text.get_width() / 2 + text_surface_speed.get_width() / 2, self.speed_box.y + 5)

            # cursor blinks
            if time.time() % 1 > 0.5:
                pygame.draw.rect(self.screen, (255, 255, 255), self.speed_cursor)

        # Center the text horizontally within the box
        ants_text_x = self.ants_box.x + ((self.ants_box.width - text_surface_ants.get_width()) // 2) - 20
        ants_text_y = self.ants_box.y + (self.ants_box.height - text_surface_ants.get_height()) // 2
        
        speed_text_x = self.ants_box.x + ((self.speed_box.width - text_surface_speed.get_width()) // 2) - 20
        speed_text_y = self.speed_box.y + (self.speed_box.height - text_surface_speed.get_height()) // 2

        # print the input 
        self.screen.blit(text_surface_ants, (ants_text_x, ants_text_y))
        self.screen.blit(text_surface_speed,(speed_text_x, speed_text_y))

        # Draw the value range information
        self.screen.blit(self.value_range_ants, (self.screen_width / 2 - self.value_range_ants.get_width() / 2, self.screen_height - 290))
        self.screen.blit(self.value_range_speed, (self.screen_width / 2 - self.value_range_speed.get_width() / 2, self.screen_height - 200))

        pygame.display.update()


    def handle_events(self):
        """
        Handle events such as key presses and mouse clicks.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                # if the number of ants input box is selected
                if self.ants_box_active: 
                    # delete input with Backspace or Delete
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        self.num_ants = self.num_ants[:-1]
                    else:
                        # update the variable with the given input
                        self.num_ants += event.unicode
        
                # if the speed input box is selected
                elif self.speed_box_active:
                    # delete input with Backspace or Delete
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        self.speed = self.speed[:-1]
                    else:
                        # update the variable with the given input
                        self.speed += event.unicode


            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # activate input box for number of ants when it's selected by the user
                if self.ants_box.collidepoint(event.pos):
                    self.ants_box_active = True
                else:
                    self.ants_box_active = False

                # activate input box for speed value when it's selected
                if self.speed_box.collidepoint(event.pos):
                    self.speed_box_active = True
                else:
                    self.speed_box_active = False

                if self.start_button_rect.collidepoint(event.pos):
                    print(f"Number of Ants: {int(self.num_ants)}")
                    print(f"Speed: {self.speed}")
                    self.game_state = "Simulation"


def main():
    """
    Main function to run the simulation.
    """
    pygame.init()
    start_menu = StartMenu()

    while True:
        start_menu.handle_events()
        start_menu.draw()

if __name__ == "__main__":
    main()   
