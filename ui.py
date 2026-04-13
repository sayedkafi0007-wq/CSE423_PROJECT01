from OpenGL.GL import (
    glMatrixMode, glPushMatrix, glPopMatrix, glLoadIdentity, glOrtho,
    glDisable, glEnable, glRasterPos2f, glColor3f,
    GL_PROJECTION, GL_MODELVIEW, GL_DEPTH_TEST
)
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18


def begin_2d(width, height):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)


def end_2d():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_text(x, y, text, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
