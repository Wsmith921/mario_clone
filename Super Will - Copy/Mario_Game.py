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

        self.music = parser.get("level 1", "music")

            
        

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
            
        self.image = self.right_images[0]
        self.rect = self.image.get_rect()
        self.rect.width = self.rect.width-10

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
                    self.index = 1  # First running frame
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
                if str(block) == "<Pow sprite(in 1 groups)>" and block.image != block.blank:
                    block.hit()
                block.sound.play()

 
            # Stop our vertical movement
            self.change_y = 0

        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for block in enemy_hit_list:
            if self.change_y > 0:
                block.stompy()
                self.change_y = -8

            

    def calc_grav(self):
        # Calculate the effects of gravity
        if self.change_y == 0:
            self.change_y = 2
        else:
            self.change_y += 0.50

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
        if len(platform_hit_list) > 0:
            Sounds().jump.play()
            self.change_y = -15

    # Player Controlled movement
    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6
    def stop(self):
        self.change_x = 0
        




class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.time = 0

        self.index = 0
        

        # Set speed vector of Enemies
         
        self.change_x = -3
        self.change_y = 0

        self.level = None
    def update(self):
        self.time += 1
        if self.images != None:
            if self.time % 8 == 0:
                self.index += 1
                if self.index > (len(self.images)-1):
                    self.index = 0
                self.image = self.images[self.index]

        self.rect.x += self.change_x

        
        collide = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in collide:
            if self.change_x < 0:
                self.rect_left = block.rect.right
                self.change_x = -self.change_x
            elif self.change_x > 0:
                self.rect_right = block.rect.left
                self.change_x = -self.change_x

        self.calc_grav()

        self.rect.y += self.change_y
        collide = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in collide:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

    def stompy(self):
        Sounds().stomp.play()
        if str(self) == "<Goombas sprite(in 1 groups)>":
            self.rect.height -= scale

        elif str(self) == "<Koopas sprite(in 1 groups)>":
            self.rect.height = self.dumb.height 
        self.image = self.stomp
        self.images = None
        self.change_x = 0

    

class Goombas(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.images = []
        self.stomp = pygame.image.load("slub3.png").convert()
        self.stomp = pygame.transform.scale(self.stomp, (scale,scale//2))
        self.image1 = pygame.image.load("slub1.png").convert()
        self.image1 = pygame.transform.scale(self.image1, (scale,scale))
        self.image2 = pygame.image.load("slub2.png").convert()
        self.image2 = pygame.transform.scale(self.image2, (scale,scale))
        self.images.append(self.image1)
        self.images.append(self.image2)
        self.time = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "goomba")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b

class Koopas(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.images = []
        self.stomp = pygame.image.load("monster3.png")
        self.stomp = pygame.transform.scale(self.stomp, (scale, scale//2))
        self.dumb = self.stomp.get_rect()
        self.image1 = pygame.image.load("monster1.png").convert()
        self.image1 = pygame.transform.scale(self.image1, (scale,scale))
        self.image2 = pygame.image.load("monster2.png").convert()
        self.image2 = pygame.transform.scale(self.image2, (scale,scale))
        self.images.append(self.image1)
        self.images.append(self.image2)

        self.time = 0
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        


    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "koopa")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b




class Bricks(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("brick_block.png")
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
class Blocks(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("metal_block.png")
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.rect = self.image.get_rect()

    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "metal")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b

class Pow(pygame.sprite.Sprite):
    # Power blocks in super mario
    def __init__(self):
        super().__init__()
        self.player = Player()
        self.images = []
        self.blank = pygame.image.load("platform-air.png")
        self.blank = pygame.transform.scale(self.blank,(scale,scale))
        self.image1 = pygame.image.load("platform-q.png")
        self.image2 = pygame.image.load("platform-q1.png")
        self.image3 = pygame.image.load("platform-q2.png")
        self.image4 = pygame.image.load("platform-q3.png")
        self.images.append(self.image1)
        self.images.append(self.image2)
        self.images.append(self.image3)
        self.images.append(self.image4)
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (scale,scale))
        
        self.time = 0        
        self.image = self.images[0]
        self.index = 0
            
        self.rect = self.image.get_rect()
        # Makes it so we can hit the pow block without hitting the bricks all the time
        self.rect.height = self.rect.height + 2

        self.a = [False]

    
    def update(self):
        self.time += 1
        if self.images != None:
            if self.time % 15 == 0:
                self.index += 1
                if self.index > (len(self.images)-1):
                    self.index = 0
                self.image = self.images[self.index]
            
            


    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "power")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b

    def hit(self):
        self.sound = Sounds().coin
        self.image = self.blank
        self.images = None
        self.rect.height = self.rect.height - 2




        





class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ground_block.jpg")
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

class Small_Pipes(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("small_green_pipe.png")
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (scale*2,scale*2))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "pipe")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b

class Medium_Pipes(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pipe_green.png")
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (scale*2,scale*3))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "medium_pipe")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b

class Big_Pipes(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pipe_greenbig.png")
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (scale*2,scale*4))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "big_pipe")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b

class Small_Hill(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("hill2.png")
        #self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (scale*3,scale))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "small_hill")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b
    
class Big_Hill(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("hill.png")
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (scale*5,scale*2))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "big_hill")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b

class Small_Bush(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bush-3.png")
        self.image = pygame.transform.scale(self.image, (scale*3,scale))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "small_bush")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b

class Medium_Bush(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bush-2.png")
        self.image = pygame.transform.scale(self.image, (scale*4,scale))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "medium_bush")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b
    
class Big_Bush(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bush-1.png")
        self.image = pygame.transform.scale(self.image, (scale*5,scale))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "big_bush")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b
    

class Small_Cloud(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cloud.png").convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.image = pygame.transform.scale(self.image, (scale*3,scale*2))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "small_cloud")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b
class Medium_Cloud(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("dobbelclouds.png").convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.image = pygame.transform.scale(self.image, (scale*4,scale*2))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "medium_cloud")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b

class Big_Cloud(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("big_cloud.png").convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.image = pygame.transform.scale(self.image, (scale*5,scale*2))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "large_cloud")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b

class Flagpole(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("flagpole.png").convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.image = pygame.transform.scale(self.image, (scale*2,scale*10))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "flagpole")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b
    
class Small_Castle(pygame.sprite.Sprite):
    # Small Green Pipes
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("castle.png")
        self.image = pygame.transform.scale(self.image, (scale*5,scale*5))
        self.rect = self.image.get_rect()
    def pos(self):
        a = Structure().obj
        b = np.array((np.where(a == "small_castle")))
        b = np.flip(b, 0)
        b = np.transpose(b)*scale
        b[:,-1] = SCREEN_HEIGHT - scale - b[:,-1]
        b = b.tolist()
        return b



class Sounds():
    def __init__(self):
        super().__init__()
        self.jump = pygame.mixer.Sound("jump_sound.wav")
        self.bump = pygame.mixer.Sound("smb_bump.wav")
        self.stomp = pygame.mixer.Sound("smb_stomp.wav")
        self.coin = pygame.mixer.Sound("smb_coin.wav")
        self.death = pygame.mixer.Sound("smb_mariodie.wav")
        self.win = pygame.mixer.Sound("smb_stage_clear.wav")

class Music():
    def __init__(self):
        super().__init__()
        self.overworld = "01-main-theme-overworld.mp3"
        
        
        


class Level(object):
    def __init__(self, player):
        # We need to pass in the player to handle collisions with platforms
        #super().__init__()
        self.platform_list = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # How far world has shifted
        self.world_shift = 0
        

        self.music = Structure().music
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()
        
        self.build()
        self.bump()

    # Need to update everything on this level
    def update(self):
        self.background.update()
        self.platform_list.update()
        for enemy in self.enemy_list:
            if enemy.rect.x <= 800:
                enemy.update()

    

    def draw(self, screen):
        # Draw everything on this level

        # Draw the background
        screen.fill(SKY_BLUE)

        # Draw all the sprite lists that we have
        for back in self.background:
            if back.rect.x < 800:
                screen.blit(back.image,[back.rect.x, back.rect.y])
            if back.rect.x < -scale*5:
                back.kill()
        for plat in self.platform_list:
            if plat.rect.x < 800:
                screen.blit(plat.image,[plat.rect.x, plat.rect.y])
            if plat.rect.x < -scale*5:
                plat.kill()
        for enemy in self.enemy_list:
            if enemy.rect.x < 800:
                screen.blit(enemy.image,[enemy.rect.x, enemy.rect.y])
            if enemy.rect.x < -scale or enemy.rect.y + scale >= SCREEN_HEIGHT:
                enemy.kill()

    def shift_world(self, shift_x):
    # Scrolls the screen

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for back in self.background:
            back.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

                
        #self.enemy_list.draw(screen)
    def bump(self):
        for block in self.platform_list:
            if str(block) !="<Pow sprite(in 1 groups)>":
                block.sound = Sounds().bump




    def build(self):        
        # Positions of all the given blocks in the Level
        bricks = Bricks().pos()
        ground = Ground().pos()
        powblocks = Pow().pos()
        metal_blocks = Blocks().pos()
        small_pipes = Small_Pipes().pos()
        medium_pipes = Medium_Pipes().pos()
        big_pipes = Big_Pipes().pos()
        small_hills = Small_Hill().pos()
        big_hills = Big_Hill().pos()
        small_bush = Small_Bush().pos()
        medium_bush = Medium_Bush().pos()
        big_bush = Big_Bush().pos()
        small_cloud = Small_Cloud().pos()
        medium_cloud = Medium_Cloud().pos()
        big_cloud = Big_Cloud().pos()
        small_castle = Small_Castle().pos()
        flagpole = Flagpole().pos()

        goomba = Goombas().pos()
        koopa = Koopas().pos()
        

        
        for b in bricks:
            block = Bricks()
            block.rect.x = b[0]
            block.rect.y = b[1]
            block.player = self.player
            self.platform_list.add(block)



        for g in ground:
            block1 = Ground()
            block1.rect.x = g[0]
            block1.rect.y = g[1]
            block1.player = self.player
            self.platform_list.add(block1)

        
        
        for p in powblocks:
            block2 = Pow()
            block2.rect.x = p[0]
            block2.rect.y = p[1]
            #block2.player = self.player
            self.platform_list.add(block2)

        for m in metal_blocks:
            block3 = Blocks()
            block3.rect.x = m[0]
            block3.rect.y = m[1]
            block3.player = self.player
            self.platform_list.add(block3)

        for p1 in small_pipes:
            block4 = Small_Pipes()
            block4.rect.x = p1[0]
            block4.rect.y = p1[1]
            block4.player = self.player
            self.platform_list.add(block4)
            
        for p2 in medium_pipes:
            block5 = Medium_Pipes()
            block5.rect.x = p2[0]
            block5.rect.y = p2[1]
            block5.player = self.player
            self.platform_list.add(block5)

        for p3 in big_pipes:
            block6 = Big_Pipes()
            block6.rect.x = p3[0]
            block6.rect.y = p3[1]
            block6.player = self.player
            self.platform_list.add(block6)


        for h in small_hills:
            block7 = Small_Hill()
            block7.rect.x = h[0]
            block7.rect.y = h[1]
            block7.player = self.player
            self.background.add(block7)
            
        for h1 in big_hills:
            block8 = Big_Hill()
            block8.rect.x = h1[0]
            block8.rect.y = h1[1]
            block8.player = self.player
            self.background.add(block8)

        for b in small_bush:
            block9 = Small_Bush()
            block9.rect.x = b[0]
            block9.rect.y = b[1]
            block9.player = self.player
            self.background.add(block9)

        for b2 in medium_bush:
            block11 = Medium_Bush()
            block11.rect.x = b2[0]
            block11.rect.y = b2[1]
            block11.player = self.player
            self.background.add(block11)

        for b1 in big_bush:
            block10 = Big_Bush()
            block10.rect.x = b1[0]
            block10.rect.y = b1[1]
            block10.player = self.player
            self.background.add(block10)

        for c in small_cloud:
            block11 = Small_Cloud()
            block11.rect.x = c[0]
            block11.rect.y = c[1]
            block11.player = self.player
            self.background.add(block11)

        for c1 in medium_cloud:
            block12 = Medium_Cloud()
            block12.rect.x = c1[0]
            block12.rect.y = c1[1]
            block12.player = self.player
            self.background.add(block12)

        for c2 in big_cloud:
            block12 = Big_Cloud()
            block12.rect.x = c2[0]
            block12.rect.y = c2[1]
            block12.player = self.player
            self.background.add(block12)

        for s in small_castle:
            block13 = Small_Castle()
            block13.rect.x = s[0]
            block13.rect.y = s[1]
            block13.player = self.player
            self.background.add(block13)

        for f in flagpole:
            block14 = Flagpole()
            block14.rect.x = f[0]
            block14.rect.y = f[1]
            block14.player = self.player
            self.background.add(block14)

        for g in goomba:
            block15 = Goombas()
            block15.rect.x = g[0]
            block15.rect.y = g[1]
            block15.level = self
            self.enemy_list.add(block15)

        for k in koopa:
            block16 = Koopas()
            block16.rect.x = k[0]
            block16.rect.y = k[1]
            block16.level = self
            self.enemy_list.add(block16)

        

    



        


def main():
    pygame.mixer.pre_init(buffer = 100)
    pygame.init()
    
    player = Player()
    # Create all the levels
    level = Level(player)
    #level_list.append(Level_01(player))
 
    # Set the current level
    #current_level_no = 0
    #current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = level
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
            level.shift_world(-diff)

        active_sprite_list.update()
        # Update items in the level
        level.update()
        level.draw(screen)
        active_sprite_list.draw(screen)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

if __name__== "__main__":
    main()



        
