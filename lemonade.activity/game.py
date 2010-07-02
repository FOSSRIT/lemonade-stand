import sys
import pygame
from pygame.locals import *

#import lemonade

class game:
    font_name = "Vera"
    text_lines = []
    # Resources at the player's disposal.  Fourth resource is money.
    resources = [0, 0, 0, 1000]
    background = None
    font = None
    window = None
    
    def __init__(self):
        # 1200 x 800
        self.window = pygame.display.set_mode((1200, 800))
        self.background = pygame.image.load("images/game.gif")
        self.background = pygame.transform.scale(self.background, (1200, 800))
        pygame.init()
        
    def update_supply(self, supply_number, new_value):
        self.resources[supply_number] = new_value
        
    def modify_supply(self, supply_number, mod_value):
        self.resources[supply_number] += mod_value
    
    def output(self, text = None):
        # Put the background up.
        self.window.blit(self.background, (0,0))
        
        # Display the amount of each resource, starting at 150 pixels.
        self.font = pygame.font.SysFont(self.font_name, 48)
        i = 100
        for item in self.resources[:3]:
            rendered_text = self.font.render(str(item), True, (0,0,0))
            self.window.blit(rendered_text, (1050, i))
            i += 100
        
        # Money shows up on the other side of the screen, at (150, 200)
        self.font = pygame.font.SysFont(self.font_name, 64)
        rendered_text = self.font.render("${0:.2f}".format(self.resources[3] / 100.0), True, (0,0,0))
        self.window.blit(rendered_text, (150, 200))
        
        # Cut the output down to 11 lines, the most we can show.
        if text:
            self.text_lines.append(text)
            while len(self.text_lines) >= 11:
                self.text_lines.pop(0)
        
        # Write out the console statring at 500 pixels
        self.font = pygame.font.SysFont(self.font_name, 36)
        i = 500
        for line in self.text_lines:
            rendered_text = self.font.render(line, True, (255,255,255))
            self.window.blit(rendered_text, (0,i))
            i += 30
        pygame.display.update()
    
    def keypress(self, text):
        self.output(text)
        input_text = ""
        done = False
        while not done:
            for event in pygame.event.get():
                if (event.type == KEYDOWN):
                    key_name = pygame.key.name(event.key)
                    if key_name == "return":
                        done = True
                        break
                        
                    last_line = self.text_lines[len(self.text_lines) - 1]
                    if key_name == "backspace":
                        if len(input_text) > 0:
                            input_text = input_text[:len(input_text) - 1]
                            self.text_lines[len(self.text_lines) - 1] = last_line[:len(last_line) - 1]
                    elif len(key_name) == 1:
                        input_text = input_text + key_name
                        self.text_lines[len(self.text_lines) - 1] = last_line + key_name
                    self.output()
        return input_text

    def take_input(self, text, default = 0):
        in_text = self.keypress(text+" ["+`default`+"]: ")
        if not in_text:
            return default
        else:
            try:
                in_text = int(in_text)
                if in_text < 0:
                    self.output("Entered text should be positive.  Please try again.")
                    return take_input(text, default)
            except ValueError:
                self.output("Entered text is not a whole number.  Please try again.")
                return take_input(text, default)
            else:
                return in_text
