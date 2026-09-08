# Duck Jam — round-00-dash 1.0.0 — The Dash

You are helping a player write a controller for a simulated microduck robot. The controller is
`controller.py`, pure Python 3.12, **standard library only** (no numpy, no torch: the sandbox has
none). It runs at 50 Hz inside a WebAssembly sandbox on the player's machine and in the Arena.

## The function

```python
def step(obs: list[float]) -> list[float]:   # 63 in, 14 out
```

`obs` has 61 + 2 floats. `act` is 14 joint deltas in radians, added to the STAND pose and clipped
by the runner. Module-level code runs once per seed; globals persist within a seed and reset between
seeds. `print()` goes to the player's log. `random` is seeded per seed. Do not read the clock.

## obs[0:61] — the robot, identical in every round

| slice | name | unit |
|---|---|---|
| 0–2 | base_ang_vel | rad/s, body frame |
| 3–5 | projected_gravity | unit vector, body frame; [0, 0, -1] when upright |
| 6–19 | joint_pos | rad, relative to STAND, actuator order below |
| 20–33 | joint_vel | rad/s |
| 34–47 | last_action | rad, the previous act |
| 48–60 | command | vx, vy, vtheta, neck_pitch, head_pitch, head_yaw, head_roll, body_x, body_y, body_z, body_roll, body_pitch, body_yaw — written by the round |

Actuator order: left_hip_yaw, left_hip_roll, left_hip_pitch, left_knee, left_ankle, neck_pitch, head_pitch, head_yaw, head_roll, right_hip_yaw, right_hip_roll, right_hip_pitch, right_knee, right_ankle. Legs are indices 0–4 and 9–13.

## obs[61:63] — this round's task_obs

| index | name | unit | range |
|---|---|---|---|
| 61 | goal_dx | m | −10 … 10 |
| 62 | goal_dy | m | −10 … 10 |

Body frame: relative to the base, in its yaw frame.

## This round

## Round 00 — The Dash

Walk to the goal. It is drawn between 1.5 m and 2.5 m ahead of the duck, inside a ±0.5 rad cone,
and it never moves. `task_obs` gives you where it is at every step — `goal_dx`, `goal_dy`, metres,
in the duck's own yaw frame — so a controller never has to guess the world.

A seed ends when the duck comes within 15 cm of the goal (`reached`), when its base drops below
6 cm (`fell`), or when the twenty seconds run out.

Ten points for reaching the goal, zero for falling, and in between the fraction of the starting
distance you closed, read off the recorded trace.

**Training on it with a GPU.** The round is also an mjlab task, `Duckjam-Round00-Dash`: `microduck_rl`'s walking recipe on this
exact scene, steered by this round's command, seeing its `task_obs`, ending on its `fell` and
`reached`. `train/round00_train.py` is the whole of it — a project of its own beside the round,
since the round's package is trusted code and imports nothing but the SDK — and `train/` installs
mjlab and `microduck_rl` at the commit the robot is pinned to.

```
cd train && uv sync
uv run train Duckjam-Round00-Dash --env.scene.num-envs 4096 --agent.max_iterations 2000 --agent.logger tensorboard
uv run python -m mjlab_microduck.export Duckjam-Round00-Dash --checkpoint-file model_2000.pt --num-envs 1 --onnx-file policy.onnx
uv run duckjam play --seeds eval    # from your clone, its duckjam.toml saying kind = "onnx", entry = "policy.onnx"
```

The export reads 63 floats — the robot's 61 and `goal_dx`, `goal_dy` — so it enters this round and
no other. What one such run cost and scored is in the contract spec, §Training on a round.

Episode 20 s; score in 0.0 … 10.0, higher is better; a seed ending in `fell` scores 0.0. Evaluation seeds 0-19, public; local play draws from 1000-1999.

## Commands

    uv run duckjam play              # five local seeds, one line each, then the aggregate
    uv run duckjam play --seeds eval # the leaderboard's seeds
    uv run duckjam watch             # replay the worst seed of the last play
    uv run duckjam submit            # smoke test, then enter the jam with HEAD (must be pushed)

## Rules

- Change `controller.py` and files beside it. Do not change `duckjam.toml`, `pyproject.toml` or
  `uv.lock`; do not add dependencies — none can be installed in the sandbox.
- A run that is refused (the log says why: a budget, an import, a non-finite action) fails the
  whole submission. Run `duckjam play` before every `submit`.
- Every seed must be deterministic: the same code on the same seed gives the same trace.
