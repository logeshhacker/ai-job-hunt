# Wheels on the Bus – Nursery Rhyme Animation

A colourful, cartoon-style 2-D animated nursery rhyme built with **Pygame**.

## What it does

The animation plays through **7 scenes** (≈ 8 seconds each, looping), each
synced to a verse of *"The Wheels on the Bus"*:

| # | Scene | Lyric |
|---|-------|-------|
| 1 | Spinning wheels + bouncing bus | "The wheels on the bus go round and round…" |
| 2 | Horn with animated sound waves | "The horn on the bus goes beep beep beep…" |
| 3 | Kids bouncing inside | "The kids on the bus go up and down…" |
| 4 | Driver shushing (finger to lips) | "The driver on the bus goes shh shh shh…" |
| 5 | Windows sliding up and down | "The windows on the bus go up and down…" |
| 6 | Brakes with dust cloud effects | "The brakes on the bus go squeak squeak squeak…" |
| 7 | Doors opening and closing | "The doors on the bus go open and shut…" |

Features:
- Bright, cheerful background with sky gradient, sun with rotating rays, clouds, trees, and houses
- Animated road stripes that scroll to simulate movement
- Cartoon characters (smiling kids, bus driver with cap & steering wheel)
- Lyrics subtitles overlaid at the bottom of each scene
- A progress bar showing how far through the song you are
- **Optional background music**: drop a file named `background_music.mp3` in this directory and it will play automatically

## Requirements

- Python 3.8+
- Pygame 2.x

## Installation

```bash
pip install -r animations/requirements.txt
```

Or install Pygame directly:

```bash
pip install pygame
```

## Running

```bash
python animations/wheels_on_the_bus.py
```

A 900 × 600 window will open. The animation loops continuously.

| Key | Action |
|-----|--------|
| `Q` or `Esc` | Quit |
| Any key / click | Skip title screen |

## Adding background music

Place any MP3 file named `background_music.mp3` next to `wheels_on_the_bus.py`:

```
animations/
  wheels_on_the_bus.py
  background_music.mp3   ← drop your nursery rhyme audio here
  requirements.txt
  README.md
```

A royalty-free version of "The Wheels on the Bus" can be downloaded from
sites like [Freesound](https://freesound.org) or
[Free Music Archive](https://freemusicarchive.org).

## Headless / CI environments

Pygame requires a display. In headless environments set the SDL dummy video
driver before running:

```bash
SDL_VIDEODRIVER=dummy python animations/wheels_on_the_bus.py
```

## Extending the animation

| What to change | Where to look |
|----------------|---------------|
| Scene duration | `SCENE_DURATION` constant (default 8 s) |
| Colours | Palette constants at the top of the file |
| Add a scene | Append a function to `SCENES` list and a string to `LYRICS` |
| Bus position / size | `BUS_X`, `BUS_Y`, `BUS_W`, `BUS_H`, `WHEEL_R` constants |
