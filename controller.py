"""Fourteen sines with a bit of feedback: the beginner's controller, and the measurement's."""
import math

t = 0.0


def step(obs):
    global t
    t += 0.02
    phase = 2 * math.pi * 1.5 * t
    return [0.1 * math.sin(phase + 0.4 * i) - 0.02 * obs[6 + i] for i in range(14)]
