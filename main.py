import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
score = 0 

font = pygame.font.Font(None, 36)

def game_over():
    screen.fill("black")
    text = font.render("Game Over! Press R to Restart", True, (255, 255, 255))
    screen.blit(text, (500, 350))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return 


class Block:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def get_coordinates(self):
        return self.x, self.y, self.width, self.height

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class SpaceShip:
    def __init__(self):
        self.space_ship = Block(600, 600, 50, 50, (0, 0, 255))
        self.missiles = []

    def draw(self, surface):
        self.space_ship.draw(surface)
        for missile in self.missiles:
            missile.draw(surface)

    def get_spaceship(self):
        return self.space_ship

    def send_missile(self):
        x, y, width, height = self.space_ship.get_coordinates()
        new_missile = Block(x + width // 2 - 5, y, 10, 10, (255, 0, 0))
        self.missiles.append(new_missile)

    def move_missiles_up(self, step):
        for missile in self.missiles:
            missile.move(0, step)

    def remove_out_of_bounds_missiles(self):
        self.missiles = [missile for missile in self.missiles if missile.y > -10]


class Enemy:
    def __init__(self):
        self.enemies = []
        self.missiles = []

    def draw(self, surface):
        for enemy in self.enemies:
            enemy.draw(surface)
        for missile in self.missiles:
            missile.draw(surface)

    def move_enemies_down(self, step):
        for enemy in self.enemies:
            enemy.move(0, step)

    def move_missiles_down(self, step):
        for missile in self.missiles:
            missile.move(0, step)

    def generate_enemy(self):
        new_enemy = Block(random.randint(50, 1200), 100, 50, 50, (0, 255, 255))
        self.enemies.append(new_enemy)

    def send_missile(self):
        for enemy in self.enemies:
            x, y, width, height = enemy.get_coordinates()
            new_missile = Block(x + width // 2 - 5, y + height, 10, 10, (255, 0, 0))
            self.missiles.append(new_missile)

    def remove_out_of_bounds(self):
        self.enemies = [enemy for enemy in self.enemies if enemy.y < 720]
        self.missiles = [missile for missile in self.missiles if missile.y < 720]


space_ship = SpaceShip()
enemies = Enemy()

MOVE_ENEMIES_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_ENEMIES_EVENT, 1000)

GENERATE_ENEMIES_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(GENERATE_ENEMIES_EVENT, 5000)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == MOVE_ENEMIES_EVENT:
            enemies.move_enemies_down(10)
            enemies.move_missiles_down(20)
            space_ship.move_missiles_up(-20)
            space_ship.remove_out_of_bounds_missiles()
            enemies.remove_out_of_bounds()

        if event.type == GENERATE_ENEMIES_EVENT:
            enemies.generate_enemy()
            enemies.send_missile()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        space_craft = space_ship.get_spaceship()
        if space_craft.x > 0:
            space_craft.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        space_craft = space_ship.get_spaceship()
        if space_craft.x + space_craft.width < 1280:
            space_craft.move(5, 0)
    if keys[pygame.K_SPACE]:
        space_ship.send_missile()


    for missile in space_ship.missiles:
        mx, my, mw, mh = missile.get_coordinates()
        for enemy in enemies.enemies:
            ex, ey, ew, eh = enemy.get_coordinates()
            if mx < ex + ew and mx + mw > ex and my < ey + eh and my + mh > ey:
                enemies.enemies.remove(enemy)
                space_ship.missiles.remove(missile)
                score += 10
                break

    for missile in enemies.missiles:
        mx, my, mw, mh = missile.get_coordinates()
        sx, sy, sw, sh = space_ship.get_spaceship().get_coordinates()
        if mx < sx + sw and mx + mw > sx and my < sy + sh and my + mh > sy:
            game_over()
            score = 0
            enemies = Enemy()
            space_ship = SpaceShip()


    screen.fill("purple")


    space_ship.draw(screen)
    enemies.draw(screen)


    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


    pygame.display.flip()


    clock.tick(60)

pygame.quit()
