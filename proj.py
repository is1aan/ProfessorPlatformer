import pygame
import pygame.freetype
from pygame.locals import *



pygame.init()
pygame.font.init()

#sets fps
clock = pygame.time.Clock()
fps = 60
#set game/global variables
screen_width = 800
screen_height = 800
tile_size = screen_height/20
winScreen = False
game_over = 0
main_menu = True
level = 0

font = pygame.font.Font(None, 32)
color = pygame.Color('chartreuse4')

screen =  pygame.display.set_mode((screen_width, screen_height)) #makes screen
pygame.display.set_caption('67platformer67')  #name for the screen in the top header bar

class Button():
    def __init__(self,x,y, image = None,option = None,string = None):
        self.image = image
        self.rect = pygame.Rect(tile_size, tile_size, tile_size*2, tile_size*2) 
        if image != None:
            self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.option  = option
        self.str = string
    
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
    #similar to .draw but to render a string instead of an image since getting a new image for every button takes time
    def drawStr(self):
        action  = False

        pos = pygame.mouse.get_pos()
        
        #creates a colored background equal to size of button and draws a string on it that is displayed to player
        input_rect = pygame.Rect(self.rect.x, self.rect.y, tile_size*2, tile_size*2)
        pygame.draw.rect(screen, color, input_rect)
        txt_surface = font.render(self.str,True, (255, 255, 255))
        screen.blit(txt_surface, (input_rect.x+5, input_rect.y+5))
        
        #draws hitbox of button, mostly for debugging but also looks nice
        pygame.draw.rect(screen,(0,0,0),self.rect,2)

        if self.rect.collidepoint(pos):
            #getpressed function returns list that has left, right and middle mouse click where left mouse click is 0th index
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action  = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
#for visualizing how blocks can be placed by drawing a grid, for testing/coding, not in main game
def draw_grid():
    for line in range(0,20): 
        pygame.draw.line(screen, (255,255,255),(0, line *tile_size),(screen_width,line*tile_size))
        pygame.draw.line(screen, (255,255,255),( line *tile_size,0),(line*tile_size,screen_width))
#loads level
def load_level(level): 
    worldCurrent.update(level)


class Player():
    def __init__(self,x,y):
        self.reset(x,y)
    
    def update(self, game_over):
        #what the player is GOING to move
        dx = 0
        dy = 0

        if game_over == 0:

            #get key presses
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped ==False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True  
            elif key[pygame.K_UP] == False:
               self.jumped = False
            if key[pygame.K_LEFT] and self.rect.x >0:
                dx -= 3
            if key[pygame.K_RIGHT]  and self.rect.x < screen_width-(tile_size-15):
                dx += 3
        
        
            #add gravity 
            self.vel_y += 1   #base gravity value
            if self.vel_y >10: #stops you from infinetly accelerating when falling for too long, terminal velocity
                self.vel_y = 10

            dy += self.vel_y

            #check for collision
            #checks for collision at location player WILL move before actually letting player move
            #1. calculate new player pos
            #2. check collision at new pos
            #3. adjust player position
           
            self.in_air = True
            for tile in worldCurrent.tile_list:
                #check for collision in x direction
                #always use 1 since tile is a tuple and the hitbox is stored in the 1 index of the tile
                if tile[1].colliderect(self.rect.x +dx, self.rect.y,self.width,self.height):    
                    dx = 0
                    #if world !=1:
                        #adds a wall jump when you move on from world 1
                    if self.rect.top != tile[1].bottom:
                        self.in_air = False
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
               
            
            
            #for sprite in blob_group.sprites():
            #    if sprite.rect.top == self.rect.bottom and self.in_air == True:
            #        print("get goombad")
            #        self.vel_y = -15
            #        self.jumped = True  

            #check for collision with enemies     
            if pygame.sprite.collide_rect(self, pendar):
                print("asking")
                game_over = pendar.askQuestion(screen,game_over)
            
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1     
                #check for collision with spike
            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, flyer1_group, False):
                game_over = -1      
            if pygame.sprite.spritecollide(self, flyerv_Group, False):
                game_over = -1
       
        elif game_over == -1:
            self.image = self.dead_image
            
        #update player coords after checking for collision at future lucation
        self.rect.x +=dx
        self.rect.y +=dy
      
        #draw player on screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen,(0,0,0),self.rect,2)

        return game_over
    
    def reset (self,x = tile_size +10 ,y = screen_height-tile_size):
        #essentaially the initializer for the player, can be called multiple times, for when player dies
        img = pygame.image.load('img/player.png')
        dead = pygame.image.load('img/dead.png')
        self.image = pygame.transform.scale(img,(tile_size-15,tile_size-1 ))
        self.rect = self.image.get_rect()  #creates hitbox for player, alwasy attached to player
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped  = False
        self.dead_image =  pygame.transform.scale(dead, (tile_size-15,tile_size ))
        self.in_air = True

    


class World():
    def __init__(self, data):
        self.update(data)
    def draw(self):
        for tile in self.tile_list: #self.tile_list looks for the tile list from this created object and no other world objects
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen,(0,0,0),tile[1],2)

    def update(self, data):
        #essentially init function that can be ran many times
        self.tile_list = []
        
        #load images
        dirt_img = pygame.image.load('img/dirt.jpg')
        grass_img = pygame.image.load('img/grass.png')
        
        #loops through each col and row in world data list and checks its value, adds a corresponding tile to a list of tiles 
        #based on value at each location
        row_count = 0
        for row in data[0]:
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
                if tile == 6: #vertical flyer
                    flyer = FlyerV(col_count *tile_size, row_count *tile_size)
                    flyerv_Group.add(flyer)
                if tile == 7: #not used
                    wallR = wallSpikeR()  
                if tile == 9: #game goal
                    pendar.update(col_count *tile_size, row_count *tile_size, data[1], data[2])
                col_count += 1
            row_count +=1

    def nextLevel (self, level,gameOver):
        #clears all entities and prepares world for the next level
        blob_group.empty()
        spike_group.empty()
        flyer1_group.empty()
        flyerv_Group.empty()
    
        if level == 1:
            self.update(world1_data)
        if level == 2:
            self.update(world2_data)
        if level == 3:
            self.update(world3_data)
        if level == 4:
            self.update(world4_data)
        if level == 5:
            self.update(world5_data)
        if level ==6:
            gameOver = 0
            
        return gameOver
            


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        Eimg = pygame.image.load('img/enemy.png')
        
        self.image = pygame.transform.scale(Eimg, (tile_size-5, tile_size-5))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y+5
        self.move_direction = 1
        self.move_counter = 0

    def update (self):
        #moves the enemy left a certain distance a certain number of times until it swaps direction and moves backwards a certain number of times
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > tile_size-5:
            self.move_direction *= -1
            self.move_counter *= -1

#similar to enemy class with differen variables, moves further
class FlyerH(pygame.sprite.Sprite):
    def __init__(self, x,y,numTiles = 5):
        pygame.sprite.Sprite.__init__(self)
        Eimg = pygame.image.load('img/enemy.png') #CHANGE IMAGE
        
      
        self.image = pygame.transform.scale(Eimg, (tile_size-5, tile_size-5))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 3
        self.move_counter = 0
        self.range = numTiles/self.move_direction * 1.5 * tile_size

    def update (self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > self.range:
            self.move_direction *= -1
            self.move_counter *= -1
#similar to enemy class with differen variables, moves further
class FlyerV(pygame.sprite.Sprite):
    def __init__(self, x,y,numTiles = 1):
        pygame.sprite.Sprite.__init__(self)
        Eimg = pygame.image.load('img/enemy.png') #CHANGE IMAGE
      
        self.image = pygame.transform.scale(Eimg, (tile_size, tile_size))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 4
        self.move_counter = 0
        self.range = numTiles/self.move_direction * 1.5 * tile_size

    def update (self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if self.move_counter > self.range:
            self.move_direction *= -1
            self.move_counter *= -1
#similar to enemy class except it doesnt move
class Spike(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        Eimg = pygame.image.load('img/spike.png')
        
        self.image = pygame.transform.scale(Eimg, (tile_size - 15, tile_size - 15))
        self.rect= self.image.get_rect()
        self.rect.x = x + 6
        self.rect.y = y + 15
#not used
class wallSpikeR(pygame.sprite.Sprite):
    def __init__(self, x,y,rotation):
        pygame.sprite.Sprite.__init__(self)
        Eimg = pygame.image.load('img/spike.png')
        
        self.image = pygame.transform.scale(Eimg, (tile_size - 15, tile_size - 15))
        self.image = pygame.transform.rotate(self.image,-90)
        self.rect= self.image.get_rect()
        self.rect.x = x + 6
        self.rect.y = y + 15
        self.rotation = rotation
#goal of the game
class Pendar(pygame.sprite.Sprite):
    def __init__(self, x,y , question, answer):
        self.update(x,y,question,answer)
    
    def askQuestion(self, screen,game_over):
        #changes game state to wher enemies dont move but question is still rendered
        game_over = 1
        #load fond
        font = pygame.freetype.SysFont("sans", 20)
        #make rectangle to make text stand out
        input_rect = pygame.Rect(200, 300, 400, 200)
        pygame.draw.rect(screen, color, input_rect)
        
        #since \n does not work, this splits the question along the - key and for each element in the split list it
        #prints the element in the list but a little but further down for each loop of for loop
        QList = self.question.split("-")
        for i in range(len(QList)):
            txt2_surface = font.render(QList[i], (0, 0, 0))
           
            screen.blit(txt2_surface[0], (input_rect.x+5 , input_rect.y+5+ i*20))
        

        return game_over

    def update(self, x , y , question,answer):
        
        pygame.sprite.Sprite.__init__(self)
        if level <=2:
            Eimg = pygame.image.load('img/Pendar.png')
        elif level <5:
            Eimg = pygame.image.load('img/boxin.png')
        else:
            Eimg = pygame.image.load('img/aucoin.png')
        self.image = pygame.transform.scale(Eimg, (tile_size - 10, tile_size - 10))
        self.rect= self.image.get_rect()
        self.rect.x = x + 4
        self.rect.y = y + 10
        self.question = question
        self.ans = answer
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x,self.rect.y))
    #i forgot why I added this and It seems like its never used but im too scared to remove it
    def answer (self,answer):
        self.ans = answer.lower()
    def guess(self, guess, game_over):
        if self.ans == guess.lower():
            game_over = 2
        else:
            game_over = -1
        return game_over
    
       


#blueprint for making world, a tuple with a list, string, and string
#each number in list corresponds to a type of block and the first string is the question for the level and the second string is the answer


#worldAsFile = open(f"level{level}_data.txt")
#world_data = [worldAsFile.read()]
#print(worldAsFile)
#print(worldAsFile.read())

worldTest_data = ([
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #2
  [0,0,0,0,4,0,0,4,0,0,0,0,0,3,0,0,0,0,0,0], #3
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
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #19 
  [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]  #20
  ],
   'pendar question',
   "a"
)
world1_data = (
    [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #2
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #3
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #4
    [0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0], #5
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
    ],
    'Which logic statement returns True?-a: True and False-b: True or False-c: True or False and False',  #pendars question
    "b"  #answer for pendars question
    
)
world2_data = ([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #t
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #3
    [2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9], #4
    [0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,2,2,2], #5
    [0,0,0,0,0,2,0,2,0,2,0,2,0,2,0,2,0,0,0,0], #6
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #7
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #8
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #9
    [0,0,0,0,0,2,4,4,4,4,4,4,4,4,4,4,4,4,4,4], #10
    [0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], #11
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #12
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #13
    [0,2,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0], #14
    [0,0,0,0,4,0,0,4,0,0,4,0,0,4,0,0,0,0,0,0], #15
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0], #16
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #17
    [0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,2,0], #18
    [0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0,0], #19
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], #20
    ],
    'Which object type is not immutable?-a: tuples-b: dictionaries-c: strings',  #pendars question 2
    "b"  #answer for pendars question
)



world3_data= ([
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #2
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #3
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #4
  [0,0,0,0,0,3,0,0,0,9,0,0,0,0,3,0,0,0,0,0], #5
  [0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0], #6
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #7
  [2,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2], #8
  [2,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0], #9 
  [2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,2], #10 
  [2,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,2], #11 
  [2,2,2,2,2,0,0,0,0,2,2,0,0,0,0,0,0,0,0,2], #12 
  [0,0,0,0,0,4,0,0,0,2,2,0,0,0,0,0,0,0,6,2], #13
  [0,0,0,2,2,2,2,0,2,0,0,2,0,2,2,2,2,2,0,2], #14 
  [0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0], #15
  [0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0], #16
  [0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0], #17
  [0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0], #18
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #19 
  [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]  #20
  ],
   'Which equation can be used to calculate mass of-a substance given pressure, volume, and temperature?-a: Ideal gas law-b: Clausius Clayperon-c: vant hOff',
   "a"
)
world4_data= ([
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #2
  [0,0,0,0,4,0,0,4,0,0,0,0,0,3,0,0,0,0,0,0], #3
  [0,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,0,2], #4
  [9,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2], #5
  [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2], #6
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2], #7
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2], #8
  [0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,2], #9 
  [0,0,0,2,2,2,2,2,0,0,0,2,2,2,2,0,2,2,0,2], #10 
  [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2], #11 
  [0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #12 
  [0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #13
  [0,2,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0], #14 
  [0,2,2,2,2,2,0,2,2,0,0,0,0,0,0,0,0,0,0,0], #15
  [0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0], #16
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0], #17
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #18
  [0,0,0,0,0,0,3,0,0,0,4,0,0,0,0,0,0,0,0,0], #19 
  [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]  #20
  ],
   'What is the effect of increasing pressure on vapor-liquid equilibrium?-a: Boiling point decrease-b: Boiling point increase-c: No change',
   "b"
)
world5_data = ([
  [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], #1
  [2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,2], #2
  [2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,2], #3
  [2,0,0,0,0,2,2,0,2,0,0,2,2,2,2,2,2,2,0,2], #4
  [2,0,0,0,0,0,2,0,2,0,0,2,0,0,0,0,0,0,0,2], #5
  [2,0,0,0,0,0,2,0,2,0,0,2,0,2,0,0,0,0,0,2], #6
  [2,0,0,0,0,2,2,0,2,0,0,2,0,2,6,2,0,0,0,2], #7
  [2,0,0,0,0,0,2,0,2,0,0,2,0,2,0,0,0,0,0,2], #8
  [2,6,0,0,0,0,2,0,2,0,0,2,0,2,0,0,0,4,0,2], #9 
  [2,0,0,0,0,2,2,0,2,0,9,2,0,2,2,2,2,2,2,2], #10 
  [2,0,0,4,0,0,2,0,2,2,2,2,0,0,0,0,0,0,0,2], #11 
  [2,0,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,0,2], #12 
  [2,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2], #13
  [2,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2], #14 
  [2,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2], #15
  [2,0,2,0,0,0,2,0,0,3,0,0,3,0,0,3,0,0,0,2], #16
  [2,0,2,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2], #17
  [2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2], #18
  [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2], #19 
  [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]  #20
  ],
   'What is the chemical reaction for making soap?-a: soaponfication-b: acid lypolisis-c: saponification',
   "c"
)

#load images
sky_img = pygame.image.load('img/placeholder.jpg') #looks for img folder inside of open folder and inside of img folder looks for placeholder.jpg
restart_img = pygame.image.load("img/restart.png")
start_img = pygame.image.load("img/start_btn.png")
backToMenu = pygame.image.load("img/menu.png")
exit_img = pygame.image.load("img/exit_btn.png")
a_img = pygame.image.load("img/a.png")
b_img = pygame.image.load("img/b.png")
c_img = pygame.image.load("img/c.png")

#creates objects and sprite groups
player = Player(tile_size +10 , screen_height-tile_size)
spike_group = pygame.sprite.Group()
blob_group = pygame.sprite.Group()
flyer1_group = pygame.sprite.Group()
flyerv_Group = pygame.sprite.Group()
pendar = Pendar(1 *tile_size, 1 *tile_size, "test question", "a")


#load  in level data and create world
#pickle_in = open(f'level{level}_data.text')
#world_data = pickle.load(pickle_in)

#first level
worldCurrent = World(world1_data)

#world2 = World(world2_data)

#create buttons
restart_button = Button(screen_width//2 -128 -50, screen_height//2 + 100, restart_img) 
start_button = Button(screen_width//2 -150, screen_height//2, start_img)
exit_button = Button(screen_width//2 +50, screen_height//2, exit_img)
menuButton = Button(screen_width//2 +50 , screen_height//2+100, backToMenu)
menuButtonWin = Button(screen_width//2-50, screen_height//2+100, backToMenu)
A_button = Button(300, 700, a_img)
B_button =  Button(400, 700, b_img)
C_button = Button(500, 700, c_img)
lvl1 = Button(128 +32,600,string="Level 1")
lvl2 = Button(228+32,600,string="Level 2")
lvl3 = Button(328+32,600,string="Level 3")
lvl4 = Button(428+32,600,string="Level 4")
lvl5 = Button(528+32,600,string="Level 5")


run = True
while run: #runs game
    clock.tick(fps) #restricts game to certain fps
    
    #draws loaded images
    #order images drawn matter because a larger image can cover a smaller image if smaller image is loaded first
    screen.blit(sky_img, (0,0))
    if main_menu:
        #shortcut to test win screen since beating level 5 every time got annoying
        ky = pygame.key.get_pressed()
        
        if ky[pygame.K_q]:
            print("plus")
            game_over = 0
            main_menu = False
            winScreen = True

        #level select buttons    
        if lvl1.drawStr() == True:
            level = 1
            print("button1")
            worldCurrent.nextLevel(level, game_over)
            game_over = 0
            main_menu = False
        if lvl2.drawStr() == True:
            print("button2")
            level = 2
            worldCurrent.nextLevel(level, game_over)
            game_over = 0
            main_menu = False
        if lvl3.drawStr() == True:
            print("button3")
            level = 3
            worldCurrent.nextLevel(level, game_over)            
            game_over = 0
            main_menu = False
        if lvl4.drawStr() == True:
            print("button4")
            level = 4
            worldCurrent.nextLevel(level, game_over)            
            game_over = 0
            main_menu = False
        if lvl5.drawStr() == True:
            print("button5")
            level = 5
            worldCurrent.nextLevel(level, game_over)
            game_over = 0
            main_menu = False
        
        if exit_button.draw() == True:
            run = False
        if start_button.draw():
            main_menu = False
        
        #main menu text box works same as AskQuestion from pendar class
        colorM = pygame.Color(214,170, 24)
        fnt = pygame.freetype.SysFont("sans", 50)
        #make rectangle to make text stand out
        input_rect = pygame.Rect(screen_height//2-100, screen_width//2-100,230, 50)
        pygame.draw.rect(screen, colorM, input_rect)
        
        text_surface = fnt.render("Main Menu", (0, 0, 0))
        screen.blit(text_surface[0], (input_rect.x+5 , input_rect.y+5))
    elif winScreen:
        #win text box works same as AskQuestion from pendar class
        win_rect = pygame.Rect(screen_height//2-50, screen_width//2, 100, 50)
        pygame.draw.rect(screen, color, win_rect)
        win_surface = font.render("you win!", True, (255, 255, 255))
        screen.blit(win_surface, (win_rect.x+5, win_rect.y+5))
        if menuButtonWin.draw():
            print("menuPressed")
            player.reset()
            main_menu = True
    else:
      
        worldCurrent.draw()
        #game running
        if game_over == 0:
            blob_group.update() #moves enemies
            flyer1_group.update()
            flyerv_Group.update()
            pendar.draw(screen)
            blob_group.draw(screen)
            spike_group.draw(screen)
            flyer1_group.draw(screen)
            flyerv_Group.draw(screen)
            game_over = player.update(game_over)

        
        #answering question
        if game_over == 1:
            game_over = player.update(game_over)

            pendar.draw(screen)
            blob_group.draw(screen)
            spike_group.draw(screen)
            flyer1_group.draw(screen)
            game_over = pendar.askQuestion(screen,game_over)
            #game over is a global var so it can't easily be accesed in a function cause it will look for a local var by name
            #of game_over which doesnt exist so the player update function, takes game_over as an input so that the same game_over
            #can be used as both a local and global variable with respect to the player update function
            #the update function then returns the game_over variable to allow the global game_over variable to be changed by the 
            #local game_over var that is created in update function
            #use similar methods for variabels throught the code
            if A_button.draw() == True:
                game_over = pendar.guess("a",game_over)
            if B_button.draw() == True:
                game_over = pendar.guess("b", game_over)
            if C_button.draw() == True:
                game_over = pendar.guess("c", game_over)
        
        #add level increments, if question is right
        if game_over == 2:
            level +=1
            player.reset()
            game_over = worldCurrent.nextLevel(level, game_over)
            game_over = 0
            
            if level == 6:
                main_menu = False
                winScreen = True
      
          

      
        
        
        #game over
        if game_over == -1:
            player.update(game_over)
            input_rect = pygame.Rect(screen_height//2-50, screen_width//2, 100, 50)
            pygame.draw.rect(screen, color, input_rect)
            text_surface = font.render("you lose!", True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))

            if restart_button.draw():
                print("restart")
                player.reset()
                game_over = 0
            if menuButton.draw():
                print("menuPressed")
                player.reset()
                main_menu = True

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #looking for when you press 'x' in top right of window to close it
            run = False  #turns off game loop when you quit it, MAKES SURE GAME DOES NOT RUN WIThOUT A SCREEN 

    pygame.display.update()

pygame.quit() #once game loop is turned off the, code after the loop can run; here the game ends




