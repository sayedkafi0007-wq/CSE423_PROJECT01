# INITIAL D (OpenGL)

A lightweight 3D racing prototype built with PyOpenGL + GLUT. The track is generated procedurally (curves + hills), and the game includes collectibles, obstacles, lap tracking, and two camera modes.

## Features
- Procedural 3D track (looped)
- Simple car physics with drift-style lateral movement
- Tokens to collect and obstacles to avoid
- Chase camera + top-down camera
- HUD with speed, lap count, tokens, and hits

## Requirements
- Python 3.9+
- OpenGL-capable GPU
- FreeGLUT (usually bundled with PyOpenGL on Windows)

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

If GLUT fails to initialize, install a FreeGLUT binary and ensure it is on your PATH.

## Controls
- `W` / Up Arrow: accelerate
- `S` / Down Arrow: brake
- `A` / Left Arrow: steer left
- `D` / Right Arrow: steer right
- `C`: toggle camera
- `P`: pause
- `R`: reset
- `Esc`: quit

## Structure
- `main.py`: OpenGL/GLUT setup and loop
- `game.py`: game state + update loop
- `track.py`: procedural track generator
- `car.py`: car physics
- `render.py`: OpenGL draw helpers
- `ui.py`: 2D HUD text helpers
- `constants.py`: tunable parameters

## Notes
This project is designed for immediate-mode OpenGL (glBegin/glEnd) to align with typical CSE423 lab workflows.
