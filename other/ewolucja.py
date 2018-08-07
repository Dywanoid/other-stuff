import pygame
from random import random
from math import floor


class World:
    def __init__(self):
        self.predators = []
        self.regions = [[] for _ in range(REGIONS*REGIONS)]
        self.regions_boundries = [[e for e in range(0, WINDOW_WIDTH + 1, WINDOW_WIDTH // REGIONS)],
                                  [e for e in range(0, WINDOW_HEIGHT + 1, WINDOW_HEIGHT // REGIONS)]]
        self.to_erase = []
        self.object_count = 0

    def new_entity(self):
        e = Entities()
        e.region_allocation(self)
        self.regions[e.region].append(e)
        self.object_count += 1

    def erase_entity(self, entity):
        self.to_erase.remove(entity)
        self.regions[entity.region].remove(entity)
        self.object_count -= 1

    def new_predator(self):
        self.predators.append(Predator())

    def region_swap(self, entity):
        a = entity.region
        entity.region_allocation(self)
        if a != entity.region:
            self.regions[a].remove(entity)
            self.regions[entity.region].append(entity)

    def new_born(self, mom, dad):
        colors = [(mom.color[a] + dad.color[a])//2 + floor(random() * 30 - 15) for a in range(3)]
        for c in range(3):
            if colors[c] > 255:
                colors[c] = 255
            elif colors[c] < 0:
                colors[c] = 0
        e = Entities()
        e.color = (colors[0], colors[1], colors[2])
        e.region_allocation(self)
        e.x = mom.x
        e.y = mom.y
        e.can_reproduce = False
        self.regions[e.region].append(e)
        self.object_count += 1


class GameObject:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.x = floor(random() * (WINDOW_WIDTH - self.width))
        self.y = floor(random() * (WINDOW_HEIGHT - self.height))
        self.dx = floor(random() * 6 - 3)
        self.dy = floor(random() * 6 - 3)
        self.color = (255, 255, 255)
        self.region = 0

    def move(self):
        if self.x + self.dx + self.width >= WINDOW_WIDTH or self.x + self.dx <= 0:
            self.dx *= -1
        if self.y + self.dy + self.height >= WINDOW_HEIGHT or self.y + self.dy <= 0:
            self.dy *= -1

        self.y += self.dy
        self.x += self.dx

    def region_allocation(self, world):
        for a in range(1, REGIONS+1):
            for b in range(1, REGIONS+1):
                if world.regions_boundries[0][a-1] <= self.x < world.regions_boundries[0][a] and \
                        world.regions_boundries[1][b - 1] <= self.y < world.regions_boundries[1][b]:
                    self.region = (a-1) + REGIONS*(b-1)

    def collision_check(self, e):
        return True if self.x + self.width > e.x and self.y + self.height > e.y and \
                e.x + e.width > self.x and e.y + e.height > self.y else False


class Entities(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.color = (floor(random()*255), floor(random()*255), floor(random()*255))
        self.direction_change = floor(FPS*(3 + random()*2))
        self.mating = floor(FPS*(5 + random()*2))
        self.can_reproduce = True
        self.die = 10
        self.die_bool = False

    def change_speeds(self):
        self.dx = floor(random()*6 - 3)
        self.dy = floor(random()*6 - 3)

    def countdown(self):
        if not self.direction_change:
            self.change_speeds()
            self.direction_change = floor(FPS*(3 + random()*2))
        else:
            self.direction_change -= 1

        if not self.can_reproduce:
            if not self.mating:
                self.can_reproduce = True
                self.mating = floor(FPS*(5 + random()*2))
            else:
                self.mating -= 1

    def dying(self, world):
        self.die -= 1
        if not self.die:
            world.erase_entity(self)


class Predator(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.width = 30
        self.height = 30
        self.eating = COLORS

    def eat(self, entity):
        if self.eating[0] + eat_const >= entity.color[0] >= self.eating[0] - eat_const and \
                self.eating[1] + eat_const >= entity.color[1] >= self.eating[1] - eat_const and \
                self.eating[2] + eat_const >= entity.color[2] >= self.eating[2] - eat_const:
            return False
        return True


pygame.init()
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60
Window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Ewolucja')
clock = pygame.time.Clock()
eat_const = 50
REGIONS = 4
COLORS = (floor(random()*255), floor(random()*255), floor(random()*255))
trigger = False


def updating(world):
    check_collision(world)
    check_eat(world)

    for p in world.predators:
        move_object(p)
        p.region_allocation(world)
        draw_object(p)

    for r in range(len(world.regions)):
        for e in world.regions[r]:
            move_object(e)
            world.region_swap(e)
            e.countdown()

    for r in range(len(world.regions)):
        for e in world.regions[r]:
            draw_object(e)
    erase(world)
    pygame.display.set_caption('Ewolucja ' + str(world.object_count) + '  ' + str(floor(clock.get_fps())))


def draw_object(obj):
    pygame.draw.rect(Window, obj.color, (obj.x, obj.y, obj.width, obj.height))


def move_object(obj):
    obj.move()


def check_collision(world):
    for r in range(len(world.regions)):
        for e in world.regions[r]:
            if e.can_reproduce:
                for ch in world.regions[r][world.regions[r].index(e) + 1:]:
                    if ch.can_reproduce and e.collision_check(ch):
                            e.can_reproduce, ch.can_reproduce = False, False
                            reproduce(world, e, ch)


def reproduce(world, mom, dad):
    world.new_born(mom, dad)


def check_eat(world):
    for predator in world.predators:
        for entity in world.regions[predator.region]:
            if entity.collision_check(predator) and predator.eat(entity):
                world.to_erase.append(entity)


def erase(w):
    for e in w.to_erase:
        e.dying(w)


crashed = False
World = World()
print(World.regions_boundries)
for x in range(2500):
    World.new_entity()

for y in range(0):
    World.new_predator()

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            World.new_predator()

    if World.object_count >= 5500 and not trigger:
        trigger = True
        for y in range(10):
            World.new_predator()

    Window.fill((30, 10, 50))
    updating(World)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
