import math
import random

from constants import (
    TRACK_SEGMENTS,
    TRACK_BASE_RADIUS,
    TRACK_RADIUS_WOBBLE,
    TRACK_WIGGLE,
    TRACK_HILL_AMPLITUDE,
    ROAD_HALF_WIDTH,
)
from math3d import lerp, wrap_index


class Track:
    def __init__(self, seed=7):
        self.num_segments = TRACK_SEGMENTS
        self.points = []
        self.headings = []
        self.tokens = []
        self.obstacles = []
        self._build(seed)

    def _build(self, seed):
        rng = random.Random(seed)
        for i in range(self.num_segments):
            theta = (2.0 * math.pi * i) / self.num_segments
            radius = TRACK_BASE_RADIUS + math.sin(theta * 2.0) * TRACK_RADIUS_WOBBLE
            x = math.cos(theta) * radius + math.cos(theta * 3.0) * TRACK_WIGGLE
            z = math.sin(theta) * radius + math.sin(theta * 2.0) * TRACK_WIGGLE
            y = (math.sin(theta * 3.0) * TRACK_HILL_AMPLITUDE +
                 math.sin(theta * 5.0) * TRACK_HILL_AMPLITUDE * 0.5)
            self.points.append((x, y, z))

        for i in range(self.num_segments):
            p0 = self.points[i]
            p1 = self.points[wrap_index(i + 1, self.num_segments)]
            heading = math.atan2(p1[0] - p0[0], p1[2] - p0[2])
            self.headings.append(heading)

        # Place tokens and obstacles at deterministic intervals
        for i in range(20, self.num_segments, 55):
            offset = rng.uniform(-ROAD_HALF_WIDTH * 0.6, ROAD_HALF_WIDTH * 0.6)
            self.tokens.append((i, offset))

        for i in range(45, self.num_segments, 90):
            offset = rng.uniform(-ROAD_HALF_WIDTH * 0.7, ROAD_HALF_WIDTH * 0.7)
            self.obstacles.append((i, offset))

    def sample(self, s):
        s = s % self.num_segments
        i = int(s)
        t = s - i
        p0 = self.points[i]
        p1 = self.points[wrap_index(i + 1, self.num_segments)]
        pos = lerp(p0, p1, t)
        heading = self.headings[i]
        return pos, heading

    @staticmethod
    def right_vector(heading):
        return (math.cos(heading), 0.0, -math.sin(heading))

    @staticmethod
    def forward_vector(heading):
        return (math.sin(heading), 0.0, math.cos(heading))
