import pygame
from pygame.locals import *
import pickle

pygame.init()

#sets fps
clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800
tile_size = screen_height/20
game_over = 0
main_menu = True
level = 1


screen =  pygame.display.set_mode((screen_width, screen_height)) #makes screen
pygame.display.set_caption('67platformer67')  #name for the screen in the top header bar

class Button():
    def __init__(self,x,y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    
    def draw(self):
        action  = False
        
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            #getpressed function returns list that has left, right and middle mouse click where left mouse click is 0th index
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action  = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #draw button
        screen.blit(self.image, self.rect)

        return action

def draw_grid():
    for line in range(0,20): 
        pygame.draw.line(screen, (255,255,255),(0, line *tile_size),(screen_width,line*tile_size))
        pygame.draw.line(screen, (255,255,255),( line *tile_size,0),(line*tile_size,screen_width))

class Player():
    def __init__(self,x,y):
        self.reset(x,y)
 
    def update(self, game_over):
        
        dx = 0
        dy = 0

        if game_over == 0:

            #get key presses
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped ==False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True  
            #elif key[pygame.K_UP] == False:
            #   self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 3
            if key[pygame.K_RIGHT]:
                dx += 3
        
        
            #add gravity 
            self.vel_y += 1   #base gravity value
            if self.vel_y >10: #stops you from infinetly accelerating when falling for too long, terminal velocity
                self.vel_y = 10

            dy += self.vel_y

            #check for collision
            #1. calculate new player pos
            #2. check collision at new pos
            #3. adjust player position
           
            self.in_air = True
            for tile in worldCurrent.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x +dx, self.rect.y,self.width,self.height):    
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width,self.height): #creates new rect with coords of current player but adds the future y coord (dy) to check for collision before updating player position
                    #check if below ground (jumping)
                    if self.vel_y< 0: #y only negative when jumping
                        dy = tile[1].bottom - self.rect.top  #sets dy to most largest it can move with no collision, bottom of block - top of player
                        self.vel_y = 0
                    #check if above ground(falling)
                    elif self.vel_y >= 0: #y only negative when jumping
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0 
                        self.in_air = False  
            if dy == 0:
                self.jumped = False    
                
            

            #check for collision with enemies 
            for sprite in blob_group:
                if sprite.rect.top == self.rect.bottom and self.in_air == True:
                    print("get goombad")
                    self.vel_y = -15
                    self.jumped = True  
                
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1     
                #check for collision with spike
            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, flyer1_group, False):
                game_over = -1      
       
        elif game_over == -1:
            self.image = self.dead_image
            

            
            
        #update player coords
        self.rect.x +=dx
        self.rect.y +=dy

      
        #draw player on screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen,(255,255,0),self.rect,2)

        return game_over
    
    def reset (self,x,y):
        img = pygame.image.load('img/player.webp')
        dead = pygame.image.load('img/dead.webp')
        self.image = pygame.transform.scale(img,(tile_size-15,tile_size ))
        self.rect = self.image.get_rect()  #creates hitbox for player, alwasy attached to player
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped  = False
        self.dead_image =  pygame.transform.scale(dead ,(tile_size-15,tile_size ))
        self.in_air = True

    


class World():
    def __init__(self, data):
        self.tile_list = []
        
        #load images
        dirt_img = pygame.image.load('img/dirt.jpg')
        grass_img = pygame.image.load('img/grass.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:  #dirt
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))  #makes image of dirt cube
                    img_rect = img.get_rect()   #makes the dirt image actually have a bounds
                    img_rect.x = col_count *tile_size
                    img_rect.y = row_count *tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:  #grass
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))  #makes image of grass cube
                    img_rect = img.get_rect()   #makes the dirt image actually have a bounds
                    img_rect.x = col_count *tile_size
                    img_rect.y = row_count *tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:  #enemy
                    blob = Enemy(col_count *tile_size, row_count *tile_size)
                    blob_group.add(blob)
                if tile == 4: #spike
                    spike = Spike(col_count *tile_size, row_count *tile_size)
                    spike_group.add(spike)
                if tile == 5: #horiztonal flyer
                    flyer = FlyerH(col_count *tile_size, row_count *tile_size)
                    flyer1_group.add(flyer)

                col_count += 1
            row_count +=1
    def draw(self):
        for tile in self.tile_list: #self.tile_list looks for the tile list from this created object and no other world objects
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen,(0,0,0),tile[1],2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        Eimg = pygame.image.load('img/enemy.jpg')
        
        self.image = pygame.transform.scale(Eimg, (tile_size, tile_size))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update (self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > tile_size-5:
            self.move_direction *= -1
            self.move_counter *= -1

class FlyerH(pygame.sprite.Sprite):
    def __init__(self, x,y,numTiles = 5):
        pygame.sprite.Sprite.__init__(self)
        Eimg = pygame.image.load('img/enemy.jpg') #CHANGE IMAGE
        
      
        self.image = pygame.transform.scale(Eimg, (tile_size, tile_size))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.range = numTiles * tile_size

    def update (self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > self.range:
            self.move_direction *= -1
            self.move_counter *= -1

class Spike(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        Eimg = pygame.image.load('img/spike.png')
        
        self.image = pygame.transform.scale(Eimg, (tile_size - 10, tile_size - 10))
        self.rect= self.image.get_rect()
        self.rect.x = x + 4
        self.rect.y = y + 10
       


#blueprint for making world, every 1 will be a block and it matches 10x10 grid
worldAsFile = open(f"level{level}_data.txt")
world_data = [worldAsFile.read()]
print(worldAsFile)
print(worldAsFile.read())

worldTest_data = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #2
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #3
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #4
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #5
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #6
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #7
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #8
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #9
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #10
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #11
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #12
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #13
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #14
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #15
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #16
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #17
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #18
    [0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0], #19
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], #20
]
world11_data = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #2
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #3
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #4
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #5
    [0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,0,0,0,0], #6
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0], #7
    [0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0], #8
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0], #9
    [0,0,2,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0], #10
    [0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0], #11
    [0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0], #12
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #13
    [0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0], #14
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #15
    [0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0], #16
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #17
    [0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0], #18
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #19
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], #20
]
world12_data = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #t
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #3
    [2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #4
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2], #5
    [0,0,0,0,0,2,0,2,0,2,0,2,0,2,0,2,0,0,0,0], #6
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #7
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #8
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #9
    [0,0,0,0,0,2,4,4,4,4,4,4,4,4,4,4,4,4,4,4], #10
    [0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], #11
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #12
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #13
    [0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #14
    [0,0,0,0,4,0,0,4,0,0,4,0,0,4,0,0,0,0,0,0], #15
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0], #16
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #17
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0], #18
    [0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0,0], #19
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], #20
]
#load images
sky_img = pygame.image.load('img/placeholder.jpg') #looks for img folder inside of open folder and inside of img folder looks for placeholder.jpg
restart_img = pygame.image.load("img/restart.png")
start_img = pygame.image.load("img/start_btn.png")
exit_img = pygame.image.load("img/exit_btn.png")

player = Player(40,screen_height - 50)
spike_group = pygame.sprite.Group()
blob_group = pygame.sprite.Group()
flyer1_group = pygame.sprite.Group()

#load  in level data and create world
#pickle_in = open(f'level{level}_data.text')
#world_data = pickle.load(pickle_in)

worldCurrent = World(worldTest_data)

#world2 = World(world2_data)

#create buttons
restart_button = Button(screen_width//2 -50, screen_height//2 + 100, restart_img) 
start_button = Button(screen_width//2 -250, screen_height//2 + 100, start_img)
exit_button = Button(screen_width//2 +150, screen_height//2 + 100, exit_img)


run = True
while run: #runs game
    clock.tick(fps) #restricts game to certain fps
    
    #draws loaded images
    #order images drawn matter because a larger image can cover a smaller image if smaller image is loaded first
    screen.blit(sky_img, (0,0))
    if main_menu:
        if exit_button.draw() == True:
            run = False
        if start_button.draw():
            main_menu = False
    else:
        
        worldCurrent.draw()

        if game_over == 0:
            blob_group.update() #moves enemies
            flyer1_group.update()

        blob_group.draw(screen)
        spike_group.draw(screen)
        flyer1_group.draw(screen)

        #game over is a global var so it can't easily be accesed in a function cause it will look for a local var by name
        #of game_over which doesnt exist so the player update function, takes game_over as an input so that the same game_over
        #can be used as both a local and global variable with respect to the player update function
        #the update function then returns the game_over variable to allow the global game_over variable to be changed by the 
        #local game_over var that is created in update function
        game_over = player.update(game_over)

        if game_over == -1:
            if restart_button.draw():
                player.reset(100,screen_height-130)
                game_over = 0

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #looking for when you press 'x' in top right of window to close it
            run = False  #turns off game loop when you quit it, MAKES SURE GAME DOES NOT RUN WIThOUT A SCREEN 

    pygame.display.update()

pygame.quit() #once game loop is turned off the, code after the loop can run; here the game ends
