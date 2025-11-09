import pygame
from pygame.locals import *

pygame.init()

#sets fps
clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800
tile_size = screen_height/10

screen =  pygame.display.set_mode((screen_width, screen_height)) #makes screen
pygame.display.set_caption('67platformer67')  #name for the screen in the top header bar

def draw_grid():
    for line in range(0,10): 
        pygame.draw.line(screen, (255,255,255),(0, line *tile_size),(screen_width,line*tile_size))
        pygame.draw.line(screen, (255,255,255),( line *tile_size,0),(line*tile_size,screen_width))

class Player():
    def __init__(self,x,y):
        img = pygame.image.load('img/player.webp')
        self.image = pygame.transform.scale(img,(60,80))
        self.rect = self.image.get_rect()  #creates hitbox for player, alwasy attached to player
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped  = False
 

    def update(self):
        
        dx = 0
        dy = 0

        
        #get key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.jumped ==False:
            self.vel_y = -15
            self.jumped = True  
        if key[pygame.K_UP] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 3
        if key[pygame.K_RIGHT]:
            dx += 3
       
       
        #add gravity 
        self.vel_y += 1
        if self.vel_y >20:
            self.vel_y = 1

        dy += self.vel_y

        #check for collision
        #1. calculate new player pos
        #2. check collision at new pos
        #3. adjust player position
        for tile in world1.tile_list:
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
            
        #update player coords
        self.rect.x +=dx
        self.rect.y +=dy

        if self.rect.bottom > screen_height: #check if player off screen
            self.rect.bottom  =screen_height
            dy = 0
        #draw player on screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen,(255,255,0),self.rect,2)

    


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
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))  #makes image of dirt cube
                    img_rect = img.get_rect()   #makes the dirt image actually have a bounds
                    img_rect.x = col_count *tile_size
                    img_rect.y = row_count *tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))  #makes image of grass cube
                    img_rect = img.get_rect()   #makes the dirt image actually have a bounds
                    img_rect.x = col_count *tile_size
                    img_rect.y = row_count *tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count +=1
    def draw(self):
        for tile in self.tile_list: #self.tile_list looks for the tile list from this created object and no other world objects
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen,(0,0,0),tile[1],2)


#blueprint for making world, every 1 will be a block and it matches 10x10 grid
world1_data = [
    [0,0,0,0,0,0,0,0,0,0], #1
    [0,0,0,0,0,0,0,0,0,0], #2
    [0,0,0,0,0,0,0,0,0,0], #3
    [0,0,0,0,0,0,0,0,0,0], #4
    [0,0,0,0,0,0,0,0,0,0], #5
    [2,0,0,0,0,0,0,0,0,0], #6
    [0,0,2,2,2,2,2,0,0,0], #7
    [0,0,0,0,0,0,0,0,2,2], #8
    [0,0,0,0,0,0,0,2,1,1], #9
    [2,2,2,2,2,2,2,1,1,1], #10
]

#load images
player_img = pygame.image.load('img/placeholder.jpg') #looks for img folder inside of open folder and inside of img folder looks for placeholder.jpg

player = Player(100,screen_height - 160)
world1 = World(world1_data)


run = True
while run: #runs game
    clock.tick(fps) #restricts game to certain fps
    
    #draws loaded images
    #order images drawn matter because a larger image can cover a smaller image if smaller image is loaded first
    screen.blit(player_img, (0,0))

    #draw_grid()
    world1.draw()
    player.update()

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #looking for when you press 'x' in top right of window to close it
            run = False  #turns off game loop when you quit it, MAKES SURE GAME DOES NOT RUN WIThOUT A SCREEN 

    pygame.display.update()

pygame.quit() #once game loop is turned off the, code after the loop can run; here the game ends
