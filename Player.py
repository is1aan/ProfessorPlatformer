import pygame
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
                #reset jump when touching top of block, makes you able to stick to bottom of blocks for some reason 
                
                
                #if self.rect.bottom == tile[1].top and self.rect.top != tile[1].bottom:
                    #print("double jump")
                    self.jumped = False
                #if self.rect.right == tile[1].left: 
                    #print("double jump")
                    self.jumped = False
                #if self.rect.left == tile[1].right:
                    #print("double jump")
                    self.jumped = False

            #check for collision with enemies 
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1 

                #check for collision with spike
            if pygame.sprite.spritecollide(self, spike_group, False):
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
