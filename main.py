import sys
import time

from OpenGL.GL import (
    glClearColor, glClear, glEnable, glViewport, glMatrixMode, glLoadIdentity,
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_PROJECTION, GL_MODELVIEW
)
from OpenGL.GLU import gluPerspective, gluLookAt
from OpenGL.GLUT import (
    glutInit, glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition,
    glutCreateWindow, glutDisplayFunc, glutReshapeFunc, glutKeyboardFunc,
    glutKeyboardUpFunc, glutSpecialFunc, glutSpecialUpFunc, glutMainLoop,
    glutSwapBuffers, glutPostRedisplay, glutTimerFunc,
    GLUT_DOUBLE, GLUT_RGBA, GLUT_DEPTH,
    GLUT_KEY_UP, GLUT_KEY_DOWN, GLUT_KEY_LEFT, GLUT_KEY_RIGHT,
)

from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    TARGET_FPS,
    FOV,
    NEAR_PLANE,
    FAR_PLANE,
    SKY_COLOR,
)
from game import Game
from render import draw_track, draw_car, draw_token, draw_obstacle, draw_ground
from math3d import add, mul
from ui import begin_2d, end_2d, draw_text


game = Game()
window_width = WINDOW_WIDTH
window_height = WINDOW_HEIGHT
last_time = time.perf_counter()


def init_gl():
    glClearColor(*SKY_COLOR)
    glEnable(GL_DEPTH_TEST)


def reshape(width, height):
    global window_width, window_height
    window_width = max(1, width)
    window_height = max(1, height)
    glViewport(0, 0, window_width, window_height)


def setup_camera():
    cam_pos, target, up = game.camera()
    aspect = window_width / float(window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOV, aspect, NEAR_PLANE, FAR_PLANE)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        cam_pos[0], cam_pos[1], cam_pos[2],
        target[0], target[1], target[2],
        up[0], up[1], up[2]
    )


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    setup_camera()
    draw_ground()
    draw_track(game.track)

    # Tokens
    for idx, (seg, offset) in enumerate(game.track.tokens):
        if game.token_collected[idx]:
            continue
        pos, heading = game.track.sample(seg)
        right = game.track.right_vector(heading)
        token_pos = add(pos, mul(right, offset))
        draw_token(token_pos)

    # Obstacles
    for seg, offset in game.track.obstacles:
        pos, heading = game.track.sample(seg)
        right = game.track.right_vector(heading)
        obstacle_pos = add(pos, mul(right, offset))
        draw_obstacle(obstacle_pos)

    # Car
    car_pos, car_heading = game.car_world()
    draw_car(car_pos, car_heading)

    # UI
    begin_2d(window_width, window_height)
    draw_text(20, window_height - 30, f"Speed: {game.car.speed:05.1f}")
    draw_text(20, window_height - 55, f"Lap: {game.car.lap}")
    draw_text(20, window_height - 80, f"Tokens: {game.car.collected}")
    draw_text(20, window_height - 105, f"Hits: {game.car.hit}")
    draw_text(20, 25, "WASD / Arrow keys: drive | C: camera | P: pause | R: reset")
    if game.paused:
        draw_text(window_width * 0.5 - 40, window_height * 0.5, "PAUSED", (1.0, 0.9, 0.2))
    end_2d()

    glutSwapBuffers()


def timer(_value):
    global last_time
    now = time.perf_counter()
    dt = now - last_time
    last_time = now
    if dt > 0.1:
        dt = 0.1
    game.update(dt)
    glutPostRedisplay()
    glutTimerFunc(int(1000 / TARGET_FPS), timer, 0)


def key_down(key, _x, _y):
    key = key.decode("utf-8").lower()
    if key == "w":
        game.input_state["throttle"] = True
    elif key == "s":
        game.input_state["brake"] = True
    elif key == "a":
        game.input_state["left"] = True
    elif key == "d":
        game.input_state["right"] = True
    elif key == "p":
        game.paused = not game.paused
    elif key == "r":
        game.reset()
    elif key == "c":
        game.camera_mode = (game.camera_mode + 1) % 2
    elif key == "\x1b":
        sys.exit(0)


def key_up(key, _x, _y):
    key = key.decode("utf-8").lower()
    if key == "w":
        game.input_state["throttle"] = False
    elif key == "s":
        game.input_state["brake"] = False
    elif key == "a":
        game.input_state["left"] = False
    elif key == "d":
        game.input_state["right"] = False


def special_down(key, _x, _y):
    if key == GLUT_KEY_UP:
        game.input_state["throttle"] = True
    elif key == GLUT_KEY_DOWN:
        game.input_state["brake"] = True
    elif key == GLUT_KEY_LEFT:
        game.input_state["left"] = True
    elif key == GLUT_KEY_RIGHT:
        game.input_state["right"] = True


def special_up(key, _x, _y):
    if key == GLUT_KEY_UP:
        game.input_state["throttle"] = False
    elif key == GLUT_KEY_DOWN:
        game.input_state["brake"] = False
    elif key == GLUT_KEY_LEFT:
        game.input_state["left"] = False
    elif key == GLUT_KEY_RIGHT:
        game.input_state["right"] = False


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(80, 60)
    glutCreateWindow(WINDOW_TITLE)

    init_gl()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(key_down)
    glutKeyboardUpFunc(key_up)
    glutSpecialFunc(special_down)
    glutSpecialUpFunc(special_up)
    glutTimerFunc(int(1000 / TARGET_FPS), timer, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
