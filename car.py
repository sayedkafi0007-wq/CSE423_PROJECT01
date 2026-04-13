from constants import (
    MAX_SPEED,
    ACCEL,
    BRAKE,
    DRAG,
    STEER_STRENGTH,
    CENTERING_FORCE,
    OFFROAD_DRAG,
    ROAD_HALF_WIDTH,
    SHOULDER_WIDTH,
)
from math3d import clamp


class Car:
    def __init__(self):
        self.reset()

    def reset(self):
        self.s = 0.0
        self.offset = 0.0
        self.speed = 0.0
        self.lap = 0
        self.collected = 0
        self.hit = 0
        self._last_s = 0.0

    def update(self, dt, input_state, track_length=None):
        accel = ACCEL if input_state.get("throttle") else 0.0
        brake = BRAKE if input_state.get("brake") else 0.0
        steering = 0.0
        if input_state.get("left"):
            steering -= 1.0
        if input_state.get("right"):
            steering += 1.0

        # Speed update
        self.speed += (accel - brake - DRAG * self.speed) * dt
        self.speed = clamp(self.speed, 0.0, MAX_SPEED)

        # Steering scales with speed
        steer_scale = (self.speed / MAX_SPEED) if MAX_SPEED > 0 else 0.0
        self.offset += steering * STEER_STRENGTH * steer_scale * dt * 6.0

        if steering == 0.0:
            # Gently re-center
            self.offset -= self.offset * CENTERING_FORCE * dt

        # Off-road penalty
        edge_limit = ROAD_HALF_WIDTH + SHOULDER_WIDTH * 0.7
        if abs(self.offset) > edge_limit:
            self.speed *= (1.0 - OFFROAD_DRAG * dt)
            self.offset = clamp(self.offset, -edge_limit, edge_limit)

        # Advance along the track
        self._last_s = self.s
        self.s += self.speed * dt

        if track_length is not None and track_length > 0:
            while self.s >= track_length:
                self.s -= track_length
                self.lap += 1
