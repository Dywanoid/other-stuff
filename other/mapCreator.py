import pygame
from itertools import product

# ILE NA ILE MA BYC MAPA
tiles_x = 30
tiles_y = 30
# WYMIAR KWADRATOW NA EKRANIE (TYLKO W TYM EDYTORZE)
tile_size = 20
# KOLORY JAKO STANY, TYLE ILE CHCESZ STANOW TYLE DAJ ROZNYCH KOLOROW, KOLORY DAJEMY W TUPLE JAKO RGB
COLORS = ((255, 255, 255), (0, 0, 0), (150, 150, 150), (21, 37, 143))
# False JEŚLI EDYTUJESZ JEDNĄ MAPĘ, True JESLI CHCESZ WYCZYŚCIC I ZACZAC OD NOWA
nowa = False

pygame.init()
WINDOW_HEIGHT = tile_size * tiles_y
WINDOW_WIDTH = tile_size * tiles_x

FPS = 60
gameWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Kreator')
clock = pygame.time.Clock()


class Tile:
    def __init__(self, x, y, s=0):
        self.x = x * tile_size
        self.y = y * tile_size
        self.state = s
        self.color = COLORS[self.state]

    def change_state(self, t):
        if t - 1 == self.state:
            self.state += 1
            if self.state == len(COLORS):
                self.state = 0
            self.change_color()

    def change_color(self):
        self.color = COLORS[self.state]

    def __str__(self):
        return 'x: {} y: {}'.format(self.x / tile_size, self.y / tile_size)


def draw_tiles():
    for tile in tiles:
            pygame.draw.rect(gameWindow, tile.color, (tile.x, tile.y, tile_size, tile_size))


def save():
    text_file = open("mapa", "w")
    text_file.write(" ".join([str(tile.state) for tile in tiles]))
    text_file.close()


tiles = [Tile(x, y) for y, x in product(range(tiles_y), range(tiles_x))]
if not nowa:
    file = ''.join(open("mapa", "r").read().split(' '))
    print(file)
    for index, state in enumerate(file):
        tiles[index].state = int(state)
        tiles[index].change_color()

rysowanie = False
crashed = False
ev = None
typ = None
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
            save()
        if event.type == pygame.MOUSEBUTTONDOWN:
            rysowanie = True
            typ = tiles[tiles_x * (ev.pos[1] // tile_size) + (ev.pos[0] // tile_size)].state + 1
        if event.type == pygame.MOUSEBUTTONUP:
            rysowanie = False
        if event.type == pygame.MOUSEMOTION:
            ev = event
    if rysowanie and ev != None:
        tiles[tiles_x * (ev.pos[1] // tile_size) + (ev.pos[0] // tile_size)].change_state(typ)
        typ = tiles[tiles_x * (ev.pos[1] // tile_size) + (ev.pos[0] // tile_size)].state
    gameWindow.fill((30, 10, 50))
    draw_tiles()
    pygame.display.update()
    clock.tick(60)
