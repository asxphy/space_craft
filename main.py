import pygame
import random 
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


    
class Block:
    def __init__(self,x,y,width,height,color):
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.color = color 

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,(self.x,self.y,self.width,self.height))

    def get_corrdinates(self):
        return (self.x,self.y)

    def move(self,dx,dy):
        self.x +=dx 
        self.y +=dy

# class SpaceShip:
#     def __init__(self):

    
space_ship = Block(600,600,50,50,"BLUE")


class Enemy:
    def __init__(self):
        self.enemies = []
        self.missiles = []

    def draw(self,surface):
        for enemy in self.enemies:
            enemy.draw(surface)
        for missile in self.missiles:
            missile.draw(surface)

    def move_enemies_down(self,step):
        for enemy in self.enemies:
            enemy.move(0,step)

    def move_missile_down(self,step):
        for enemy in self.missiles:
            enemy.move(0,step)

    def generate_enemy(self):
        new_enemy = Block(random.randint(50,1000),100,50,50,(0,255,255))
        self.enemies.append(new_enemy)

    def send_missile(self):
        for enemy in self.enemies:
            x,y = enemy.get_corrdinates()
            new_missile = Block(x+20,y+20,10,10,(255,0,0))
            self.missiles.append(new_missile)  

          
    
    
enemies = Enemy()
enemies.generate_enemy()

MOVE_ENEMIES_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_ENEMIES_EVENT, 1000) 

GENERATE_ENEMIES_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(GENERATE_ENEMIES_EVENT, 5000) 

LAUNCH_MISSILE_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(LAUNCH_MISSILE_EVENT, 5000) 




while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == MOVE_ENEMIES_EVENT:
            enemies.move_enemies_down(10)
            enemies.move_missile_down(20)

        if event.type == GENERATE_ENEMIES_EVENT:
            enemies.generate_enemy()
            enemies.send_missile()

        # if event.type == LAUNCH_MISSILE_EVENT:
            

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        space_ship.move(-5,0)
    if keys[pygame.K_RIGHT]:
        space_ship.move(5,0)
    space_ship.draw(screen)
    enemies.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()