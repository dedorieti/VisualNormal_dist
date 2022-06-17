# Based on the tutorial https://www.youtube.com/watch?v=tLsi2DeUsak&t=382s
# Import modules

import pygame
import pymunk
import pymunk.pygame_util
import math
import random

pygame.init()

WIDTH, HEIGHT = 1200, 1000
window = pygame.display.set_mode((WIDTH, HEIGHT))
x_step = 30

# some variables
layers = 15

x = range(-4, 5, 2)
b = []
for j in x:
    b.append((500 + j*25, 300))

# print(b)


def generate_pin_points(layers, y_start, x_start, y_step, x_step):
    pin_points = []
    for i in range(0, layers+1):
        x = range(-i, i+1, 2)
        for j in x:
            a = (y_start + j*y_step)
            b = (x_start + i*x_step)
            pin_points.append((a, b))

    return pin_points


def generate_buckets(space, layers, x_start, y, x_step):
    x = range(-layers, layers+1, 2)
    b = []
    for j in x:
        b.append((x_start + j * x_step, y))

    for pos in b:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, (10, 600), radius=2)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)


# print(generate_buckets(4, 500, 300, 25))
# print(f"here my points {generate_pin_points(4, 500, 100, 25, 25)}")


def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()


def create_boundaries(space, width, height):
    rects = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
        [(10, height / 2), (20, height)],
        [(width - 10, height / 2), (20, height)]
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)


def create_ball(space, radius, mass, pos):
    # In pymunk an object needs a body and a shape. The shape is how the object appears.
    # The actual calculations are done on the body
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.3
    shape.friction = 0.4
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape


def create_structure(space, layers):
    points = generate_pin_points(layers, WIDTH/2, 100, 30, 30)

    for pos in points:
        road_block = pymunk.Body(body_type=pymunk.Body.STATIC)
        road_block.position = pos
        shape = pymunk.Circle(road_block, 1)
        shape.elasticity = 0
        shape.friction = 0.5

        space.add(road_block, shape)


def run(window, width, height, layers):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 981)

    create_boundaries(space, width, height)
    create_structure(space, layers)
    generate_buckets(space, layers, WIDTH/2, 900, 30)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        random_factor = random.choice(range(-2, 3))
        create_ball(space, 10, 10, (WIDTH/2 + random_factor, 50))
        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    run(window, WIDTH, HEIGHT, layers)
