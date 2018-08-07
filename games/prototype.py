import pygame
import time
from random import random
from math import floor


# Constants
SCREEN_RATIO = 10 * 4  # Change this second number to change screen size
WINDOW_WIDTH = 9 * SCREEN_RATIO
WINDOW_HEIGHT = 16 * SCREEN_RATIO
fps = 60
COLORS = ((255, 255, 255), (0, 0, 0), (floor(random() * 256), floor(random() * 256), floor(random() * 256)),
          (floor(random() * 256), floor(random() * 256), floor(random() * 256)),
          (floor(random() * 256), floor(random() * 256), floor(random() * 256)))
FIELDS = 5
WALLS_COLOR = (184, 184, 148)


# Classes
class Game:
    def __init__(self):
        self.tiles = []
        self.game_speed = 2
        self.player = Player()
        self.walls = 0
        self.score = 0
        self.can_speed_up = True

    def start(self):
        for _ in range(11):
            self.new_tile()
        self.player.on_tile = self.tiles[0]
        self.player.next_tile = self.tiles[1]

    def new_tile(self):
        if len(self.tiles):
            t = Tile()
            t.y = self.tiles[-1].y - t.height
            self.tiles.append(t)
        else:
            self.tiles.append(Tile())

    def tiles_movement(self):
        for tile in self.tiles:
            tile.move(self.game_speed)

    def check_tiles(self):
        if self.tiles[0].y > WINDOW_HEIGHT:
            self.new_tile()
            self.tiles.pop(0)

    def update(self):
        self.tiles_movement()
        self.check_tiles()
        self.player.jump()
        self.player.move(self)

        if self.score and not self.score % 5 and self.score % 6 and self.can_speed_up:
            self.speed_up()
            self.can_speed_up = False
        if self.score and not self.score % 6:
            self.can_speed_up = True

    def direction_change(self, direction):
        for tile in self.tiles:
            tile.change(direction)

    def place_wall(self):
        self.walls += 1

    def speed_up(self):
        if self.can_speed_up:
            global fps
            fps += 1


class Tile:
    def __init__(self):
        self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT // 10
        self.x, self.y = 0, 0
        self.color = (random() * 250, random() * 250, random() * 250)
        self.colors = [floor(random()*5) for _ in range(FIELDS)]
        self.colors_check()
        self.can_move = True

    def move(self, speed):
        self.y += speed

    def change(self, direction):
        if self.can_move:
            if direction:  # right
                x = self.colors.pop()
                self.colors.insert(0, x)
            else:  # left
                self.colors.append(self.colors.pop(0))

    def colors_check(self):
        if 2 not in self.colors:
            self.colors[floor(random() * 5)] = 2


class Player:
    def __init__(self):
        self.width, self.height = 50, 50
        self.x, self.y = WINDOW_WIDTH // 2 - self.width // 2, WINDOW_HEIGHT - self.height * 1.5
        self.graphic = pygame.image.load('data/img/p.png')
        self.graphic_displayed = self.graphic
        self.moving = False
        self.landing = False
        self.on_tile = Tile()
        self.next_tile = Tile()

    def jump(self):
        if not self.landing and not self.moving and self.on_tile.y+self.on_tile.height // 2 >= self.y+self.height // 2:
            self.moving = True
            self.graphic_displayed = pygame.transform.smoothscale(self.graphic, (60, 60))

    def move(self, game):
        if self.moving:
            self.y -= game.game_speed * 3
            if self.next_tile.y + self.next_tile.height // 2 >= self.y + self.height // 2:
                self.land(game)

        if not self.moving and self.landing:
            self.y += game.game_speed
            if self. y >= WINDOW_HEIGHT - self.height * 1.5:
                self.landing = False
                self.tile_color_check(game)

    def land(self, game):
        self.tile_allocation(game)
        self.y = self.on_tile.y + self.on_tile.height // 2 - self.height // 2
        self.landing = True
        self.moving = False
        self.graphic_displayed = self.graphic

    def collision_check(self, tile):
        if self.x + self.width >= tile.x and self.y + self.height >= tile.y and \
                tile.x + tile.width >= self.x and tile.y + tile.height >= self.y:
            return True
        return False

    def tile_allocation(self, game):
        for i, tile in enumerate(game.tiles):
            if self.collision_check(tile) and self.y <= tile.y + tile.height:
                tile.can_move = False
                self.on_tile = tile
                self.next_tile = game.tiles[i+1]
                break

    def tile_color_check(self, game):
        if self.on_tile.colors[2] != 2:
            game.place_wall()
        else:
            game.score += 1


# PyGame initialization and variables
pygame.init()
Display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Prototype')
clock = pygame.time.Clock()
Game = Game()
Game.start()
crashed = False


# Functions
def draw_tiles(game):
    for tile in game.tiles:
        pygame.draw.rect(Display, tile.color, (tile.x, tile.y, tile.width, tile.height))
        for x in range(FIELDS):
            pygame.draw.rect(Display, COLORS[tile.colors[x]],
                             (tile.x + x * (WINDOW_WIDTH / FIELDS), tile.y, WINDOW_WIDTH / FIELDS, tile.height))


def draw_walls(game):
    for y in range(game.walls):
        pygame.draw.rect(Display, WALLS_COLOR, (0, y * WINDOW_HEIGHT // 10, WINDOW_WIDTH, WINDOW_HEIGHT // 10))


def draw_player(game):
    Display.blit(game.player.graphic_displayed, (game.player.x, game.player.y))


def update(game):
    game.update()
    draw_tiles(game)
    draw_player(game)
    draw_walls(game)


def text_objects(text, font):
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()


def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 115)
    text_surface, text_rectangle = text_objects(text, large_text)
    text_rectangle.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))
    Display.blit(text_surface, text_rectangle)
    pygame.display.update()
    time.sleep(2)


def start():
    global crashed
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Game.direction_change(1)
                elif event.key == pygame.K_RIGHT:
                    Game.direction_change(0)
                    # message_display('xD')
                '''
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Game.direction_change(1)
                if event.button == 3:
                    Game.direction_change(0)
                    '''
        pygame.display.set_caption('Prototype ' + str(Game.score) + '  ' + str(floor(clock.get_fps())) + ' ' + str(fps))
        Display.fill(COLORS[2])
        update(Game)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()


# Starting the game
start()
