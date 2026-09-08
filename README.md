# The Dash — round-00-dash

Your duck, your code. This repository is one entry to the Duck Jam round `round-00-dash` 1.0.0: edit
`controller.py`, score it on your own machine in the very sandbox the Arena uses, and submit the commit
you pushed. Nothing here is graded until you type `duckjam submit`.

## Ten minutes to your first score

    curl -LsSf https://astral.sh/uv/install.sh | sh   # once, if you have no uv
    uv sync                                           # the SDK, the runner and the round
    uv run duckjam play                               # five local seeds, one line each
    uv run duckjam watch                              # replay the worst of them
    uv run duckjam submit                             # enter the jam with your pushed HEAD

The first `play` fetches the robot model and the sandbox's Python — about 45 MB, once per machine,
into your user cache and never into this repository. Traces, logs and summaries land under `runs/`,
which is ignored: what you commit is your controller.

## The round

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

## What you edit, and what you do not

`controller.py` and anything you put beside it is yours. `duckjam.toml`, `pyproject.toml` and `uv.lock`
pin the round and the runner the Arena scores you with; changing them changes nothing in the Arena
and breaks your local run. The sandbox has the standard library and nothing else, so a dependency
you add is a run that is refused.

`AGENTS.md` is the same contract, written for your AI assistant; `CLAUDE.md` points at it.
