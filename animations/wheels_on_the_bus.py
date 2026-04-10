"""
Wheels on the Bus - Animated Nursery Rhyme
==========================================
A colourful, cartoon-style 2-D animation built with Pygame.

Scenes
------
1  Wheels rotating          → "The wheels on the bus go round and round"
2  Horn / sound waves        → "The horn on the bus goes beep beep beep"
3  Kids bouncing             → "The kids on the bus go up and down"
4  Driver shushing           → "The driver on the bus goes shh shh shh"
5  Windows sliding           → "The windows on the bus go up and down"
6  Brakes / dust clouds      → "The brakes on the bus go squeak squeak squeak"
7  Doors opening & closing   → "The doors on the bus go open and shut"

Run
---
    pip install pygame
    python wheels_on_the_bus.py

Press  Q / ESC  to quit at any time.
An optional  background_music.mp3  file placed in the same directory will be
played automatically if pygame.mixer finds it.
"""

import math
import os
import sys
import pygame

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 900, 600
FPS = 60
SCENE_DURATION = 8          # seconds each scene is shown
TITLE = "Wheels on the Bus – Nursery Rhyme"

# Palette
SKY_TOP      = (135, 206, 250)
SKY_BOTTOM   = (173, 224, 255)
GROUND       = ( 88, 180,  80)
ROAD         = ( 80,  80,  80)
ROAD_STRIPE  = (255, 220,   0)
BUS_YELLOW   = (255, 210,   0)
BUS_DARK     = (220, 160,   0)
WHEEL_DARK   = ( 30,  30,  30)
WHEEL_HUB    = (200, 200, 200)
WINDOW_BLUE  = (100, 180, 255)
WINDOW_FRAME = ( 50,  50, 200)
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
RED          = (220,  50,  50)
GREEN_TREE   = ( 34, 139,  34)
TRUNK        = (101,  67,  33)
HOUSE_RED    = (200,  80,  80)
HOUSE_CREAM  = (255, 240, 200)
CLOUD_WHITE  = (240, 240, 255)
SUBTITLE_BG  = (  0,   0,   0, 160)
SUN_YELLOW   = (255, 220,  50)
SKIN         = (255, 200, 150)
HAIR         = ( 80,  40,  10)
HORN_ORANGE  = (255, 140,   0)
DUST_COLOR   = (200, 180, 140)

# Bus geometry (all positions relative to the 900×600 canvas)
BUS_X    = 120    # left edge of bus body
BUS_Y    = 300    # top edge of bus body
BUS_W    = 520
BUS_H    = 160
WHEEL_R  = 38
WHEEL1_X = BUS_X + 110
WHEEL2_X = BUS_X + BUS_W - 110
WHEEL_Y  = BUS_Y + BUS_H + WHEEL_R - 10

# Lyrics for each scene
LYRICS = [
    "The wheels on the bus\ngo round and round,\nround and round, round and round…",
    "The horn on the bus\ngoes beep beep beep,\nbeep beep beep, beep beep beep…",
    "The kids on the bus\ngo up and down,\nup and down, up and down…",
    "The driver on the bus\ngoes shh shh shh,\nshh shh shh, shh shh shh…",
    "The windows on the bus\ngo up and down,\nup and down, up and down…",
    "The brakes on the bus\ngo squeak squeak squeak,\nsqueak squeak squeak…",
    "The doors on the bus\ngo open and shut,\nopen and shut, open and shut…",
]


# ---------------------------------------------------------------------------
# Helper drawing utilities
# ---------------------------------------------------------------------------

def gradient_rect(surface, top_colour, bottom_colour, rect):
    """Draw a vertical gradient rectangle."""
    x, y, w, h = rect
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(top_colour[0] + (bottom_colour[0] - top_colour[0]) * t)
        g = int(top_colour[1] + (bottom_colour[1] - top_colour[1]) * t)
        b = int(top_colour[2] + (bottom_colour[2] - top_colour[2]) * t)
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))


def draw_cloud(surface, cx, cy, r):
    for dx, dy, factor in [(-r * 0.6, r * 0.2, 0.7), (0, 0, 1.0), (r * 0.6, r * 0.2, 0.7)]:
        pygame.draw.circle(surface, CLOUD_WHITE, (int(cx + dx), int(cy + dy)), int(r * factor))


def draw_tree(surface, x, y):
    pygame.draw.rect(surface, TRUNK, (x - 7, y, 14, 40))
    pygame.draw.circle(surface, GREEN_TREE, (x, y), 32)
    pygame.draw.circle(surface, (50, 160, 50), (x - 10, y + 10), 22)


def draw_house(surface, x, y):
    body_w, body_h = 80, 60
    pygame.draw.rect(surface, HOUSE_CREAM, (x, y, body_w, body_h))
    roof_pts = [(x - 8, y), (x + body_w + 8, y), (x + body_w // 2, y - 35)]
    pygame.draw.polygon(surface, HOUSE_RED, roof_pts)
    # door
    pygame.draw.rect(surface, (160, 100, 60), (x + 30, y + 30, 20, 30))
    # windows
    pygame.draw.rect(surface, WINDOW_BLUE, (x + 8,  y + 15, 18, 18))
    pygame.draw.rect(surface, WINDOW_BLUE, (x + 54, y + 15, 18, 18))


def draw_sun(surface, t):
    cx = int(800 + 20 * math.sin(t * 0.3))
    cy = 70
    pygame.draw.circle(surface, SUN_YELLOW, (cx, cy), 38)
    for i in range(8):
        angle = i * math.pi / 4 + t * 0.5
        sx = cx + int(50 * math.cos(angle))
        sy = cy + int(50 * math.sin(angle))
        ex = cx + int(65 * math.cos(angle))
        ey = cy + int(65 * math.sin(angle))
        pygame.draw.line(surface, SUN_YELLOW, (sx, sy), (ex, ey), 4)


def draw_background(surface, t, road_offset):
    gradient_rect(surface, SKY_TOP, SKY_BOTTOM, (0, 0, WIDTH, HEIGHT - 160))
    # ground
    pygame.draw.rect(surface, GROUND, (0, HEIGHT - 160, WIDTH, 160))
    # road
    pygame.draw.rect(surface, ROAD, (0, HEIGHT - 120, WIDTH, 80))
    # road stripes (animated)
    stripe_w, stripe_gap = 60, 40
    total = stripe_w + stripe_gap
    offset = int(road_offset) % total
    for x in range(-total + offset, WIDTH + total, total):
        pygame.draw.rect(surface, ROAD_STRIPE, (x, HEIGHT - 85, stripe_w, 10))

    draw_sun(surface, t)

    # Clouds
    draw_cloud(surface, 150 + 30 * math.sin(t * 0.15), 80, 45)
    draw_cloud(surface, 500 + 20 * math.sin(t * 0.1 + 1), 55, 35)
    draw_cloud(surface, 700 + 25 * math.sin(t * 0.12 + 2), 95, 40)

    # Trees & houses in the background
    for pos in [(50, 220), (820, 210), (740, 225)]:
        draw_tree(surface, *pos)
    for hx, hy in [(80, 175), (680, 165)]:
        draw_house(surface, hx, hy)


def draw_bus_body(surface, extra_y=0):
    bx, by = BUS_X, BUS_Y + extra_y
    # Shadow
    pygame.draw.ellipse(surface, (60, 60, 60, 80),
                        (bx + 10, by + BUS_H + WHEEL_R * 2 - 10, BUS_W - 20, 20))
    # Body
    pygame.draw.rect(surface, BUS_YELLOW, (bx, by, BUS_W, BUS_H), border_radius=18)
    pygame.draw.rect(surface, BUS_DARK,   (bx, by, BUS_W, BUS_H), 4, border_radius=18)
    # Roof bump
    pygame.draw.rect(surface, BUS_YELLOW, (bx + 30, by - 20, BUS_W - 60, 28), border_radius=10)
    pygame.draw.rect(surface, BUS_DARK,   (bx + 30, by - 20, BUS_W - 60, 28), 3, border_radius=10)


def draw_bus_windows(surface, win_offsets, extra_y=0):
    """Draw three passenger windows (with optional up/down clip)."""
    by = BUS_Y + extra_y
    win_tops = [BUS_X + 80, BUS_X + 200, BUS_X + 320]
    for i, wx in enumerate(win_tops):
        wy = by + 20
        ww, wh = 80, 70
        clip_h = max(0, min(wh, wh - int(win_offsets[i])))
        # Frame
        pygame.draw.rect(surface, WINDOW_FRAME, (wx, wy, ww, wh), border_radius=8)
        # Glass (clipped to show open/close effect)
        pygame.draw.rect(surface, WINDOW_BLUE,  (wx + 4, wy + 4, ww - 8, clip_h - 8),
                         border_radius=6)


def draw_door(surface, open_amount, extra_y=0):
    """Draw a pair of bus doors. open_amount 0=closed, 1=fully open."""
    by = BUS_Y + extra_y
    dx = BUS_X + BUS_W - 80
    dy = by + 30
    dw, dh = 60, 110
    half = dw // 2
    gap = int(half * open_amount)
    # Left panel
    pygame.draw.rect(surface, BUS_DARK,
                     (dx - gap, dy, half, dh), border_radius=6)
    # Right panel
    pygame.draw.rect(surface, BUS_DARK,
                     (dx + half + gap, dy, half, dh), border_radius=6)


def draw_wheel(surface, cx, cy, angle, extra_y=0):
    cy += extra_y
    pygame.draw.circle(surface, WHEEL_DARK, (cx, cy), WHEEL_R)
    # Tyre tread highlights
    for i in range(6):
        a = angle + i * math.pi / 3
        sx = cx + int((WHEEL_R - 6) * math.cos(a))
        sy = cy + int((WHEEL_R - 6) * math.sin(a))
        ex = cx + int(WHEEL_R * math.cos(a))
        ey = cy + int(WHEEL_R * math.sin(a))
        pygame.draw.line(surface, (60, 60, 60), (sx, sy), (ex, ey), 3)
    pygame.draw.circle(surface, WHEEL_HUB, (cx, cy), WHEEL_R // 3)
    # Spokes
    for i in range(4):
        a = angle + i * math.pi / 2
        sx = cx + int(4 * math.cos(a))
        sy = cy + int(4 * math.sin(a))
        ex = cx + int((WHEEL_R // 3 - 2) * math.cos(a + math.pi / 6))
        ey = cy + int((WHEEL_R // 3 - 2) * math.sin(a + math.pi / 6))
        pygame.draw.line(surface, WHEEL_DARK, (sx, sy), (ex, ey), 3)


# ---------------------------------------------------------------------------
# Character helpers
# ---------------------------------------------------------------------------

def draw_kid(surface, cx, cy, bounce=0, smile=True):
    """Draw a simple round-headed cartoon kid."""
    cy -= int(bounce)
    # Body
    pygame.draw.ellipse(surface, (100, 150, 255), (cx - 14, cy + 20, 28, 32))
    # Head
    pygame.draw.circle(surface, SKIN, (cx, cy), 20)
    pygame.draw.circle(surface, HAIR, (cx, cy - 8), 14)
    # Eyes
    pygame.draw.circle(surface, BLACK, (cx - 7, cy - 2), 4)
    pygame.draw.circle(surface, BLACK, (cx + 7, cy - 2), 4)
    pygame.draw.circle(surface, WHITE, (cx - 6, cy - 3), 2)
    pygame.draw.circle(surface, WHITE, (cx + 8, cy - 3), 2)
    # Mouth
    if smile:
        pygame.draw.arc(surface, RED,
                        (cx - 8, cy + 4, 16, 10), math.pi, 2 * math.pi, 3)


def draw_driver(surface, cx, cy, shh=False):
    """Draw the bus driver behind the steering wheel."""
    # Body
    pygame.draw.ellipse(surface, (50, 120, 200), (cx - 16, cy + 22, 32, 36))
    # Head
    pygame.draw.circle(surface, SKIN, (cx, cy), 22)
    # Cap
    pygame.draw.ellipse(surface, (30, 60, 150), (cx - 22, cy - 22, 44, 16))
    pygame.draw.rect(surface,  (30, 60, 150), (cx - 18, cy - 30, 36, 14),
                     border_radius=6)
    # Eyes
    pygame.draw.circle(surface, BLACK, (cx - 8, cy - 4), 4)
    pygame.draw.circle(surface, BLACK, (cx + 8, cy - 4), 4)
    pygame.draw.circle(surface, WHITE, (cx - 7, cy - 5), 2)
    pygame.draw.circle(surface, WHITE, (cx + 9, cy - 5), 2)
    if shh:
        # Finger to lips
        pygame.draw.line(surface, SKIN, (cx + 10, cy + 6), (cx + 20, cy - 10), 4)
        pygame.draw.circle(surface, SKIN, (cx + 20, cy - 12), 5)
        pygame.draw.circle(surface, RED, (cx, cy + 6), 5)   # small 'o' mouth
    else:
        pygame.draw.arc(surface, RED, (cx - 8, cy + 4, 16, 10), math.pi, 2 * math.pi, 3)
    # Steering wheel
    pygame.draw.circle(surface, (60, 40, 20), (cx + 30, cy + 35), 20, 4)
    pygame.draw.line(surface, (60, 40, 20), (cx + 30, cy + 15), (cx + 30, cy + 55), 3)
    pygame.draw.line(surface, (60, 40, 20), (cx + 10, cy + 35), (cx + 50, cy + 35), 3)


# ---------------------------------------------------------------------------
# Sound-wave helper (for horn scene)
# ---------------------------------------------------------------------------

def draw_sound_waves(surface, cx, cy, t, active=True):
    if not active:
        return
    for i in range(1, 4):
        alpha = int(200 * (1 - (t % 1.0)))
        r = int(20 + 30 * i + 25 * (t % 1.0))
        if alpha > 0:
            wave_surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(wave_surf, (HORN_ORANGE[0], HORN_ORANGE[1],
                                           HORN_ORANGE[2], alpha),
                               (r + 2, r + 2), r, 3)
            surface.blit(wave_surf, (cx - r - 2, cy - r - 2))


# ---------------------------------------------------------------------------
# Subtitle renderer
# ---------------------------------------------------------------------------

def draw_subtitle(surface, font, text, y_base):
    lines = text.split("\n")
    padding = 10
    line_surfs = [font.render(ln, True, WHITE) for ln in lines]
    max_w = max(s.get_width() for s in line_surfs)
    total_h = sum(s.get_height() for s in line_surfs) + padding * 2 + (len(lines) - 1) * 4

    bg = pygame.Surface((max_w + padding * 2, total_h), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 150))
    x_bg = (WIDTH - bg.get_width()) // 2
    surface.blit(bg, (x_bg, y_base - total_h - 6))

    y_cursor = y_base - total_h - 6 + padding
    for surf in line_surfs:
        x_text = (WIDTH - surf.get_width()) // 2
        surface.blit(surf, (x_text, y_cursor))
        y_cursor += surf.get_height() + 4


# ---------------------------------------------------------------------------
# Scene renderers
# ---------------------------------------------------------------------------

def scene_wheels(surface, t, road_offset):
    """Spinning wheels + bouncing bus."""
    draw_background(surface, t, road_offset)
    extra_y = int(3 * math.sin(t * 8))
    angle = t * 4.0
    draw_bus_body(surface, extra_y)
    draw_bus_windows(surface, [0, 0, 0], extra_y)
    draw_door(surface, 0, extra_y)
    draw_wheel(surface, WHEEL1_X, WHEEL_Y, angle, extra_y)
    draw_wheel(surface, WHEEL2_X, WHEEL_Y, angle, extra_y)
    # Kids inside (visible through windows)
    for i, wx in enumerate([BUS_X + 110, BUS_X + 230, BUS_X + 350]):
        draw_kid(surface, wx, BUS_Y + extra_y + 60, bounce=0)
    draw_driver(surface, BUS_X + BUS_W - 60, BUS_Y + extra_y + 60)


def scene_horn(surface, t, road_offset):
    """Horn + sound wave rings."""
    draw_background(surface, t, road_offset)
    draw_bus_body(surface)
    draw_bus_windows(surface, [0, 0, 0])
    draw_door(surface, 0)
    draw_wheel(surface, WHEEL1_X, WHEEL_Y, t * 1.5)
    draw_wheel(surface, WHEEL2_X, WHEEL_Y, t * 1.5)
    # Horn on roof
    hx, hy = BUS_X + BUS_W // 2 - 20, BUS_Y - 35
    pygame.draw.rect(surface, HORN_ORANGE, (hx, hy, 40, 18), border_radius=6)
    pygame.draw.ellipse(surface, HORN_ORANGE, (hx + 25, hy - 8, 28, 34))
    draw_sound_waves(surface, hx + 50, hy + 9, t)
    draw_driver(surface, BUS_X + BUS_W - 60, BUS_Y + 60)
    for i, wx in enumerate([BUS_X + 110, BUS_X + 230, BUS_X + 350]):
        draw_kid(surface, wx, BUS_Y + 60, bounce=0)


def scene_kids_bounce(surface, t, road_offset):
    """Kids bouncing up and down."""
    draw_background(surface, t, road_offset)
    draw_bus_body(surface)
    draw_bus_windows(surface, [0, 0, 0])
    draw_door(surface, 0)
    draw_wheel(surface, WHEEL1_X, WHEEL_Y, t * 1.5)
    draw_wheel(surface, WHEEL2_X, WHEEL_Y, t * 1.5)
    for i, wx in enumerate([BUS_X + 110, BUS_X + 230, BUS_X + 350]):
        phase = i * math.pi * 2 / 3
        bounce = 14 * abs(math.sin(t * 4 + phase))
        draw_kid(surface, wx, BUS_Y + 60, bounce=bounce)
    draw_driver(surface, BUS_X + BUS_W - 60, BUS_Y + 60)


def scene_driver_shh(surface, t, road_offset):
    """Driver says shh shh shh."""
    draw_background(surface, t, road_offset)
    draw_bus_body(surface)
    draw_bus_windows(surface, [0, 0, 0])
    draw_door(surface, 0)
    draw_wheel(surface, WHEEL1_X, WHEEL_Y, t * 1.0)
    draw_wheel(surface, WHEEL2_X, WHEEL_Y, t * 1.0)
    for i, wx in enumerate([BUS_X + 110, BUS_X + 230, BUS_X + 350]):
        draw_kid(surface, wx, BUS_Y + 60, bounce=0, smile=False)
    draw_driver(surface, BUS_X + BUS_W - 60, BUS_Y + 60, shh=True)
    # "SHH" text pops in time with beat
    if int(t * 2) % 2 == 0:
        shh_font = pygame.font.SysFont("Comic Sans MS", 42, bold=True)
        shh_surf = shh_font.render("SHH!", True, RED)
        surface.blit(shh_surf,
                     (BUS_X + BUS_W - 30, BUS_Y + 20))


def scene_windows(surface, t, road_offset):
    """Windows slide up and down."""
    draw_background(surface, t, road_offset)
    draw_bus_body(surface)
    offsets = [
        30 * abs(math.sin(t * 3 + i * 1.1))
        for i in range(3)
    ]
    draw_bus_windows(surface, offsets)
    draw_door(surface, 0)
    draw_wheel(surface, WHEEL1_X, WHEEL_Y, t * 1.5)
    draw_wheel(surface, WHEEL2_X, WHEEL_Y, t * 1.5)
    for i, wx in enumerate([BUS_X + 110, BUS_X + 230, BUS_X + 350]):
        draw_kid(surface, wx, BUS_Y + 60)
    draw_driver(surface, BUS_X + BUS_W - 60, BUS_Y + 60)


def scene_brakes(surface, t, road_offset):
    """Brakes: bus slows, dust clouds."""
    draw_background(surface, t, road_offset)
    draw_bus_body(surface)
    draw_bus_windows(surface, [0, 0, 0])
    draw_door(surface, 0)
    # Dust at wheels
    for wx in [WHEEL1_X, WHEEL2_X]:
        for j in range(5):
            angle = t * 3 + j * 1.2
            dr = int(20 + 10 * math.sin(t * 5 + j))
            dx = wx + int(dr * math.cos(angle))
            dy = WHEEL_Y + int(dr * 0.5 * math.sin(angle)) + WHEEL_R
            radius = int(8 + 4 * math.sin(t * 4 + j))
            alpha = int(180 * (0.5 + 0.5 * math.sin(t * 3 + j)))
            dust_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(dust_surf,
                               (DUST_COLOR[0], DUST_COLOR[1], DUST_COLOR[2], alpha),
                               (radius, radius), radius)
            surface.blit(dust_surf, (dx - radius, dy - radius))
    draw_wheel(surface, WHEEL1_X, WHEEL_Y, t * 0.3)
    draw_wheel(surface, WHEEL2_X, WHEEL_Y, t * 0.3)
    for i, wx in enumerate([BUS_X + 110, BUS_X + 230, BUS_X + 350]):
        draw_kid(surface, wx, BUS_Y + 60)
    draw_driver(surface, BUS_X + BUS_W - 60, BUS_Y + 60)
    # "SQUEAK" label
    if int(t * 3) % 2 == 0:
        sq_font = pygame.font.SysFont("Comic Sans MS", 36, bold=True)
        sq_surf = sq_font.render("SQUEAK!", True, (200, 80, 0))
        surface.blit(sq_surf, (BUS_X + 10, BUS_Y - 50))


def scene_doors(surface, t, road_offset):
    """Doors open and close."""
    draw_background(surface, t, road_offset)
    draw_bus_body(surface)
    draw_bus_windows(surface, [0, 0, 0])
    open_amount = 0.5 + 0.5 * math.sin(t * 3)
    draw_door(surface, open_amount)
    draw_wheel(surface, WHEEL1_X, WHEEL_Y, t * 1.0)
    draw_wheel(surface, WHEEL2_X, WHEEL_Y, t * 1.0)
    for i, wx in enumerate([BUS_X + 110, BUS_X + 230, BUS_X + 350]):
        draw_kid(surface, wx, BUS_Y + 60)
    draw_driver(surface, BUS_X + BUS_W - 60, BUS_Y + 60)


SCENES = [
    scene_wheels,
    scene_horn,
    scene_kids_bounce,
    scene_driver_shh,
    scene_windows,
    scene_brakes,
    scene_doors,
]


# ---------------------------------------------------------------------------
# Progress bar
# ---------------------------------------------------------------------------

def draw_progress_bar(surface, scene_index, scene_t):
    total = len(SCENES)
    bar_w = WIDTH - 40
    bar_h = 10
    bar_x, bar_y = 20, HEIGHT - 18
    pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h), border_radius=5)
    filled = int(bar_w * (scene_index + scene_t / SCENE_DURATION) / total)
    pygame.draw.rect(surface, BUS_YELLOW, (bar_x, bar_y, filled, bar_h), border_radius=5)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Fonts
    subtitle_font = pygame.font.SysFont("Comic Sans MS", 22, bold=True)
    title_font    = pygame.font.SysFont("Comic Sans MS", 48, bold=True)
    info_font     = pygame.font.SysFont("Arial", 18)

    # Optional background music
    music_path = os.path.join(os.path.dirname(__file__), "background_music.mp3")
    if os.path.isfile(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    # --- Title screen ---
    title_start = pygame.time.get_ticks()
    showing_title = True
    while showing_title:
        dt_ms = pygame.time.get_ticks() - title_start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                showing_title = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                showing_title = False

        if dt_ms > 3000:
            showing_title = False

        gradient_rect(screen, SKY_TOP, SKY_BOTTOM, (0, 0, WIDTH, HEIGHT))
        draw_sun(screen, dt_ms / 1000.0)

        t_surf = title_font.render("🚌  Wheels on the Bus  🚌", True, BUS_YELLOW)
        shadow_surf = title_font.render("🚌  Wheels on the Bus  🚌", True, (80, 60, 0))
        tx = (WIDTH - t_surf.get_width()) // 2
        screen.blit(shadow_surf, (tx + 3, HEIGHT // 2 - 60 + 3))
        screen.blit(t_surf,      (tx,     HEIGHT // 2 - 60))

        hint = info_font.render("Press any key or wait…", True, WHITE)
        screen.blit(hint, ((WIDTH - hint.get_width()) // 2, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(FPS)

    # --- Animation loop ---
    start_time = pygame.time.get_ticks()
    road_offset = 0.0

    while True:
        dt = clock.tick(FPS) / 1000.0
        road_offset += 120 * dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        elapsed = (pygame.time.get_ticks() - start_time) / 1000.0
        total_duration = len(SCENES) * SCENE_DURATION

        if elapsed >= total_duration:
            # Loop back
            start_time = pygame.time.get_ticks()
            elapsed = 0.0

        scene_index = min(int(elapsed / SCENE_DURATION), len(SCENES) - 1)
        scene_t     = elapsed - scene_index * SCENE_DURATION

        # Draw current scene
        SCENES[scene_index](screen, scene_t, road_offset)

        # Subtitle
        draw_subtitle(screen, subtitle_font, LYRICS[scene_index], HEIGHT - 28)

        # Progress bar
        draw_progress_bar(screen, scene_index, scene_t)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
