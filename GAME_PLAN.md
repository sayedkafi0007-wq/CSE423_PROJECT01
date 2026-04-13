# INITIAL D - Build Plan

## Goal
Create a small 3D racing game prototype using PyOpenGL/GLUT that mirrors the arcade feel of PicoWorldRace: looping track, curves/hills, collectibles, and a fast iteration loop.

## Core Loop
1. Start race
2. Accelerate/brake and steer
3. Collect tokens, avoid obstacles
4. Complete laps while maximizing score

## Mechanics
- **Track**: Procedurally generated loop (curves + hills) using parametric functions.
- **Car**: Forward speed + lateral offset, off‑road penalty, basic collision checks.
- **Scoring**: Tokens collected; obstacle hits tracked.
- **Camera**: Chase and top‑down modes.

## OpenGL Function Mapping
These core lab functions are used directly in the code:
- `glutInit`, `glutInitDisplayMode`, `glutInitWindowSize`, `glutCreateWindow`, `glutMainLoop`
- `glMatrixMode`, `glLoadIdentity`, `glViewport`
- `gluPerspective`, `gluLookAt`
- `glBegin`, `glVertex3f`, `glColor3f`, `glEnd`

## Repo Milestones
1. **MVP (Complete)**
   - OpenGL window setup
   - 3D track rendering (quads)
   - Car movement + chase camera
2. **Gameplay Pass (Complete)**
   - Tokens + obstacles
   - Lap counter and HUD
3. **Polish (Optional)**
   - Better collision feedback (camera shake, hit flash)
   - AI ghost car
   - Track presets + seed selector

## File Map
- `main.py`: window, loop, input
- `game.py`: state update + collisions
- `track.py`: procedural track
- `car.py`: physics
- `render.py`: drawing helpers
- `ui.py`: HUD overlay
- `constants.py`: tunable parameters

## Next Steps (Optional)
- Add minimap using orthographic projection
- Add difficulty presets (speed, friction)
- Add custom track editor (CSV or JSON)
