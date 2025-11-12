# game.py - SISTEMA COMPLETO MEJORADO CON NIVEL 4 CORREGIDO
import pygame
import sys
import random
from config import *
from player import Player
from items import ItemManager
from enemies import EnemyManager

class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, move_x=0, move_y=0, move_distance=100):
        super().__init__()
        self.image = self.create_platform_surface(width, height, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movimiento
        self.start_x = x
        self.start_y = y
        self.move_x = move_x
        self.move_y = move_y
        self.move_distance = move_distance
        self.direction = 1
        self.speed = 2

    def create_platform_surface(self, width, height, base_color):
        """Crear superficie de plataforma móvil"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surface, base_color, (0, 0, width, height), border_radius=6)
        
        # Efecto especial para plataformas móviles
        highlight_color = (
            min(255, base_color[0] + 60),
            min(255, base_color[1] + 60), 
            min(255, base_color[2] + 60)
        )
        pygame.draw.rect(surface, highlight_color, (3, 3, width - 6, 4), border_radius=2)
        
        # Indicadores de movimiento
        for i in range(0, width, 15):
            pygame.draw.circle(surface, (255, 255, 100), (i + 7, height - 5), 2)
            
        return surface

    def update(self):
        # Movimiento horizontal
        if self.move_x != 0:
            self.rect.x += self.move_x * self.speed * self.direction
            if abs(self.rect.x - self.start_x) > self.move_distance:
                self.direction *= -1
        
        # Movimiento vertical
        if self.move_y != 0:
            self.rect.y += self.move_y * self.speed * self.direction
            if abs(self.rect.y - self.start_y) > self.move_distance:
                self.direction *= -1

class OneWayPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = self.create_one_way_surface(width, height, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def create_one_way_surface(self, width, height, base_color):
        """Crear superficie de plataforma de un solo sentido"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surface, base_color, (0, 0, width, height), border_radius=6)
        
        # Efecto de transparencia en la parte superior
        for i in range(0, height, 2):
            alpha = 150 - (i * 50 // height)
            pygame.draw.line(surface, (*base_color[:3], alpha), (0, i), (width, i))
        
        # Flechas indicadoras
        for i in range(0, width, 20):
            pygame.draw.polygon(surface, (100, 255, 100), [
                (i + 5, 2), (i + 15, 2), (i + 10, 8)
            ])
            
        return surface

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Aether Runner - Nivel 1")
        self.clock = pygame.time.Clock()
        
        # Cargar sonidos
        self.load_sounds()
        
        # Estado del juego
        self.current_level = 1
        self.game_state = PLAYING
        self.level_completed = False
        
        # Inicializar sistemas
        self.reset_game()
        
        print("🎮 JUEGO INICIADO - SISTEMA MEJORADO CON SONIDOS")

    def load_sounds(self):
        """Cargar efectos de sonido y música"""
        try:
            # Efectos de sonido
            self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav") if pygame.mixer else None
            self.attack_sound = pygame.mixer.Sound("assets/sounds/attack.wav") if pygame.mixer else None
            self.collect_sound = pygame.mixer.Sound("assets/sounds/collect.wav") if pygame.mixer else None
            self.hurt_sound = pygame.mixer.Sound("assets/sounds/hurt.wav") if pygame.mixer else None
            self.enemy_death_sound = pygame.mixer.Sound("assets/sounds/enemy_death.wav") if pygame.mixer else None
            self.level_complete_sound = pygame.mixer.Sound("assets/sounds/level_complete.wav") if pygame.mixer else None
            
            # Configurar volúmenes
            for sound in [self.jump_sound, self.attack_sound, self.collect_sound, 
                         self.hurt_sound, self.enemy_death_sound, self.level_complete_sound]:
                if sound:
                    sound.set_volume(0.5)
            
            # Música de fondo
            if pygame.mixer:
                pygame.mixer.music.load("assets/sounds/background_music.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)  # Repetir indefinidamente
                
        except:
            print("⚠️ No se pudieron cargar algunos sonidos")
            # Crear sonidos placeholder si no existen los archivos
            self.jump_sound = self.attack_sound = self.collect_sound = None
            self.hurt_sound = self.enemy_death_sound = self.level_complete_sound = None

    def play_sound(self, sound):
        """Reproducir efecto de sonido si está disponible"""
        if sound and pygame.mixer:
            sound.play()

    def reset_game(self):
        """Reiniciar completamente el juego"""
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.solid_platforms = pygame.sprite.Group()  # Plataformas sólidas
        self.one_way_platforms = pygame.sprite.Group()  # Plataformas de un solo sentido
        
        # Sistemas
        self.item_manager = ItemManager()
        self.enemy_manager = EnemyManager()
        
        # Crear nivel según el nivel actual
        if self.current_level == 1:
            self.create_level_1()
        elif self.current_level == 2:
            self.create_level_2()
        elif self.current_level == 3:
            self.create_level_3()
        elif self.current_level == 4:
            self.create_level_4()  # ✅ NIVEL 4 CORREGIDO
        elif self.current_level == 5:
            self.create_level_5()
        elif self.current_level == 6:
            self.create_level_6()
        
        # Estrellas de fondo
        self.stars = self.create_stars()

    def create_platform_surface(self, width, height, base_color):
        """Crear superficie de plataforma normal"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surface, base_color, (0, 0, width, height), border_radius=8)
        
        highlight_color = (
            min(255, base_color[0] + 40),
            min(255, base_color[1] + 40), 
            min(255, base_color[2] + 40)
        )
        pygame.draw.rect(surface, highlight_color, (5, 5, width - 10, 5), border_radius=3)
        
        for i in range(0, width, 20):
            pygame.draw.circle(surface, (200, 200, 255), (i + 10, height - 8), 2)
            
        return surface

    def create_level_1(self):
        """Nivel 1 - Introducción"""
        print("🔧 CREANDO NIVEL 1 - INTRODUCCIÓN")
        
        # Crear jugador
        self.player = Player(100, 300)
        self.all_sprites.add(self.player)
        
        # Plataforma base sólida
        platform = pygame.sprite.Sprite()
        platform.image = self.create_platform_surface(SCREEN_WIDTH, 30, PLATFORM_COLOR)
        platform.rect = platform.image.get_rect()
        platform.rect.x = 0
        platform.rect.y = SCREEN_HEIGHT - 30
        self.all_sprites.add(platform)
        self.platforms.add(platform)
        self.solid_platforms.add(platform)
        
        # Plataformas flotantes normales
        platforms_data = [
            (200, 550, 150, 20), (400, 550, 150, 20), (600, 550, 150, 20), (800, 550, 150, 20),
            (650, 450, 200, 20), (450, 450, 150, 20), (250, 450, 150, 20),
            (500, 350, 120, 20), (700, 350, 120, 20),
            (600, 250, 100, 20), (400, 250, 100, 20),
            (500, 150, 80, 20)
        ]
        
        for x, y, width, height in platforms_data:
            platform = pygame.sprite.Sprite()
            platform.image = self.create_platform_surface(width, height, PLATFORM_COLOR)
            platform.rect = platform.image.get_rect()
            platform.rect.x = x
            platform.rect.y = y
            self.all_sprites.add(platform)
            self.platforms.add(platform)
            self.solid_platforms.add(platform)
        
        # Enemigos básicos
        enemy_positions = [
            (300, 520, 'FLOATER'), (600, 520, 'FLOATER'), 
            (500, 320, 'SHOOTER'), (350, 220, 'FLOATER'), (650, 220, 'FLOATER')
        ]
        
        for x, y, enemy_type in enemy_positions:
            enemy = self.enemy_manager.spawn_enemy(x, y, enemy_type)
            if enemy:
                self.all_sprites.add(enemy)
                self.position_enemy_on_platform(enemy)
        
        # Fragmentos
        fragment_positions = [
            (220, 520), (820, 520), (500, 420), (300, 420), (700, 420),
            (520, 320), (720, 320), (450, 220), (650, 220), (540, 120)
        ]
        
        for x, y in fragment_positions:
            item = self.item_manager.spawn_item(x, y, 'FRAGMENT')
            if item:
                self.position_item_on_platform(item)
        
        # Power-ups
        powerup_positions = [
            (850, 520, 'INVINCIBILITY'), (700, 320, 'JUMP_BOOST'), (250, 220, 'MAGNET')
        ]
        
        for x, y, powerup_type in powerup_positions:
            self.item_manager.spawn_item(x, y, powerup_type)

    def create_level_2(self):
        """Nivel 2 - Plataformas móviles"""
        print("🔧 CREANDO NIVEL 2 - PLATAFORMAS MÓVILES")
        
        self.player = Player(100, 500)
        self.all_sprites.add(self.player)
        
        # Plataforma base
        platform = pygame.sprite.Sprite()
        platform.image = self.create_platform_surface(SCREEN_WIDTH, 30, (100, 150, 200))
        platform.rect = platform.image.get_rect()
        platform.rect.x = 0
        platform.rect.y = SCREEN_HEIGHT - 30
        self.all_sprites.add(platform)
        self.platforms.add(platform)
        self.solid_platforms.add(platform)
        
        # Plataformas móviles
        moving_platforms = [
            # (x, y, width, height, color, move_x, move_y, distance)
            (200, 550, 120, 15, (150, 100, 200), 1, 0, 100),
            (500, 550, 120, 15, (150, 100, 200), 1, 0, 150),
            (350, 450, 100, 15, (150, 100, 200), 0, 1, 80),
            (600, 450, 100, 15, (150, 100, 200), 0, 1, 60),
            (450, 350, 80, 15, (150, 100, 200), 1, 0, 120),
            (250, 250, 80, 15, (150, 100, 200), 0, 1, 100),
            (650, 250, 80, 15, (150, 100, 200), 1, 0, 80)
        ]
        
        for data in moving_platforms:
            platform = MovingPlatform(*data)
            self.all_sprites.add(platform)
            self.platforms.add(platform)
            self.solid_platforms.add(platform)
        
        # Enemigos
        enemy_positions = [
            (300, 520, 'SHOOTER'), (600, 520, 'SHOOTER'), (450, 420, 'FLOATER'),
            (300, 320, 'SHOOTER'), (600, 320, 'SHOOTER'), (450, 220, 'FLOATER'),
            (200, 170, 'FLOATER'), (700, 170, 'FLOATER')
        ]
        
        for x, y, enemy_type in enemy_positions:
            enemy = self.enemy_manager.spawn_enemy(x, y, enemy_type)
            if enemy:
                self.all_sprites.add(enemy)
                self.position_enemy_on_platform(enemy)
        
        # Fragmentos en plataformas móviles
        fragment_positions = [
            (180, 520), (380, 520), (580, 520), (780, 520),
            (270, 420), (470, 420), (670, 420), (370, 320),
            (570, 320), (470, 220), (220, 170), (720, 170), (480, 90)
        ]
        
        for x, y in fragment_positions:
            item = self.item_manager.spawn_item(x, y, 'FRAGMENT')
            if item:
                self.position_item_on_platform(item)
        
        # Power-ups
        powerup_positions = [
            (800, 520, 'SPEED_BOOST'), (400, 320, 'INVINCIBILITY'),
            (650, 170, 'JUMP_BOOST'), (250, 170, 'MAGNET')
        ]
        
        for x, y, powerup_type in powerup_positions:
            self.item_manager.spawn_item(x, y, powerup_type)

    def create_level_3(self):
        """Nivel 3 - Plataformas de un solo sentido"""
        print("🔧 CREANDO NIVEL 3 - PLATAFORMAS DE UN SOLO SENTIDO")
        
        self.player = Player(100, 500)
        self.all_sprites.add(self.player)
        
        # Plataforma base
        platform = pygame.sprite.Sprite()
        platform.image = self.create_platform_surface(SCREEN_WIDTH, 30, (150, 100, 200))
        platform.rect = platform.image.get_rect()
        platform.rect.x = 0
        platform.rect.y = SCREEN_HEIGHT - 30
        self.all_sprites.add(platform)
        self.platforms.add(platform)
        self.solid_platforms.add(platform)
        
        # Plataformas de un solo sentido (verdes)
        one_way_platforms = [
            (200, 550, 150, 10), (400, 550, 150, 10), (600, 550, 150, 10), (800, 550, 150, 10),
            (300, 450, 120, 10), (500, 450, 120, 10), (700, 450, 120, 10),
            (400, 350, 100, 10), (600, 350, 100, 10),
            (500, 250, 80, 10), (300, 200, 80, 10), (700, 200, 80, 10),
            (450, 150, 60, 10)
        ]
        
        for x, y, width, height in one_way_platforms:
            platform = OneWayPlatform(x, y, width, height, (100, 200, 100))
            self.all_sprites.add(platform)
            self.platforms.add(platform)
            self.one_way_platforms.add(platform)
        
        # Enemigos más agresivos
        enemy_positions = [
            (150, 520, 'SHOOTER'), (450, 520, 'SHOOTER'), (750, 520, 'SHOOTER'),
            (250, 420, 'SHOOTER'), (550, 420, 'SHOOTER'), (350, 320, 'FLOATER'),
            (650, 320, 'FLOATER'), (450, 220, 'FLOATER'), (180, 170, 'SHOOTER'), (680, 170, 'SHOOTER')
        ]
        
        for x, y, enemy_type in enemy_positions:
            enemy = self.enemy_manager.spawn_enemy(x, y, enemy_type)
            if enemy:
                self.all_sprites.add(enemy)
                self.position_enemy_on_platform(enemy)
        
        # Fragmentos
        fragment_positions = [
            (50, 520), (350, 520), (650, 520), (130, 420), (430, 420), (730, 420),
            (230, 320), (530, 320), (330, 220), (630, 220), (430, 120), (180, 70), (680, 70)
        ]
        
        for x, y in fragment_positions:
            item = self.item_manager.spawn_item(x, y, 'FRAGMENT')  # ✅ CORREGIDO: 'FRAGMENT' -> 'FRAGMENT'
            if item:
                self.position_item_on_platform(item)
        
        # Power-ups
        powerup_positions = [
            (50, 520, 'INVINCIBILITY'), (730, 420, 'SPEED_BOOST'),
            (330, 220, 'JUMP_BOOST'), (630, 220, 'MAGNET'), (430, 120, 'INVINCIBILITY')
        ]
        
        for x, y, powerup_type in powerup_positions:
            self.item_manager.spawn_item(x, y, powerup_type)

    def create_level_4(self):
        """Nivel 4 - Combinación móvil + un solo sentido - CORREGIDO"""
        print("🔧 CREANDO NIVEL 4 - HÍBRIDO CORREGIDO")
        
        self.player = Player(100, 500)
        self.all_sprites.add(self.player)
        
        # Plataforma base
        platform = pygame.sprite.Sprite()
        platform.image = self.create_platform_surface(SCREEN_WIDTH, 30, (200, 100, 150))
        platform.rect = platform.image.get_rect()
        platform.rect.x = 0
        platform.rect.y = SCREEN_HEIGHT - 30
        self.all_sprites.add(platform)
        self.platforms.add(platform)
        self.solid_platforms.add(platform)
        
        # ✅ PLATAFORMAS MÓVILES CORREGIDAS - asegurar que sean sólidas
        moving_platforms = [
            # (x, y, width, height, color, move_x, move_y, distance)
            (150, 550, 100, 15, (180, 120, 200), 1, 0, 120),
            (450, 550, 100, 15, (180, 120, 200), 0, 1, 100),
            (750, 550, 100, 15, (180, 120, 200), 1, 0, 80),
            (300, 450, 80, 15, (180, 120, 200), 1, 1, 90),
            (600, 450, 80, 15, (180, 120, 200), 0, 1, 110)
        ]
        
        for data in moving_platforms:
            platform = MovingPlatform(*data)
            self.all_sprites.add(platform)
            self.platforms.add(platform)
            self.solid_platforms.add(platform)  # ✅ Asegurar que sean sólidas
        
        # ✅ PLATAFORMAS DE UN SOLO SENTIDO CORREGIDAS
        one_way_platforms = [
            (200, 400, 120, 10), (500, 400, 120, 10), 
            (350, 300, 100, 10), (650, 300, 100, 10), 
            (450, 200, 80, 10), (250, 150, 70, 10), (700, 150, 70, 10)
        ]
        
        for x, y, width, height in one_way_platforms:
            platform = OneWayPlatform(x, y, width, height, (100, 200, 150))
            self.all_sprites.add(platform)
            self.platforms.add(platform)
            self.one_way_platforms.add(platform)
        
        # ✅ ENEMIGOS CON POSICIONES MÁS PRECISAS
        enemy_positions = [
            (200, 520, 'SHOOTER'), (500, 520, 'SHOOTER'), (800, 520, 'SHOOTER'),
            (350, 420, 'FLOATER'), (650, 420, 'FLOATER'), 
            (450, 320, 'SHOOTER'), (300, 220, 'FLOATER'), 
            (600, 220, 'FLOATER'), (200, 120, 'SHOOTER'), (700, 120, 'SHOOTER')
        ]
        
        enemy_count = 0
        for x, y, enemy_type in enemy_positions:
            enemy = self.enemy_manager.spawn_enemy(x, y, enemy_type)
            if enemy:
                self.all_sprites.add(enemy)
                if self.position_enemy_on_platform(enemy):
                    enemy_count += 1
                else:
                    # Si no se pudo posicionar, eliminar el enemigo
                    enemy.kill()
                    print(f"⚠️ Enemigo en posición inválida: ({x}, {y})")
        
        print(f"👾 Enemigos colocados en nivel 4: {enemy_count}")
        
        # ✅ FRAGMENTOS CON VERIFICACIÓN DE COLOCACIÓN
        fragment_positions = [
            (180, 520), (480, 520), (780, 520), 
            (330, 420), (630, 420), (470, 320), 
            (320, 220), (620, 220), (220, 120), 
            (720, 120), (450, 180), (300, 80), (600, 80)
        ]
        
        fragment_count = 0
        for x, y in fragment_positions:
            item = self.item_manager.spawn_item(x, y, 'FRAGMENT')  # ✅ CORREGIDO: 'FRAGMENT' -> 'FRAGMENT'
            if item:
                if self.position_item_on_platform(item):
                    fragment_count += 1
                else:
                    # Si no se pudo posicionar, eliminar el item
                    item.kill()
                    print(f"⚠️ Fragmento en posición inválida: ({x}, {y})")
        
        print(f"🔵 Fragmentos colocados en nivel 4: {fragment_count}")
        
        # ✅ POWER-UPS ESENCIALES
        powerup_positions = [
            (800, 520, 'INVINCIBILITY'), (400, 320, 'SPEED_BOOST'),
            (650, 220, 'JUMP_BOOST'), (250, 120, 'MAGNET')
        ]
        
        for x, y, powerup_type in powerup_positions:
            item = self.item_manager.spawn_item(x, y, powerup_type)
            if item:
                self.position_item_on_platform(item)
        
        # ✅ VERIFICACIÓN FINAL
        total_enemies = len(self.enemy_manager.enemies)
        total_fragments = self.item_manager.get_fragment_count()
        total_items = len(self.item_manager.items)
        
        print(f"🎯 NIVEL 4 VERIFICACIÓN: {total_enemies} enemigos, {total_fragments} fragmentos, {total_items} items totales")
        
        if total_fragments == 0:
            print("❌ ERROR: No hay fragmentos en el nivel 4!")
            # Crear fragmentos de emergencia
            emergency_positions = [(100, 520), (900, 520), (450, 320)]
            for x, y in emergency_positions:
                item = self.item_manager.spawn_item(x, y, 'FRAGMENT')  # ✅ CORREGIDO: 'FRAGMENT' -> 'FRAGMENT'
                if item:
                    self.position_item_on_platform(item)
            print("🆘 Fragmentos de emergencia creados")

    def create_level_5(self):
        """Nivel 5 - Desafío extremo"""
        print("🔧 CREANDO NIVEL 5 - DESAFÍO EXTREMO")
        
        self.player = Player(50, 500)
        self.all_sprites.add(self.player)
        
        # Plataforma base pequeña
        platform = pygame.sprite.Sprite()
        platform.image = self.create_platform_surface(200, 20, (150, 80, 180))
        platform.rect = platform.image.get_rect()
        platform.rect.x = 0
        platform.rect.y = SCREEN_HEIGHT - 30
        self.all_sprites.add(platform)
        self.platforms.add(platform)
        self.solid_platforms.add(platform)
        
        # Plataformas móviles complejas
        moving_platforms = [
            (100, 550, 80, 10, (160, 100, 220), 1, 0, 200),
            (400, 550, 80, 10, (160, 100, 220), 0, 1, 150),
            (700, 550, 80, 10, (160, 100, 220), 1, 1, 120),
            (250, 450, 60, 10, (160, 100, 220), 1, 0, 180),
            (550, 450, 60, 10, (160, 100, 220), 0, 1, 130),
            (350, 350, 50, 10, (160, 100, 220), 1, 1, 100),
            (650, 350, 50, 10, (160, 100, 220), 1, 0, 160),
            (450, 250, 40, 10, (160, 100, 220), 0, 1, 140),
            (200, 200, 40, 10, (160, 100, 220), 1, 0, 120),
            (700, 200, 40, 10, (160, 100, 220), 0, 1, 110),
            (300, 150, 30, 10, (160, 100, 220), 1, 1, 90),
            (600, 150, 30, 10, (160, 100, 220), 1, 0, 80)
        ]
        
        for data in moving_platforms:
            platform = MovingPlatform(*data)
            self.all_sprites.add(platform)
            self.platforms.add(platform)
            self.solid_platforms.add(platform)
        
        # Enemigos muy agresivos
        enemy_positions = [
            (150, 520, 'SHOOTER'), (450, 520, 'SHOOTER'), (750, 520, 'SHOOTER'),
            (300, 420, 'SHOOTER'), (600, 420, 'SHOOTER'), (150, 320, 'FLOATER'),
            (450, 320, 'FLOATER'), (750, 320, 'FLOATER'), (300, 220, 'SHOOTER'),
            (600, 220, 'SHOOTER'), (150, 120, 'FLOATER'), (450, 120, 'FLOATER'), (750, 120, 'FLOATER')
        ]
        
        for x, y, enemy_type in enemy_positions:
            enemy = self.enemy_manager.spawn_enemy(x, y, enemy_type)
            if enemy:
                self.all_sprites.add(enemy)
                self.position_enemy_on_platform(enemy)
        
        # Fragmentos bien escondidos
        fragment_positions = [
            (130, 520), (430, 520), (730, 520), (280, 420), (580, 420),
            (130, 320), (430, 320), (730, 320), (280, 220), (580, 220),
            (130, 120), (430, 120), (730, 120), (450, 80), (300, 80), (600, 80)
        ]
        
        for x, y in fragment_positions:
            item = self.item_manager.spawn_item(x, y, 'FRAGMENT')  # ✅ CORREGIDO: 'FRAGMENT' -> 'FRAGMENT'
            if item:
                self.position_item_on_platform(item)

    def create_level_6(self):
        """Nivel 6 - Jefe final"""
        print("🔧 CREANDO NIVEL 6 - JEFE FINAL")
        
        self.player = Player(SCREEN_WIDTH // 2, 500)
        self.all_sprites.add(self.player)
        
        # Plataforma principal grande
        platform = pygame.sprite.Sprite()
        platform.image = self.create_platform_surface(SCREEN_WIDTH, 40, (180, 60, 200))
        platform.rect = platform.image.get_rect()
        platform.rect.x = 0
        platform.rect.y = SCREEN_HEIGHT - 40
        self.all_sprites.add(platform)
        self.platforms.add(platform)
        self.solid_platforms.add(platform)
        
        # Plataformas móviles rápidas
        moving_platforms = [
            (100, 550, 60, 8, (200, 80, 240), 1, 0, 250),
            (500, 550, 60, 8, (200, 80, 240), 0, 1, 200),
            (300, 450, 50, 8, (200, 80, 240), 1, 1, 180),
            (700, 450, 50, 8, (200, 80, 240), 1, 0, 220),
            (200, 350, 40, 8, (200, 80, 240), 0, 1, 190),
            (600, 350, 40, 8, (200, 80, 240), 1, 1, 170),
            (400, 250, 30, 8, (200, 80, 240), 1, 0, 210),
            (800, 250, 30, 8, (200, 80, 240), 0, 1, 160),
            (150, 150, 25, 8, (200, 80, 240), 1, 1, 140),
            (650, 150, 25, 8, (200, 80, 240), 1, 0, 230)
        ]
        
        for data in moving_platforms:
            platform = MovingPlatform(*data)
            platform.speed = 3  # Más rápido
            self.all_sprites.add(platform)
            self.platforms.add(platform)
            self.solid_platforms.add(platform)
        
        # MUCHOS enemigos
        enemy_positions = [
            (100, 520, 'SHOOTER'), (300, 520, 'SHOOTER'), (500, 520, 'SHOOTER'), 
            (700, 520, 'SHOOTER'), (900, 520, 'SHOOTER'), (200, 420, 'FLOATER'),
            (400, 420, 'FLOATER'), (600, 420, 'FLOATER'), (800, 420, 'FLOATER'),
            (150, 320, 'SHOOTER'), (350, 320, 'SHOOTER'), (550, 320, 'SHOOTER'),
            (750, 320, 'SHOOTER'), (250, 220, 'FLOATER'), (450, 220, 'FLOATER'),
            (650, 220, 'FLOATER'), (850, 220, 'FLOATER'), (100, 120, 'SHOOTER'),
            (300, 120, 'SHOOTER'), (500, 120, 'SHOOTER'), (700, 120, 'SHOOTER'), (900, 120, 'SHOOTER')
        ]
        
        for x, y, enemy_type in enemy_positions:
            enemy = self.enemy_manager.spawn_enemy(x, y, enemy_type)
            if enemy:
                self.all_sprites.add(enemy)
                self.position_enemy_on_platform(enemy)
        
        # Fragmentos por todos lados
        fragment_positions = [
            (80, 520), (280, 520), (480, 520), (680, 520), (880, 520),
            (180, 420), (380, 420), (580, 420), (780, 420), (130, 320),
            (330, 320), (530, 320), (730, 320), (230, 220), (430, 220),
            (630, 220), (830, 220), (70, 120), (270, 120), (470, 120),
            (670, 120), (870, 120), (450, 80), (250, 80), (650, 80)
        ]
        
        for x, y in fragment_positions:
            item = self.item_manager.spawn_item(x, y, 'FRAGMENT')  # ✅ CORREGIDO: 'FRAGMENT' -> 'FRAGMENT'
            if item:
                self.position_item_on_platform(item)

    def position_enemy_on_platform(self, enemy):
        """Posicionar enemigo sobre plataforma"""
        for platform in self.platforms:
            if (platform.rect.left <= enemy.rect.centerx <= platform.rect.right and
                abs(enemy.rect.bottom - platform.rect.top) < 50):
                enemy.rect.bottom = platform.rect.top
                enemy.on_ground = True
                return True
        return False

    def position_item_on_platform(self, item):
        """Posicionar item sobre plataforma"""
        for platform in self.platforms:
            if (platform.rect.left <= item.rect.centerx <= platform.rect.right and
                abs(item.rect.bottom - platform.rect.top) < 100):
                item.rect.bottom = platform.rect.top - 10
                return True
        return False

    def create_stars(self):
        stars = []
        for _ in range(100):
            stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT), 
                'speed': random.uniform(0.1, 0.5),
                'size': random.randint(1, 3),
                'brightness': random.randint(150, 255)
            })
        return stars

    def update_stars(self):
        for star in self.stars:
            star['x'] -= star['speed']
            if star['x'] < 0:
                star['x'] = SCREEN_WIDTH
                star['y'] = random.randint(0, SCREEN_HEIGHT)

    def draw_stars(self):
        for star in self.stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), star['size'])

    def handle_platform_collisions(self):
        """✅ SISTEMA MEJORADO DE COLISIONES CON PLATAFORMAS"""
        # Colisión con plataformas sólidas
        hits = pygame.sprite.spritecollide(self.player, self.solid_platforms, False)
        if hits:
            # Colisión desde arriba
            if self.player.vel_y > 0:
                self.player.rect.bottom = hits[0].rect.top
                self.player.vel_y = 0
                self.player.on_ground = True
            # Colisión desde abajo  
            elif self.player.vel_y < 0:
                self.player.rect.top = hits[0].rect.bottom
                self.player.vel_y = 0
        
        # Colisión con plataformas de un solo sentido
        one_way_hits = pygame.sprite.spritecollide(self.player, self.one_way_platforms, False)
        if one_way_hits:
            # Solo colisiona si viene desde arriba
            if self.player.vel_y > 0 and self.player.rect.bottom <= one_way_hits[0].rect.top + 10:
                self.player.rect.bottom = one_way_hits[0].rect.top
                self.player.vel_y = 0
                self.player.on_ground = True

    def handle_attack_collisions(self):
        """Manejar colisiones de ataques con enemigos"""
        if not self.player.attacking:
            return
            
        attack_hitbox = self.player.get_attack_hitbox()
        
        for enemy in list(self.enemy_manager.enemies):
            if attack_hitbox.colliderect(enemy.rect):
                print(f"⚔️ ¡Enemigo golpeado! Tipo: {enemy.enemy_type}")
                
                # Destruir enemigo
                enemy.kill()
                self.play_sound(self.enemy_death_sound)
                
                # Recompensa
                self.player.add_score(200)
                
                # Efectos visuales
                self.create_enemy_death_particles(enemy.rect.centerx, enemy.rect.centery)
                break

    def create_enemy_death_particles(self, x, y):
        """Crear partículas cuando un enemigo es destruido"""
        for i in range(15):
            self.player.attack_particles.append({
                'x': x,
                'y': y,
                'vel_x': random.uniform(-3, 3),
                'vel_y': random.uniform(-3, 3),
                'color': (255, 100, 100),
                'life': 30,
                'size': random.randint(2, 6)
            })

    def handle_collisions(self):
        # ✅ COLISIONES MEJORADAS CON PLATAFORMAS
        self.handle_platform_collisions()
        
        # Colisiones enemigos con plataformas
        for enemy in self.enemy_manager.enemies:
            enemy_hits = pygame.sprite.spritecollide(enemy, self.platforms, False)
            if enemy_hits and enemy.vel_y > 0:
                enemy.rect.bottom = enemy_hits[0].rect.top
                enemy.vel_y = 0
                enemy.on_ground = True
        
        # Colisiones con ataques
        self.handle_attack_collisions()
        
        # Colisiones con items
        collected = self.item_manager.check_collisions(self.player)
        if collected > 0:
            print(f"🎯 Items recolectados: {collected}")
            self.play_sound(self.collect_sound)
        
        # Colisiones con enemigos (daño al jugador)
        if not self.player.powerups['invincibility']['active']:
            enemy_hits = self.enemy_manager.check_collisions(self.player)
            projectile_hits = self.enemy_manager.check_projectile_collisions(self.player)
            
            if enemy_hits or projectile_hits:
                self.player.take_damage()
                self.play_sound(self.hurt_sound)
                if self.player.lives <= 0:
                    self.game_state = GAME_OVER
        
        # ✅ VERIFICACIÓN DE VICTORIA - SIMPLIFICADA Y EFECTIVA
        current_fragments = self.item_manager.get_fragment_count()
        current_enemies = len(self.enemy_manager.enemies)
        
        print(f"🔍 Nivel {self.current_level}: {current_fragments} fragmentos, {current_enemies} enemigos")
        
        # ✅ DEBUG TEMPORAL: Presiona P para forzar completado
        if pygame.key.get_pressed()[pygame.K_p]:  # Presiona P para forzar completar nivel
            print("🔄 FORZANDO COMPLETADO DE NIVEL (DEBUG)")
            self.level_completed = True
            self.game_state = LEVEL_COMPLETE
            return
        
        # ✅ VERIFICACIÓN DIRECTA - Si no hay fragmentos y no hay enemigos
        if current_fragments <= 0 and current_enemies <= 0:
            if not self.level_completed and self.player.lives > 0:
                print(f"🎉 ¡NIVEL {self.current_level} COMPLETADO!")
                self.level_completed = True
                self.game_state = LEVEL_COMPLETE
                self.player.add_score(1000 + (self.current_level * 500))
                if hasattr(self, 'level_complete_sound'):
                    self.play_sound(self.level_complete_sound)

    def next_level(self):
        """Pasar al siguiente nivel"""
        if self.current_level < 6:  # ✅ Ahora hay 6 niveles
            self.current_level += 1
            self.level_completed = False
            self.reset_game()
            self.game_state = PLAYING
            pygame.display.set_caption(f"Aether Runner - Nivel {self.current_level}")
            print(f"🚀 AVANZANDO AL NIVEL {self.current_level}")
        else:
            print("🏆 ¡JUEGO COMPLETADO!")
            self.game_state = LEVEL_COMPLETE

    def draw_hud(self):
        # Puntuación
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Puntos: {self.player.score}', True, TEXT_COLOR)
        
        hud_bg = pygame.Surface((200, 40), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 128))
        self.screen.blit(hud_bg, (SCREEN_WIDTH - 210, 10))
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 20))
        
        # Nivel
        level_text = font.render(f'Nivel: {self.current_level}/6', True, TEXT_COLOR)
        self.screen.blit(level_text, (SCREEN_WIDTH - 210, 50))
        
        # Vidas
        lives_text = font.render(f'Vidas: {self.player.lives}', True, TEXT_COLOR)
        self.screen.blit(lives_text, (20, 20))
        
        # Fragmentos
        fragment_count = self.item_manager.get_fragment_count()
        fragment_text = font.render(f'Fragmentos: {fragment_count}', True, (100, 200, 255))
        self.screen.blit(fragment_text, (20, 60))
        
        # Enemigos restantes
        enemy_count = len(self.enemy_manager.enemies)
        enemy_text = font.render(f'Enemigos: {enemy_count}', True, (255, 100, 100))
        self.screen.blit(enemy_text, (20, 100))

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        print("🔄 JUEGO REINICIADO")
                    if event.key == pygame.K_n and self.game_state == LEVEL_COMPLETE:
                        self.next_level()
                    if event.key == pygame.K_x and self.player.attack_cooldown == 0:
                        self.player.attack()
                        self.play_sound(self.attack_sound)
                    if event.key == pygame.K_m:
                        # Control de música
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

            if self.game_state == PLAYING:
                self.all_sprites.update()
                self.item_manager.update()
                self.enemy_manager.update(self.player)
                self.handle_collisions()
                self.update_stars()

            # Dibujar
            self.screen.fill(BACKGROUND_COLOR)
            self.draw_stars()
            self.all_sprites.draw(self.screen)
            self.item_manager.draw(self.screen)
            self.enemy_manager.draw_projectiles(self.screen)
            
            # Dibujar hitbox de ataque (debug)
            if self.player.attacking:
                attack_hitbox = self.player.get_attack_hitbox()
                pygame.draw.rect(self.screen, (255, 0, 0), attack_hitbox, 2)
            
            # Partículas
            self.player.update_particles()
            self.item_manager.update_particles(self.screen)
            
            # Dibujar partículas del jugador
            for particle in self.player.jump_particles:
                pygame.draw.circle(
                    self.screen, 
                    particle['color'],
                    (int(particle['x']), int(particle['y'])),
                    particle['size']
                )

            for particle in self.player.attack_particles:
                pygame.draw.circle(
                    self.screen,
                    particle['color'],
                    (int(particle['x']), int(particle['y'])),
                    particle['size']
                )
            
            # HUD
            self.draw_hud()
            self.player.draw_health_bar(self.screen)
            self.player.draw_powerup_indicators(self.screen)
            
            # Controles en pantalla
            font = pygame.font.Font(None, 24)
            controls_text = font.render("CONTROLES: FLECHAS=MOVER, ESPACIO=SALTAR, X=ATACAR, M=MÚSICA, P=DEBUG", True, (200, 200, 255))
            self.screen.blit(controls_text, (SCREEN_WIDTH//2 - 220, SCREEN_HEIGHT - 30))

            # Estados especiales
            if self.game_state == LEVEL_COMPLETE:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                self.screen.blit(overlay, (0, 0))
                
                font = pygame.font.Font(None, 72)
                
                if self.current_level < 6:
                    text = font.render(f'NIVEL {self.current_level} COMPLETO!', True, (100, 255, 100))
                    self.screen.blit(text, (SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 - 50))
                    
                    inst_font = pygame.font.Font(None, 36)
                    inst_text = inst_font.render('Presiona N para siguiente nivel', True, TEXT_COLOR)
                    self.screen.blit(inst_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 + 30))
                else:
                    text = font.render('¡JUEGO COMPLETADO!', True, (255, 215, 0))
                    self.screen.blit(text, (SCREEN_WIDTH//2 - 220, SCREEN_HEIGHT//2 - 50))
                    
                    score_font = pygame.font.Font(None, 48)
                    score_text = score_font.render(f'Puntuación Final: {self.player.score}', True, (255, 255, 255))
                    self.screen.blit(score_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 + 50))
                
            elif self.game_state == GAME_OVER:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                self.screen.blit(overlay, (0, 0))
                
                font = pygame.font.Font(None, 72)
                text = font.render('GAME OVER', True, (255, 50, 50))
                self.screen.blit(text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 - 50))

            pygame.display.flip()

        pygame.quit()
        sys.exit()