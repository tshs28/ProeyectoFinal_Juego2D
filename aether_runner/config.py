# config.py
import pygame
import os

# Rutas de assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')

# Dimensiones de la pantalla
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colores
BACKGROUND_COLOR = (10, 5, 30)
PLAYER_COLOR = (100, 200, 255)
PLATFORM_COLOR = (70, 30, 150)
TEXT_COLOR = (200, 220, 255)
ENEMY_COLOR_FLOATER = (180, 80, 220)
ENEMY_COLOR_SHOOTER = (220, 60, 80)

# Configuración del jugador
PLAYER_SPEED = 8
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = -16
ANIMATION_SPEED = 0.15

# Estados del juego
MENU = 0
PLAYING = 1
GAME_OVER = 2
LEVEL_COMPLETE = 3

# Sistema de objetos
ITEM_TYPES = {
    'FRAGMENT': {'color': (100, 200, 255), 'points': 10, 'size': (15, 15)},
    'INVINCIBILITY': {'color': (255, 215, 0), 'points': 0, 'size': (20, 20), 'duration': 5000},
    'JUMP_BOOST': {'color': (50, 255, 100), 'points': 0, 'size': (20, 20), 'duration': 8000},
    'MAGNET': {'color': (255, 100, 200), 'points': 0, 'size': (20, 20), 'duration': 6000}
}

# Configuración de enemigos
ENEMY_SPEED = 2
PROJECTILE_SPEED = 5