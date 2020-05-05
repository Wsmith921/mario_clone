# Will's Super Mario Game

import pygame

SKY_BLUE = (30,144,255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600




class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Calls the parent constructor
        super().__init__()

        ground = Ground()
        # Create image of block.
        self.images = []
        stand = pygame.image.load("sprite_0.png").convert()
        stand = pygame.transform.scale(stand, (ground.width,ground.height))
        image1 = pygame.image.load("sprite_1.png").convert()
        image1 = pygame.transform.scale(image1, (ground.width,ground.height))
        image2 = pygame.image.load("sprite_2.png").convert()
        image2 = pygame.transform.scale(image2, (ground.width,ground.height))
        image3 = pygame.image.load("sprite_3.png").convert()
        image3 = pygame.transform.scale(image3, (ground.width,ground.height))
        image4 = pygame.image.load("sprite_4.png").convert()
        image4 = pygame.transform.scale(image4, (ground.width,ground.height))
        self.images.append(stand)
        self.images.append(image1)
        self.images.append(image2)
        self.images.append(image3)
        self.images.append(image4)

        standf = pygame.image.load("flip_0.png").convert()
        standf = pygame.transform.scale(standf, (ground.width,ground.height))
        image1f = pygame.image.load("flip_1.png").convert()
        image1f = pygame.transform.scale(image1f, (ground.width,ground.height))
        image2f = pygame.image.load("flip_2.png").convert()
        image2f = pygame.transform.scale(image2f, (ground.width,ground.height))
        image3f = pygame.image.load("flip_3.png").convert()
        image3f = pygame.transform.scale(image3f, (ground.width,ground.height))
        image4f = pygame.image.load("flip_4.png").convert()
        image4f = pygame.transform.scale(image4f, (ground.width,ground.height))
        self.images.append(standf)
        self.images.append(image1f)
        self.images.append(image2f)
        self.images.append(image3f)
        self.images.append(image4f)

        
        

        for i in self.images:
            i.set_colorkey(WHITE)

        self.index = 0
        self.empty = [0]
        self.time = 0

        self.image = self.images[self.index]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None


    def update(self):
        if self.change_x == 0:
            for i in self.empty:
                if i == 0:
                    self.image = self.images[0]
                elif i == 1:
                    self.image = self.images[5]
        if self.change_y != 0:
            for i in self.empty:
                if i == 0:
                    self.image = self.images[4]
                elif i == 1:
                    self.image = self.images[9]
        self.time += 1
        if self.time % 8 == 0:
            self.index += 1
            if self.change_x > 0 and self.change_y == 0:
                if self.index > (len(self.images)-7):
                    self.index = 1
                self.image = self.images[self.index]
            if self.change_x < 0 and self.change_y == 0:
                if self.index > (len(self.images)-2):
                    self.index = 6
                self.image = self.images[self.index]
        self.calc_grav()
        if self.rect.y >= SCREEN_HEIGHT:
            self.die()
        self.goomba()
        self.koopa()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            dif = self.rect.right - block.rect.left
            # If we are moving right, set our right side to the left side of the
            # item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise we are moving left, do the opposite.
                self.rect.left = block.rect.right
            

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            a = str(block)
            # Reset our position based on the top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                if a == "<Pow sprite(in 1 groups)>" :
                    if block.images == block.images2:
                        Sounds().coin.play()
                    else:
                        Sounds().bump.play()
                    for i in range(len(block.images)):
                        block.images[i] = Blank().image
                    
                else:
                    Sounds().bump.play()
                self.rect.top = block.rect.bottom
                

            # Stop our vertical movement
            self.change_y = 0
            
    
    def calc_grav(self):
        # Calculate the effect of gravity
        if self.change_y == 0:
            self.change_y = 2
        else:
            self.change_y += 0.50



    def jump(self):
        # Called when user hits 'jump' button
        # Move down a bit and see if there is a platform below us.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2 # Subtracts 2 from self.rect.y

        

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -15

    # Player-controlled movement:
    def go_left(self):
        # Called when the user hits the left arrow.
        self.change_x = -6
        self.index = 7
        self.empty.append(1)

    def go_right(self):
        # Called when the user hits the right arrow.
        self.change_x = 6
        self.empty.append(0)

    def stop(self):
        # Called when the user lets off the keyboard
        self.change_x = 0

    def die(self):
        # I die
        pygame.mixer.music.stop()
        Sounds().death.play()
        self.kill()
           

    def goomba(self):
        goomba = pygame.sprite.spritecollide(self, self.level.enemy_list[0], False)
        for block in goomba:
            dif = self.rect.bottom - block.rect.top
            right = self.rect.right - block.rect.left
            left = self.rect.left - block.rect.right
            
            if dif <= 7:
                self.change_y = -6
                Sounds().stomp.play()
                block.kill()
            elif right <= 7 or left <= 7:
                self.die()
    def koopa(self):
        koopa = pygame.sprite.spritecollide(self, self.level.enemy_list[1], False)
        for block in koopa:
            dif = self.rect.bottom - block.rect.top
            right = self.rect.right - block.rect.left
            left = self.rect.left - block.rect.right
            
            if dif <= 7:
                self.change_y = -6
                Sounds().stomp.play()
                block.kill()
            elif right <= 7 or left <= 7:
                self.die()
           

            
            

class Ground(pygame.sprite.Sprite):
    # Ground Bricks
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ground_block.jpg").convert()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (width//5,height//5))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.width:
            self.kill()

class Bricks(pygame.sprite.Sprite):
    # Bricks for the platform
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("platform-brick.png").convert()
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width,self.ground.height))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width:
            self.kill()

class Pow(pygame.sprite.Sprite):
    # Power blocks in super mario
    def __init__(self):
        super().__init__()
        self.images = []
        self.images2 = []
        self.ground = Ground()
        self.image1 = pygame.image.load("platform-q.png")
        self.image2 = pygame.image.load("platform-q1.png")
        self.image3 = pygame.image.load("platform-q2.png")
        self.image4 = pygame.image.load("platform-q3.png")
        self.image1 = pygame.transform.scale(self.image1, (self.ground.width,self.ground.height))
        self.image2 = pygame.transform.scale(self.image2, (self.ground.width,self.ground.height))
        self.image3 = pygame.transform.scale(self.image3, (self.ground.width,self.ground.height))
        self.image4 = pygame.transform.scale(self.image4, (self.ground.width,self.ground.height))
        self.images.append(self.image1)
        self.images.append(self.image2)
        self.images.append(self.image3)
        self.images.append(self.image4)
        self.images2.append(self.image1)
        self.images2.append(self.image2)
        self.images2.append(self.image3)
        self.images2.append(self.image4)
        self.time = 0        

        self.index = 0
        for i in range(len(self.images)):
            if self.images[i] != Blank().image:
                self.image = self.images[self.index]
            else:
                self.images[i] = Blank().image
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(0,2)
        player = None
        level = None
        
    def update(self):
        if self.rect.x < -self.ground.width:
            self.kill()
        self.time += 1
        if self.time % 15 == 0:
                self.index += 1
                if self.index > (len(self.images)-1):
                    self.index = 0
                self.image = self.images[self.index]

        
        
            
                
class Blank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ground = Ground()
        self.image = pygame.image.load("platform-air.png").convert()
        self.image = pygame.transform.scale(self.image, (self.ground.width,self.ground.height))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width:
            self.kill()

        



        
class Metal_Blocks(pygame.sprite.Sprite):
    # Makes the Metal Block
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("metal_block.png")
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width,self.ground.height))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width:
            self.kill()

class Small_Pipes(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("small_green_pipe.png")
        self.image.set_colorkey(WHITE)
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width*2,self.ground.height*2))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width*2:
            self.kill()

class Medium_Pipes(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pipe_green.png")
        self.image.set_colorkey(WHITE)
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width*2,self.ground.height*3))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width*2:
            self.kill()

class Large_Pipes(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pipe_greenbig.png")
        self.image.set_colorkey(WHITE)
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width*2,self.ground.height*4))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width*2:
            self.kill()

class Flag_Pole(pygame.sprite.Sprite):
    # Flag Pole at the end of the level
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("flagpole.png")
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width,self.ground.height*11))
        self.rect = self.image.get_rect()


class Small_Bushes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bush-3.png")
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width*3,self.ground.height))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width*3:
            self.kill()
            
class Medium_Bushes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bush-2.png")
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width*4,self.ground.height))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width*4:
            self.kill()

class Large_Bushes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bush-1.png")
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width*5,self.ground.height))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width*5:
            self.kill()

class Small_Hills(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("hill2.png")
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width*3,self.ground.height))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width*3:
            self.kill()

class Large_Hills(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("hill.png")
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width*5,self.ground.height*2))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width*5:
            self.kill()

class Clouds(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cloud.png")
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width*2,self.ground.height))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width*2:
            self.kill()

class Large_Clouds(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("dobbelclouds.png")
        self.ground = Ground()
        self.image = pygame.transform.scale(self.image, (self.ground.width*3,self.ground.height))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x < -self.ground.width*3:
            self.kill()

class Sounds():
    def __init__(self):
        super().__init__() 
        self.jump = pygame.mixer.Sound("jump_sound.wav")
        self.bump = pygame.mixer.Sound("smb_bump.wav")
        self.stomp = pygame.mixer.Sound("smb_stomp.wav")
        self.coin = pygame.mixer.Sound("smb_coin.wav")
        self.death = pygame.mixer.Sound("smb_mariodie.wav")
        self.win = pygame.mixer.Sound("smb_stage_clear.wav")

class Goombas(pygame.sprite.Sprite):
    # Loads all the Enemy Sprites
    def __init__(self):
        super().__init__()

        
        self.ground = Ground()
        self.images = []
        self.stomp = pygame.image.load("slub3.png").convert()
        self.stomp = pygame.transform.scale(self.stomp, (self.ground.width,self.ground.height))
        self.image1 = pygame.image.load("slub1.png").convert()
        self.image1 = pygame.transform.scale(self.image1, (self.ground.width,self.ground.height))
        self.image2 = pygame.image.load("slub2.png").convert()
        self.image2 = pygame.transform.scale(self.image2, (self.ground.width,self.ground.height))
        self.images.append(self.image1)
        self.images.append(self.image2)
        self.time = 0

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Set speed vector of Enemies
         
        self.change_x = 0
        self.change_y = 0
        

        # List of sprites we can bump against
        self.level = None

        # Change image

    
    def update(self):
        self.time += 1
        if self.time % 8 == 0:
            self.index += 1
            if self.index > (len(self.images)-1):
                self.index = 0
            self.image = self.images[self.index]
        

        
        

        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        # See if we hit anything
        collide = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        if (self.rect.x - Player().rect.x) <= 800:
            if self.change_x == 0:
                self.change_x = -2
            for block in collide:
                if self.change_x < 0:
                    self.rect.left = block.rect.right
                    self.change_x = 2
                elif self.change_x > 0:
                    self.rect.right = block.rect.left
                    self.change_x = -2
        
                
        
        self.calc_grav()
        if self.rect.y > SCREEN_HEIGHT or self.rect.x < -self.ground.width:
            self.kill()

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
                

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        # Calculate the effect of gravity
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        

class Koopas(pygame.sprite.Sprite):
    # Loads all the Enemy Sprites
    def __init__(self):
        super().__init__()

        
        self.ground = Ground()
        self.images = []
        self.shell = pygame.image.load("monster3.png").convert()
        self.shell = pygame.transform.scale(self.shell, (self.ground.width,self.ground.height))

        self.image1 = pygame.image.load("monster1.png").convert()
        self.image1 = pygame.transform.scale(self.image1, (self.ground.width,self.ground.height))
        self.image2 = pygame.image.load("monster2.png").convert()
        self.image2 = pygame.transform.scale(self.image2, (self.ground.width,self.ground.height))
        self.images.append(self.image1)
        self.images.append(self.image2)

        self.time = 0
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Set speed vector of Enemies
         
        self.change_x = 0
        self.change_y = 0
        

        # List of sprites we can bump against
        self.level = None

        # Change image

        for i in range(len(self.images)):
                if self.images[i] != self.shell:
                    self.image = self.images[self.index]
                else:
                    self.images[i] = self.shell

    
    def update(self):
        self.time += 1
        if self.time % 8 == 0:
            self.index += 1
            if self.index > (len(self.images)-1):
                self.index = 0
            self.image = self.images[self.index]

        
        

        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        # See if we hit anything
        collide = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        if (self.rect.x - Player().rect.x) <= 800:
            if self.change_x == 0:
                self.change_x = -2
            for block in collide:
                if self.change_x < 0:
                    self.rect.left = block.rect.right
                    self.change_x = 2
                elif self.change_x > 0:
                    self.rect.right = block.rect.left
                    self.change_x = -2
        
                
        
        self.calc_grav()
        if self.rect.y > SCREEN_HEIGHT or self.rect.x < -self.ground.width:
            self.kill()

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
                

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        # Calculate the effect of gravity
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35



class Level():
    # Generic super class used to define a level. Create a child class for each
    # level with level-specific info.
    def __init__(self, player):
        # Constructor. Needed for when moving collide with the player
        self.background = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.pow_list = pygame.sprite.Group()
        self.player = player
        # Specific enemies
        self.goomba_list = pygame.sprite.Group()
        self.koopa_list = pygame.sprite.Group()
        self.enemy_list = [self.goomba_list, self.koopa_list]
        

        self.world_shift = 0
        # Background image
        #self.background = None

    # Update everything on this level
    def update(self):
        # Update everything in this level.
        
        self.background.update()
        self.platform_list.update()
        for enemy in self.enemy_list:
            for i in enemy:
                if i.rect.x < 800:
                    i.update()

    def draw(self, screen):
        # Draw everything on the level

        # Draw the background
        screen.fill(SKY_BLUE)

        # Draw the sprite lists we have
        for back in self.background:
            if back.rect.x < 800:
                screen.blit(back.image, [back.rect.x, back.rect.y])
        for objects in self.platform_list:
            if objects.rect.x < 800:
                screen.blit(objects.image, [objects.rect.x, objects.rect.y])
        for enemy in self.enemy_list:
            for i in enemy:
                if i.rect.x < 800:
                    screen.blit(i.image, [i.rect.x, i.rect.y])

    def shift_world(self, shift_x):
    # Scrolls the screen

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for stuff in self.background:
            stuff.rect.x += shift_x

        for enemy in self.enemy_list:
            for i in enemy:
                i.rect.x += shift_x
        
class Level_01 (Level):
    def __init__(self, player):
        
        Level.__init__(self, player)
        end = 190*Ground().width
        self.level_limit = -end
        self.time = 300

        pygame.mixer.music.load("01-main-theme-overworld.mp3")
        

        # Array with x and y of ground
        ground = []
        missing_ground = [60, 61, 77, 78, 79, 145, 146]
        for j in range(len(missing_ground)):
                missing_ground[j] = (missing_ground[j]*Ground().width)
        for i in range(0, 10000, Ground().width):
            if i not in missing_ground:
                ground.append([i, SCREEN_HEIGHT - Ground().height])
            else:
                ground.append([0, SCREEN_HEIGHT - Ground().height])
                

        # Go through the array and add all bricks
        for bricks in ground:
            brick = Ground()
            brick.rect.x = bricks[0]
            brick.rect.y = bricks[1]
            brick.player = self.player
            self.platform_list.add(brick)

        # Brick blocks
        red_bricks = [[11*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [13*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [15*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [68*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [70*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [71*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [72*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [73*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [74*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [75*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [76*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [77*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [78*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [82*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [83*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [84*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [85*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [86*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [92*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [93*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [110*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [113*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [114*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [115*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [120*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [121*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [122*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [123*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [160*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [161*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [163*Ground().width, SCREEN_HEIGHT - 5*Ground().height]
                      ]
        for rbricks in red_bricks:
            rbrick = Bricks()
            rbrick.rect.x = rbricks[0]
            rbrick.rect.y = rbricks[1]
            rbrick.player = self.player
            self.platform_list.add(rbrick)

        # Pow Blocks
        pow_blocks = [[7*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [12*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [14*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [13*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [69*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [86*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [98*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [101*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [101*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [104*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                      [121*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [122*Ground().width, SCREEN_HEIGHT - 9*Ground().height],
                      [162*Ground().width, SCREEN_HEIGHT - 5*Ground().height]
                      ]
        for blocks in pow_blocks:
            block = Pow()
            block.rect.x = blocks[0]
            block.rect.y = blocks[1]
            block.player = self.player
            self.platform_list.add(block)            
            


        # Metal Blocks
        metal_blocks = []
        for i in range(4):
            for j in range(i+1):
                metal_blocks.append([(i+126)*Ground().width, SCREEN_HEIGHT - (j+2)*Ground().height])
                metal_blocks.append([(i+140)*Ground().width, SCREEN_HEIGHT - (j+2)*Ground().height])
            # Extra columns of blocks
            metal_blocks.append([144*Ground().width, SCREEN_HEIGHT - (i+2)*Ground().height])
        for i in range(8):
            for j in range(i+1):
                metal_blocks.append([(i+173)*Ground().width, SCREEN_HEIGHT - (j+2)*Ground().height])

            # Extra columns of blocks
            metal_blocks.append([181*Ground().width, SCREEN_HEIGHT - (i+2)*Ground().height])

        for i in range(4):
            for j in range(i+1):
                metal_blocks.append([(135-i)*Ground().width, SCREEN_HEIGHT - (j+2)*Ground().height])        
                metal_blocks.append([(150-i)*Ground().width, SCREEN_HEIGHT - (j+2)*Ground().height])        

       # Flag Pole Base
        metal_blocks.append([190*Ground().width, SCREEN_HEIGHT - 2*Ground().height])
        
        for blocks in metal_blocks:
            block = Metal_Blocks()
            block.rect.x = blocks[0]
            block.rect.y = blocks[1]
            block.player = self.player
            self.platform_list.add(block)

        # Flag Pole
        flag_pole = [end, SCREEN_HEIGHT - 12*Ground().height]
        pole = Flag_Pole()
        pole.rect.x = flag_pole[0]
        pole.rect.y = flag_pole[1]
        pole.player = self.player
        self.platform_list.add(pole)
            

        # Small Green Pipes
        small_green_pipes = [[19*Ground().width, SCREEN_HEIGHT - 3*Ground().height],
                             [155*Ground().width, SCREEN_HEIGHT - 3*Ground().height],
                             [171*Ground().width, SCREEN_HEIGHT - 3*Ground().height]
                             ]

        for pipes in small_green_pipes:
            pipe = Small_Pipes()
            pipe.rect.x = pipes[0]
            pipe.rect.y = pipes[1]
            pipe.player = self.player
            self.platform_list.add(pipe)

        # Medium Green Pipes
        medium_green_pipes = [[29*Ground().width, SCREEN_HEIGHT - 4*Ground().height]]

        for pipes in medium_green_pipes:
            pipe = Medium_Pipes()
            pipe.rect.x = pipes[0]
            pipe.rect.y = pipes[1]
            pipe.player = self.player
            self.platform_list.add(pipe)

        # Large Green Pipes
        large_green_pipes = [[37*Ground().width, SCREEN_HEIGHT - 5*Ground().height],
                             [48*Ground().width, SCREEN_HEIGHT - 5*Ground().height]
                             ]

        for pipes in large_green_pipes:
            pipe = Large_Pipes()
            pipe.rect.x = pipes[0]
            pipe.rect.y = pipes[1]
            pipe.player = self.player
            self.platform_list.add(pipe)


        # Background Scenery:

        # Small Bushes:
        bushes = [[14*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                  [62*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                  [111*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                  [159*Ground().width, SCREEN_HEIGHT - 2*Ground().height]
                  ]
        for bush in bushes:
            block = Small_Bushes()
            block.rect.x = bush[0]
            block.rect.y = bush[1]
            self.background.add(block)

        # Medium Bushes
        bushes2 = [[32*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                  [80*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                  [130*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                  ]
        for bush in bushes2:
            block = Medium_Bushes()
            block.rect.x = bush[0]
            block.rect.y = bush[1]
            self.background.add(block)

        # Large Bushes
        bushes2 = [[2*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                  [50*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                  [102*Ground().width, SCREEN_HEIGHT - 2*Ground().height]
                  ]
        for bush in bushes2:
            block = Large_Bushes()
            block.rect.x = bush[0]
            block.rect.y = bush[1]
            self.background.add(block)

        # Small Hills
        hills = [[7*Ground().width,SCREEN_HEIGHT - 2*Ground().height],
                 [55*Ground().width,SCREEN_HEIGHT - 2*Ground().height],
                 [107*Ground().width,SCREEN_HEIGHT - 2*Ground().height],
                 [152*Ground().width,SCREEN_HEIGHT - 2*Ground().height]
                 ]
        for hill in hills:
            block = Small_Hills()
            block.rect.x = hill[0]
            block.rect.y = hill[1]
            self.background.add(block)

        # Large Hills
        large_hills = [[39*Ground().width, SCREEN_HEIGHT - 3*Ground().height],
                       [100*Ground().width, SCREEN_HEIGHT - 3*Ground().height],
                       [136*Ground().width, SCREEN_HEIGHT - 3*Ground().height],
                       [184*Ground().width, SCREEN_HEIGHT - 3*Ground().height]
                       ]
        for hill in large_hills:
            block = Large_Hills()
            block.rect.x = hill[0]
            block.rect.y = hill[1]
            self.background.add(block)

        # Small Clouds
        clouds = [[10*Ground().width, SCREEN_HEIGHT - 12*Ground().height],
                  [48*Ground().width, SCREEN_HEIGHT - 11*Ground().height],
                  [19*Ground().width, SCREEN_HEIGHT - 11*Ground().height],
                  [58*Ground().width, SCREEN_HEIGHT - 12*Ground().height],
                  [67*Ground().width, SCREEN_HEIGHT - 11*Ground().height],
                  [109*Ground().width, SCREEN_HEIGHT - 11*Ground().height],
                  [111*Ground().width, SCREEN_HEIGHT - 12*Ground().height],
                  [119*Ground().width, SCREEN_HEIGHT - 11*Ground().height],
                  [145*Ground().width, SCREEN_HEIGHT - 11*Ground().height],
                  [155*Ground().width, SCREEN_HEIGHT - 12*Ground().height],
                  [163*Ground().width, SCREEN_HEIGHT - 12*Ground().height],
                  [193*Ground().width, SCREEN_HEIGHT - 12*Ground().height]
                  ]
        for cloud in clouds:
            block = Clouds()
            block.rect.x = cloud[0]
            block.rect.y = cloud[1]
            self.background.add(block)

        # Large Clouds
        large_clouds = [[49*Ground().width, SCREEN_HEIGHT - 11*Ground().height],
                        [57*Ground().width, SCREEN_HEIGHT - 12*Ground().height],
                        [68*Ground().width, SCREEN_HEIGHT - 11*Ground().height],
                        [76*Ground().width, SCREEN_HEIGHT - 12*Ground().height],
                        [120*Ground().width, SCREEN_HEIGHT - 11*Ground().height],
                        [129*Ground().width, SCREEN_HEIGHT - 12*Ground().height],
                        [164*Ground().width, SCREEN_HEIGHT - 11*Ground().height],
                        [173*Ground().width, SCREEN_HEIGHT - 12*Ground().height]
                        ]
        for cloud in large_clouds:
            block = Large_Clouds()
            block.rect.x = cloud[0]
            block.rect.y = cloud[1]
            self.background.add(block)


        # Enemies
        goombas = [[12*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                   [23*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                   [44*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                   [45*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                   [72*Ground().width, SCREEN_HEIGHT - 10*Ground().height],
                   [74*Ground().width, SCREEN_HEIGHT - 10*Ground().height],
                   [99*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                   [101*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                   [115*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                   [117*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                   [119*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                   [121*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                   [165*Ground().width, SCREEN_HEIGHT - 2*Ground().height],
                   [167*Ground().width, SCREEN_HEIGHT - 2*Ground().height]
                   ]

        for goom in goombas:
            block = Goombas()
            block.rect.x = goom[0]
            block.rect.y = goom[1]
            block.player = self.player
            block.level = self
            self.goomba_list.add(block)

        koopas = [[109*Ground().width, SCREEN_HEIGHT - 2*Ground().height]
                  ]
        for koopa in koopas:
            block = Koopas()
            block.rect.x = koopa[0]
            block.rect.y = koopa[1]
            block.player = self.player
            block.level = self
            self.koopa_list.add(block)
        


def texts(text, surface, x, y):
    font = pygame.font.Font("emulogic.ttf", 15)
    text = font.render(text, 1, WHITE)
    textrect = text.get_rect()
    textrect.topleft = (x, y)
    surface.blit(text, textrect)

def win(time, player, a):
    pygame.mixer.music.stop()
    Sounds().win.play()
    Sounds().win.stop()
    while a:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = False
            if event.type == pygame.KEYDOWN:
                return



def main():
    a = True
    while a:
        pygame.init()
        pygame.font.init()

        # Set the height and width of the screen
        size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        screen = pygame.display.set_mode(size)
        screen.set_alpha(None)

        pygame.display.set_caption("Super Will Bros.")

        
        seconds = Level_01(Level).time
        seconds1 = 0

        # Create the player
        player = Player()

        # Get Bricks
        ground = Ground()

        # Get Flag Pole
        flag = Flag_Pole()

        # Create the levels
        level_list = []
        level_list.append(Level_01(player))
       

        # Set current level
        current_level_no = 0
        current_level = level_list[current_level_no]

        active_sprite_list = pygame.sprite.Group()
        player.level = current_level

        # Play level music
        pygame.mixer.music.play(-1)

        player.rect.x = 340
        player.rect.y = SCREEN_HEIGHT - player.rect.height - ground.height
        active_sprite_list.add(player)
        

        # Loop until the user clicks the close button.
        done = False

        # Dummy Variable
        dumb = False

        
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        #win(seconds,player)
        
        # Define an empty list
        empty_list = [275]
        while not done:
            if player.rect.y > SCREEN_HEIGHT*15:
                done = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if empty_list[-1] == 275:
                            player.image = pygame.transform.flip(player.image, True, False)
                        empty_list.append(event.key)
                        player.go_left()
                    elif event.key == pygame.K_RIGHT:
                        if empty_list[-1] == 276:
                            player.image = pygame.transform.flip(player.image, True, False)
                        empty_list.append(event.key)
                        player.go_right()
                    if event.key == pygame.K_UP:
                        if player.change_y == 0:
                            Sounds().jump.play()
                        player.jump()
                        

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()

            # Update the player
            active_sprite_list.update()

            # Update items in the level
            current_level.update()

            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right >= SCREEN_WIDTH - 300:
                diff = player.rect.right - 500
                player.rect.right = 500
                current_level.shift_world(-diff)

            # Don't allow player to go past x = 0
            elif player.rect.left <= 0:
                player.rect.left = 0

            # If player gets to the end, then move on to second level
            position = player.rect.x + current_level.world_shift
            if position == current_level.level_limit + 955:
                done = True
                dumb = True


            # Code to draw items
            current_level.draw(screen)
            active_sprite_list.draw(screen)

            # Draw the text:
            seconds1 += 1
            if seconds1 % 16 == 0:
                seconds -= 1
            if seconds == 0:
                done = True
            time = texts("Time", screen, 600, 15)
            time1 = texts(str(seconds), screen, 615, 30)
            world = texts("World", screen, 450, 15)
            world1 = texts("World", screen, 450, 15)
            

            # Limit to 70 frames per second
            clock.tick(40)

            # Update the screen with what was drawn
            pygame.display.flip()
        if dumb == True:
            win(seconds, player, a)
        else:
            a = False
    pygame.quit()

if __name__ == "__main__":
    main()
