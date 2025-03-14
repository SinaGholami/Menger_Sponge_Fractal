import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np 

# Define cube vertices
vertices = [
    [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
    [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
]

# Define cube edges
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Define cube faces
faces = [
    (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
    (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
]

def draw_cube(center , size):
    half = size / 2
    vertices = np.array([
        [half, half, -half], [half, -half, -half], [-half, -half, -half], [-half, half, -half],
        [half, half, half], [half, -half, half], [-half, -half, half], [-half, half, half]
    ]) + center
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv((1,1,1))
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3fv((0, 0, 0))
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_menger_sponge(center, size, level):
    if level == 0:
        draw_cube(center, size)
        return 
    new_size = size / 3
    offsets = [-new_size, 0, new_size]
    for x in offsets:
        for y in offsets:
            for z in offsets:
                if (x!=0 and y!=0) or (y!=0 and z!=0) or (x!=0 and z!=0):
                        continue
                new_center = center + np.array([x, y, z])
                draw_menger_sponge(new_center, new_size, level - 1)

def main():
    pygame.init()
    display = (800, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(60, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -4)
    level = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                level += 1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_menger_sponge(np.array([0, 0, 0]), 2, level)
        glRotatef(1, 1, 1, 1)
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()