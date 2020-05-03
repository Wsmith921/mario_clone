# Building from the player up

import pygame
import configparser as con
import numpy as np

# Test Learning
SKY_BLUE = (30,144,255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# To scale the whole game
scale = SCREEN_WIDTH//16


# Sets screen size

size = [SCREEN_WIDTH,SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

# Reads the Text level document

class Structure():
    def __init__(self):
        super().__init__()
        parser = con.ConfigParser()
        self.filename = "level.map"
        parser.read(self.filename)
        self.list_obj = parser.get("level 1", "map").split("\n")
        self.num = []
        # List of things the level needs to be aware of that exist.
        self.objects = []

        for i in range(len(self.list_obj)):
            self.num.append([])
            for j in self.list_obj[i]:
                a = parser.get(j,"name")
                self.num[i].append(a)
                if a not in self.objects:
                    self.objects.append(a)
        self.objects.remove("air")
        self.obj = np.array(self.num[::-1]) # Need to reverse order to properly draw

        #self.dict = {
        #    "bricks":Bricks(),
        #    "ground":Ground(),
         #   "coin": Coin()
        #    }
            
        

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        
        # Create image of block.
        self.right_images = []
        self.left_images = []
        self.jump_images = []
        stand = pygame.image.load("sprite_0.png").convert()
        image1 = pygame.image.load("sprite_1.png").convert()
        image2 = pygame.image.load("sprite_2.png").convert()
        image3 = pygame.image.load("sprite_3.png").convert()
        image4 = pygame.image.load("sprite_4.png").convert()
        self.right_images.extend([stand,image1,image2,image3])
        

        standf = pygame.image.load("flip_0.png").convert()
        image1f = pygame.image.load("flip_1.png").convert()
        image2f = pygame.image.load("flip_2.png").convert()
        image3f = pygame.image.load("flip_3.png").convert()
        image4f = pygame.image.load("flip_4.png").convert()
        print(image4f.get_at((0,0)))
        self.left_images.extend([standf,image1f,image2f,image3f])

        self.jump_images.extend([image4,image4f])
        self.jump_images[0] = pygame.transform.scale(self.jump_images[0],(scale,scale))
        self.jump_images[0].set_colorkey(WHITE)
        self.jump_images[1] = pygame.transform.scale(self.jump_images[1],(scale,scale))
        self.jump_images[1].set_colorkey(WHITE)

        for i in range(len(self.right_images)):
            self.right_images[i] = pygame.transform.scale(self.right_images[i],(scale,scale))
            self.left_images[i] = pygame.transform.scale(self.left_images[i],(scale,scale))
            self.right_images[i].set_colorkey(WHITE)
            self.left_images[i].set_colorkey(WHITE)
            self.right_images[i].set_alpha(255)
            self.left_images[i].set_alpha(255)
            
        self.image = self.right_images[0]
        self.rect = self.image.get_rect()

        # Speed vectors for the player
        self.change_x = 0
        self.change_y = 0

        # List of Sprites we can bump against
        self.level = None
        
        # Animation Index
        self.index = 0

        # To slow the animation down
        self.time = 0

        self.direct = "right"

    # For moving the player
    def update(self):
        # Animation
        self.time += 1
        if self.time % 8 == 0:
            if self.change_x == 0:
                if self.direct == "right":
                    self.image = self.right_images[0]
                elif self.direct == "left":
                    self.image = self.left_images[0]
            
            elif self.change_x > 0:
                self.direct = "right"
                self.index += 1
                if self.index >= len(self.right_images):
                    self.index = 1
                self.image = self.right_images[self.index]
            elif self.change_x < 0:
                self.direct = "left"
                self.index += 1
                if self.index >= len(self.left_images):
                    self.index = 1
                self.image = self.left_images[self.index]

            if self.change_y != 0:
                if self.direct == "right":
                    self.image = self.jump_images[0]
                elif self.direct == "left":
                    self.image = self.jump_images[1]
                    

            
            
        


        
        # Gravity
        self.calc_grav()
        # Move left/right
        self.rect.x += int(self.change_x)

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        # Sprite collide finds sprites in a group that intersect another sprite
        # Returns a list of all sprites in a group that intersect with another Sprite
        # spritecollide(sprite, group, dokill, collided = None)

        for block in block_hit_list:
            # If we move right
            # Set our right side equal to the left side of the item we hit.
            if self.change_x > 0:
                self.rect.right = block.rect.left
            # If we move left, do the opposite
            elif self.change_x < 0:
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
        # Calculate the effects of gravity
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        # See if we are on the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        # Called when the player jumps
        # move down to see if there is a platform under us
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
    # Player Controlled movement
    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6
    def stop(self):
        self.change_x = 0
        



class Bricks(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("brick_block.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.rect = self.image.get_rect()

    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "bricks")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        #b[:][-1] = SCREEN_HEIGHT - scale - (b[:][-1])
        return b
    

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ground_block.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.rect = self.image.get_rect()
        self.b = []
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "ground")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b


class Level(object):
    def __init__(self, player):
        # We need to pass in the player to handle collisions with platforms
        #super().__init__()
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # How far world has shifted
        self.world_shift = 0
        
        # Background image
        self.background = None

    # Need to update everything on this level
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def shift_world(self, shift_x):
    # Scrolls the screen

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

    def draw(self, screen):
        # Draw everything on this level

        # Draw the background
        screen.fill(SKY_BLUE)

        # Draw all the sprite lists that we have
        for plat in self.platform_list:
            if plat.rect.x < 800:
                screen.blit(plat.image,[plat.rect.x, plat.rect.y])
        #self.enemy_list.draw(screen)



class Level_01(Level):
    def __init__(self, player):

        Level.__init__(self, player)

        
        # Positions of all the given blocks in the Level
        bricks = Bricks().pos()
        ground = Ground().pos()
        
        for b in bricks:
            block = Bricks()
            block.rect.x = b[0]
            block.rect.y = b[1]
            block.player = self.player
            self.platform_list.add(block)


        ground = Ground().pos()

        for g in ground:
            block1 = Ground()
            block1.rect.x = g[0]
            block1.rect.y = g[1]
            block1.player = self.player
            self.platform_list.add(block1)
        
    

    



        


def main():
    pygame.init()
    
    player = Player()
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    active_sprite_list.add(player)
    

    a = True
    clock = pygame.time.Clock()
    while a == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= SCREEN_WIDTH - 300:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)

        active_sprite_list.update()
        # Update items in the level
        current_level.update()
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

if __name__== "__main__":
    main()



        
