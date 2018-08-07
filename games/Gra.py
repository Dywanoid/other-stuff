import pygame
import random
import math
import time

class Game:
    player = {}
    def __init__(self):
        self.targets = []
        self.shots = []
        self.to_erase = []
        self.points = 0

    def new_shot(self, missile):
        self.shots.append(missile)

    def new_target(self, target):
        self.targets.append(target)

    def new_player(self, player):
        self.player = player


class GameObject:
    def __init__(self, graphic, width, height):
        self.x = 10
        self.y = 10
        self.graphic = pygame.image.load(graphic)
        self.width = width
        self.height = height
        self.speedx = 0
        self.speedy = 0
        self.can_collide = True

    def update(self):
        self.x += self.speedx
        self.y += self.speedy

    def check_collision(self, t):
        if t.x <= self.x <= t.x + t.width and t.y <= self.y <= t.y + t.height and self.can_collide and not t.hit:
            self.can_collide = False
            return True
        elif t.x <= self.x + self.width <= t.x + t.width and t.y <= self.y \
                + self.height <= t.y + t.height and self.can_collide and not t.hit:
            self.can_collide = False
            return True
        return False


class Missile(GameObject):
    def __init__(self, graphic, width, height, obj):
        GameObject.__init__(self, graphic, width, height)
        self.x = obj.x + obj.width//2 - self.width//2
        self.y = obj.y
        self.speedy = -10
        self.speedx = 0


class Target(GameObject):
    def __init__(self, graphic, width, height):
        GameObject.__init__(self, graphic, width, height)
        self.speedy = 3
        self.speedx = 0
        self.countdown = 30
        self.hit = False

    def boom(self, game):
        self.graphic = pygame.image.load('data\img\snowhit_t.png')
        self.speedx *= -1/3
        self.hit = True
        if self not in game.to_erase:
            game.to_erase.append(self)

    def timer(self, game):
        self.countdown -= 1
        if not self.countdown:
            game.points += 1
            game.to_erase.remove(self)
            game.targets.remove(self)

    '''def change_direction(self):
        if self.x + self.width > WINDOW_WIDTH:
            self.speedx *= -1
            self.y += self.height
        elif self.x <= 0:
            self.speedx *= -1
            self.y += self.height
        ''' # change direction function

    def check_over(self, player):
        if self.y + self.height > WINDOW_HEIGHT - player.height:
            return True
        return False


class Player(GameObject):
    def __init__(self, graphic, width, height):
        GameObject.__init__(self, graphic, width, height)
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - self.height
        self.speedx = 0
        self.speedy = 0
        self.shooting_speed = 0.15
        self.can_shoot = True
        self.shooting_tick = math.floor(FPS * self.shooting_speed)

    def cooldown(self):
        if not self.can_shoot:
            self.shooting_tick -= 1
        if not self.shooting_tick:
            self.can_shoot = True
            self.shooting_tick = math.floor(FPS * self.shooting_speed)

    def shoot(self, game):
        if self.can_shoot:
            game.new_shot(Missile('data\img\star_t.png', 20, 20, Game.player))
            self.can_shoot = False
            self.cooldown()
        else:
            self.cooldown()


pygame.init()
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 400
FPS = 60
gameWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Szoty')
clock = pygame.time.Clock()

Game = Game()

Game.new_player(Player('data\img\player_t.png', 60, 80))


def make(game):
    can = True
    if math.floor(random.random()*(100 - math.floor(game.points*0.02))) < 5:
        for target in game.targets:
            if target.x < target.width and target.y < target.height:
                can = False
        if can:
            temp = Target('data\img\snow_t.png', 50, 50)
            temp.x = (random.random()*(WINDOW_WIDTH - temp.width))
            temp.y = -temp.height
            game.new_target(temp)


def draw(obj):
    gameWindow.blit(obj.graphic, (obj.x, obj.y))


def updating(game):
    moving_objects(game)
    checking_collision(game)
    checking_over(game)
    destroying_hit(game)
    make(game)
    shooting_cooldown(game.player)
    game.player.update()
    pygame.display.set_caption('Szoty     Punkty: ' + str(game.points*10))


def moving_objects(game):
    for x in game.targets:
        x.update()
        # x.change_direction()
    for y in game.shots:
        y.update()


def checking_collision(game):
    for shot in game.shots:
        for target in game.targets:
            if shot.check_collision(target):
                target.boom(game)
                game.shots.remove(shot)


def checking_over(game):
    for target in game.targets:
        if target.check_over(game.player):
            game_over()


def game_over():
    print('koniec')


def destroying_hit(game):
    for cds in game.to_erase:
        cds.timer(game)


def drawing(game):
    draw(game.player)
    for x in game.targets:
        draw(x)
    for y in game.shots:
        draw(y)

def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WINDOW_WIDTH/2), (WINDOW_HEIGHT/2))
    gameWindow.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)


def shooting_cooldown(player):
    player.cooldown()


crashed = False
dol, gora, lewo, prawo = False, False, False, False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEMOTION:
            Game.player.x = event.pos[0] - Game.player.width//2
        if event.type == pygame.MOUSEBUTTONDOWN:
            Game.player.shoot(Game)

        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lewo = True
                print('lewo')
            elif event.key == pygame.K_RIGHT:
                prawo = True
                print('prawo')
            elif event.key == pygame.K_UP:
                # Game.new_shot(Missile(shots_pics[math.floor(random.random()*2)], 30, 40, Game.player))
                Game.player.shoot(Missile('shot3.png', 17, 35, Game.player), Game)
                # Game.new_shot(Missile('shot3.png', 17, 35, Game.player), Game.player)
            elif event.key == pygame.K_DOWN:
                make(Game, 1)
                message_display('XD')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                lewo = False
                prawo = False
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                gora = False
                dol = False
    if lewo and Game.player.x > 5:
        Game.player.speedx = -5
    elif prawo and Game.player.x + Game.player.width < WINDOW_WIDTH:
        Game.player.speedx = 5
    else:
        Game.player.speedx = 0
    '''




    gameWindow.fill((31, 12, 51))
    updating(Game)
    drawing(Game)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
