import math

from OpenGL.GL import (
    glBegin, glEnd, glVertex3f, glColor3f, glPushMatrix, glPopMatrix,
    glTranslatef, glRotatef, glScalef, glDisable, glEnable,
    GL_QUADS
)

from constants import (
    ROAD_HALF_WIDTH,
    SHOULDER_WIDTH,
    ROAD_COLOR,
    SHOULDER_COLOR,
    STRIPE_COLOR,
    CAR_COLOR,
    OBSTACLE_COLOR,
    GROUND_COLOR,
)
from math3d import add, mul


def _edge_points(center, right_vec, half_width):
    left = add(center, mul(right_vec, -half_width))
    right = add(center, mul(right_vec, half_width))
    return left, right


def draw_ground(size=300.0, height=-1.8):
    glColor3f(*GROUND_COLOR)
    glBegin(GL_QUADS)
    glVertex3f(-size, height, -size)
    glVertex3f(size, height, -size)
    glVertex3f(size, height, size)
    glVertex3f(-size, height, size)
    glEnd()


def draw_track(track):
    num_segments = track.num_segments

    # Road surface
    glColor3f(*ROAD_COLOR)
    glBegin(GL_QUADS)
    for i in range(num_segments):
        p0 = track.points[i]
        p1 = track.points[(i + 1) % num_segments]
        heading = track.headings[i]
        right_vec = track.right_vector(heading)
        l0, r0 = _edge_points(p0, right_vec, ROAD_HALF_WIDTH)
        l1, r1 = _edge_points(p1, right_vec, ROAD_HALF_WIDTH)
        glVertex3f(l0[0], l0[1], l0[2])
        glVertex3f(r0[0], r0[1], r0[2])
        glVertex3f(r1[0], r1[1], r1[2])
        glVertex3f(l1[0], l1[1], l1[2])
    glEnd()

    # Shoulders
    glColor3f(*SHOULDER_COLOR)
    glBegin(GL_QUADS)
    for i in range(num_segments):
        p0 = track.points[i]
        p1 = track.points[(i + 1) % num_segments]
        heading = track.headings[i]
        right_vec = track.right_vector(heading)
        l0, r0 = _edge_points(p0, right_vec, ROAD_HALF_WIDTH + SHOULDER_WIDTH)
        l1, r1 = _edge_points(p1, right_vec, ROAD_HALF_WIDTH + SHOULDER_WIDTH)

        road_l0, road_r0 = _edge_points(p0, right_vec, ROAD_HALF_WIDTH)
        road_l1, road_r1 = _edge_points(p1, right_vec, ROAD_HALF_WIDTH)

        # Left shoulder
        glVertex3f(l0[0], l0[1], l0[2])
        glVertex3f(road_l0[0], road_l0[1], road_l0[2])
        glVertex3f(road_l1[0], road_l1[1], road_l1[2])
        glVertex3f(l1[0], l1[1], l1[2])

        # Right shoulder
        glVertex3f(road_r0[0], road_r0[1], road_r0[2])
        glVertex3f(r0[0], r0[1], r0[2])
        glVertex3f(r1[0], r1[1], r1[2])
        glVertex3f(road_r1[0], road_r1[1], road_r1[2])
    glEnd()

    # Center stripes
    glColor3f(*STRIPE_COLOR)
    glBegin(GL_QUADS)
    stripe_half = 0.35
    for i in range(0, num_segments, 12):
        p0 = track.points[i]
        p1 = track.points[(i + 1) % num_segments]
        heading = track.headings[i]
        right_vec = track.right_vector(heading)
        l0, r0 = _edge_points(p0, right_vec, stripe_half)
        l1, r1 = _edge_points(p1, right_vec, stripe_half)
        glVertex3f(l0[0], l0[1] + 0.02, l0[2])
        glVertex3f(r0[0], r0[1] + 0.02, r0[2])
        glVertex3f(r1[0], r1[1] + 0.02, r1[2])
        glVertex3f(l1[0], l1[1] + 0.02, l1[2])
    glEnd()


def draw_box(size_x, size_y, size_z):
    hx = size_x * 0.5
    hy = size_y * 0.5
    hz = size_z * 0.5

    glBegin(GL_QUADS)
    # Front
    glVertex3f(-hx, -hy, hz)
    glVertex3f(hx, -hy, hz)
    glVertex3f(hx, hy, hz)
    glVertex3f(-hx, hy, hz)
    # Back
    glVertex3f(hx, -hy, -hz)
    glVertex3f(-hx, -hy, -hz)
    glVertex3f(-hx, hy, -hz)
    glVertex3f(hx, hy, -hz)
    # Left
    glVertex3f(-hx, -hy, -hz)
    glVertex3f(-hx, -hy, hz)
    glVertex3f(-hx, hy, hz)
    glVertex3f(-hx, hy, -hz)
    # Right
    glVertex3f(hx, -hy, hz)
    glVertex3f(hx, -hy, -hz)
    glVertex3f(hx, hy, -hz)
    glVertex3f(hx, hy, hz)
    # Top
    glVertex3f(-hx, hy, hz)
    glVertex3f(hx, hy, hz)
    glVertex3f(hx, hy, -hz)
    glVertex3f(-hx, hy, -hz)
    # Bottom
    glVertex3f(-hx, -hy, -hz)
    glVertex3f(hx, -hy, -hz)
    glVertex3f(hx, -hy, hz)
    glVertex3f(-hx, -hy, hz)
    glEnd()


def draw_car(position, heading):
    glPushMatrix()
    glTranslatef(position[0], position[1] + 0.7, position[2])
    glRotatef(math.degrees(heading), 0.0, 1.0, 0.0)
    glColor3f(*CAR_COLOR)
    draw_box(2.2, 1.0, 4.0)
    glPopMatrix()


def draw_token(position):
    glPushMatrix()
    glTranslatef(position[0], position[1] + 1.5, position[2])
    glColor3f(1.0, 0.9, 0.2)
    draw_box(0.8, 2.0, 0.8)
    glPopMatrix()


def draw_obstacle(position):
    glPushMatrix()
    glTranslatef(position[0], position[1] + 1.0, position[2])
    glColor3f(*OBSTACLE_COLOR)
    draw_box(1.4, 2.0, 1.4)
    glPopMatrix()
