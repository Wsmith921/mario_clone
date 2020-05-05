import pygame
import configparser as con
import numpy as np

# Test Learning
SKY_BLUE = (30,144,255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# To scale the whole game
scale = SCREEN_WIDTH//16


# Accesses level.map document
parser = con.ConfigParser()

size = [SCREEN_WIDTH,SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)




class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += int(self.change_y)
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

        
        

class Bricks(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("brick_block.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.b = None
    def pos(self, filename):
        a = Level_01(filename).obj
        self.b = np.array((np.where(a == "bricks")))
        print(self.b)
        self.b = np.flip(self.b, 0)
        #print(self.b)

        #print(self.b)
        self.b = np.transpose(self.b)
    
class Level():
    def __init__(self):
        self.structure = pygame.sprite.Group()

        self.background = None

    def draw(self, screen):
        screen.fill(SKY_BLUE)
        screen.blit(self.structure,(scale,scale))

class Level_01():
    def __init__(self, filename):
        super().__init__()
        end = 190*scale
        self.level_limit = -end
        self.filename = filename
    # Reads through the map document
        parser.read(self.filename)
    # Splits the level map into a list of strings, each new string starting on
    # a new line
        self.a = parser.get("level 1", "map").split("\n")
        self.num = []
        # Empty list for appending the name of each object in the levels structure
        # Iterating through each level of objects in each Level
        for i in range(len(self.a)):
            # Appends a list object for each level of objects in each Level
            self.num.append([])
            # Iterates through each object in each level
            for j in self.a[i]:
                # Appends the name of each object in each level of each Level
                self.num[i].append(parser.get(j,"name"))
        self.obj = np.array(self.num[::-1])


    def draw(self):
        dum = []
        
        a = Bricks(100,100)
        b = a.pos(self.filename)
        print(a.image)
        a.b = a.b*scale
        for i in a.b:
            i = i.tolist()
            i[-1]= SCREEN_HEIGHT - scale - i[-1]
            screen.blit(a.image, i)
            print(i)

        c = Ground(100,100)
        d = c.pos(self.filename)
        for i in c.b:
            i = i*scale
            i = i.tolist()
            i[-1]= SCREEN_HEIGHT - scale - i[-1]
            screen.blit(c.image, i)

        
    
    
        

        
              
    
        


    


def draw(background, bricks):
    for i in bricks:
        screen.blit(background, [bricks.rect.x, bricks.rect.y])

class Ground(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ground_block.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.b = None
    def pos(self, filename):
        a = Level_01(filename).obj
        self.b = np.array((np.where(a == "ground")))
        #print(self.b)
        self.b = np.flip(self.b, 0)
        #print(self.b)

        #print(self.b)
        self.b = np.transpose(self.b)
    


def draw(background, bricks):
    for i in bricks:
        screen.blit(background, [bricks.rect.x, bricks.rect.y])


def main():
    pygame.init()
    pygame.font.init()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(SKY_BLUE)
    screen.fill(SKY_BLUE)
    screen.set_alpha(None)
    pygame.display.update()
    filename = "level.map"
    Level_01(filename).draw()
    pygame.display.update()

if __name__ == "__main__":
    main()
