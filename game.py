from constants import (
    CHASE_DISTANCE,
    CHASE_HEIGHT,
    CHASE_LOOK_AHEAD,
    TOP_HEIGHT,
)
from math3d import add, mul
from track import Track
from car import Car


class Game:
    def __init__(self):
        self.track = Track()
        self.car = Car()
        self.input_state = {
            "throttle": False,
            "brake": False,
            "left": False,
            "right": False,
        }
        self.camera_mode = 0
        self.paused = False
        self.elapsed = 0.0
        self.token_collected = [False] * len(self.track.tokens)
        self.obstacle_hit = [False] * len(self.track.obstacles)

    def reset(self):
        self.car.reset()
        self.elapsed = 0.0
        self.token_collected = [False] * len(self.track.tokens)
        self.obstacle_hit = [False] * len(self.track.obstacles)

    def update(self, dt):
        if self.paused:
            return
        self.elapsed += dt
        self.car.update(dt, self.input_state, self.track.num_segments)
        self._check_tokens()
        self._check_obstacles()

    def _segment_delta(self, a, b):
        n = self.track.num_segments
        delta = (a - b + n * 0.5) % n - n * 0.5
        return delta

    def _check_tokens(self):
        car_segment = int(self.car.s) % self.track.num_segments
        for idx, (seg, offset) in enumerate(self.track.tokens):
            if self.token_collected[idx]:
                continue
            if abs(self._segment_delta(seg, car_segment)) < 2:
                if abs(self.car.offset - offset) < 1.5:
                    self.token_collected[idx] = True
                    self.car.collected += 1

    def _check_obstacles(self):
        car_segment = int(self.car.s) % self.track.num_segments
        for idx, (seg, offset) in enumerate(self.track.obstacles):
            if abs(self._segment_delta(seg, car_segment)) < 1:
                if abs(self.car.offset - offset) < 1.2:
                    # Speed penalty when hitting obstacles
                    self.car.speed *= 0.6
                    self.car.hit += 1

    def car_world(self):
        pos, heading = self.track.sample(self.car.s)
        right = self.track.right_vector(heading)
        offset = mul(right, self.car.offset)
        return add(pos, offset), heading

    def camera(self):
        car_pos, heading = self.car_world()
        forward = self.track.forward_vector(heading)

        if self.camera_mode == 0:
            cam_pos = add(car_pos, mul(forward, -CHASE_DISTANCE))
            cam_pos = add(cam_pos, (0.0, CHASE_HEIGHT, 0.0))
            target = add(car_pos, mul(forward, CHASE_LOOK_AHEAD))
            up = (0.0, 1.0, 0.0)
            return cam_pos, target, up

        cam_pos = add(car_pos, (0.0, TOP_HEIGHT, 0.0))
        target = car_pos
        up = (0.0, 0.0, -1.0)
        return cam_pos, target, up
