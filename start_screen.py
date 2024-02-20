import pygame


class StartMenu:
    def __init__(self) -> None:
        self.screen_width = 750
        self.screen_height = 450
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.num_ants = ''
        self.initialize_start_menu()
        self.game_state = "start_menu"


    def initialize_start_menu(self):
         # initialize font and size (for header and Start button)
        self.font = pygame.font.SysFont('Impact', 40)
        self.title = self.font.render('Ant Search Simulation', True, (0, 255, 0)) # title in green
        self.start_button = self.font.render('Start', True, (255, 255, 255)) # start button in white
        self.start_button_rect = self.start_button.get_rect(center=(self.screen_width/2, self.screen_height - 80)) # invisible rectangle to hover over and click start button
                
        # smaller font size
        self.settings_font = pygame.font.SysFont('Impact', 25)
        self.ants_text = self.settings_font.render('Number of Ants', True, (255, 255, 255)) # heading of the input box

        # font for the text in the input box
        self.textbox_font = pygame.font.SysFont('Arial', min(25, int(0.8 * self.ants_text.get_height())))
        
       

    def draw(self):
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
        self.screen.blit(self.ants_text, (self.screen_width/2 - self.ants_text.get_width()/2, self.screen_height - 230))

        white_text = (255,255,255)
       
        # input box for the user to type in the number of ants
        self.ants_box = pygame.Rect(self.screen_width / 2 - self.ants_text.get_width() / 2, self.screen_height - 200, self.ants_text.get_width(), self.ants_text.get_height())

        pygame.draw.rect(self.screen, white_text, self.ants_box, 2)
        text_surface = self.textbox_font.render(self.num_ants, True, white_text)
        width = max(200, text_surface.get_width()+10)
        self.ants_box.w = width

        # Center the text horizontally within the box
        text_x = self.ants_box.x + ((self.ants_box.width - text_surface.get_width()) // 2) - 20
        text_y = self.ants_box.y + (self.ants_box.height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))

        pygame.display.update()

    def handle_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_RETURN:
                        try:
                            # Convert the input_text to an integer
                            self.num_ants = int(self.num_ants)
                            print(f"Number of Ants: {self.num_ants}")
                        except ValueError:
                            print("Please enter a valid number.")
                        self.num_ants = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.num_ants = self.num_ants[:-1]
                    else:
                        self.num_ants += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.start_button_rect.collidepoint(event.pos):
                        print(f"Number of Ants: {int(self.num_ants)}")
                        self.game_state = "Simulation"


def main():
    pygame.init()
    start_menu = StartMenu()

    while True:
        start_menu.handle_events()
        start_menu.draw()    

if __name__ == "__main__":
    main()   