import pygame
import random

pygame.init()

screen_height = 800
screen_width = 1000
game_display = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont("/LondrinaSolid-Regular.ttf", 35)

#colors
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0, 230, 64, 1)
YELLOW = (239, 239, 0)

snake_speed = 35
game_speed = 10
snake_length = 1
cube_width = 30
cube_height = 30

class Cube():
    def __init__(self, x, y, index, color):
        self.index = index
        self.width = cube_width
        self.height = cube_height
        self.color = color
        self.direction = None
        self.previousX = None
        self.previousY = None
        self.previousDirection = None
        self.x = x
        self.y = y

head = Cube(screen_width/2, screen_height/2, "head", RED)
cubes = [head]
fruits = []


def update_cubes():
    prev_cubes = cubes.copy()
    for cube in cubes:
        if cube.index == "body":
            cube.previousX = cube.x
            cube.previousY = cube.y
            cube.x = prev_cubes[cubes.index(cube)-1].previousX
            cube.y = prev_cubes[cubes.index(cube)-1].previousY
            cube.previousDirection = cube.direction
            cube.direction = prev_cubes[cubes.index(cube)-1].previousDirection


def add_cube():
    last_cube = cubes[len(cubes)-1]
    if last_cube.direction == "up":
        cubes.append(Cube(last_cube.x, last_cube.y + 35, "body", GREEN))
    elif last_cube.direction == "down":
        cubes.append(Cube(last_cube.x, last_cube.y - 35, "body", GREEN))
    elif last_cube.direction == "left":
        cubes.append(Cube(last_cube.x + 35, last_cube.y, "body", GREEN))
    elif last_cube.direction == "right":
        cubes.append(Cube(last_cube.x - 35, last_cube.y, "body", GREEN))


def print_score(snake_length):
    text = font.render(f"LENGTH: {snake_length}", True, RED)
    game_display.blit(text, (10,10))


def draw_cubes():
    game_display.fill(BLACK)
    for cube in cubes:
        pygame.draw.rect(game_display, cube.color, [cube.x, cube.y, cube.width, cube.height])


def spawn_fruit():
    for fruit in fruits:
        pygame.draw.rect(game_display, fruit.color, [fruit.x, fruit.y, fruit.width, fruit.height])

    if len(fruits) == 0:
        random_x = random.randrange(50, screen_width - 50)
        random_y = random.randrange(50, screen_height - 75)
        fruit = Cube(random_x, random_y, "fruit", YELLOW)
        pygame.draw.rect(game_display, fruit.color, [fruit.x, fruit.y, fruit.width, fruit.height])
        fruits.append(fruit)


clock = pygame.time.Clock()
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and head.direction != "left":
                head.direction = "right"
            if event.key == pygame.K_LEFT and head.direction != "right":
                head.direction = "left"
            if event.key == pygame.K_DOWN and head.direction != "up":
                head.direction = "down"
            if event.key == pygame.K_UP and head.direction != "down":
                head.direction = "up"

    if head.direction == "right":
        head.x += snake_speed
    elif head.direction == "left":
        head.x -= snake_speed
    elif head.direction == "up":
        head.y -= snake_speed
    elif head.direction == "down":
        head.y += snake_speed

    head.previousX = head.x
    head.previousY = head.y
    head.previousDirection = head.direction

    draw_cubes()
    print_score(snake_length)
    spawn_fruit()

    #snake collision
    for cube in cubes[1:]:
        if cube.x + cube.width >= head.x + head.width >= cube.x and (cube.y + cube.height >= head.y + head.height >= cube.y):
            game_over = True

    #fruit collision
    fruit = fruits[0]
    if ((head.y + head.height >= fruit.y >= head.y or head.y <= fruit.y + fruit.height <= head.y + head.height)
            and (fruit.x + fruit.width >= head.x + head.width >= fruit.x or fruit.x <= head.x <= fruit.x + fruit.width)):
        snake_length += 1
        add_cube()
        fruits.pop()
        draw_cubes()
        print_score(snake_length)
        spawn_fruit()
        game_speed += 0.2

    update_cubes()
    if head.x < -10 or head.x + head.width > screen_width+10 or head.y < -20 or head.y + head.height > screen_height+20:
        game_over = True

    pygame.display.update()
    clock.tick(game_speed)


