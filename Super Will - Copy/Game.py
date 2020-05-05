import pygame
import numpy as np

SKY_BLUE = (30,144,255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Level Constructor
class Level():
    def __init__(self):
        super().__init__(self)

    #def build(self):
        

    def update(self):
        self.background.update()
        


class level_01(Level):
    def __init__(self):
        Level.__init__(self)

    def structure(self):
        map ={
        
        
        ________________}    

    
def main():
    print(level_01(Level).structure())
    pygame.init()
    pygame.font.init()

    size = [SCREEN_HEIGHT,SCREEN_WIDTH]
    screen = pygame.display.set_mode(size)
    screen.set_alpha(None)

    pygame.quit()
main()
