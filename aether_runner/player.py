# player.py - PERSONAJE ANIME COMPLETO
import pygame
import os
import random
import math
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Sistema de animaciones anime
        self.animations = {}
        self.load_anime_sprites()
        
        # Configuración de animación
        self.current_animation = 'idle'
        self.current_frame = 0
        self.animation_speed = 0.15
        self.facing_right = True
        
        # Sprite inicial
        self.image = self.animations['idle_right'][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Física y movimiento
        self.vel_x = 0
        self.vel_y = 0
        self.acc_x = 0
        
        # Estados
        self.on_ground = False
        self.double_jump_available = True
        self.sliding = False
        self.attacking = False
        self.attack_cooldown = 0
        self.hurt_timer = 0
        
        # Stats
        self.lives = 3
        self.score = 0
        self.attack_power = 1
        self.coins = 0
        
        # Sistema de power-ups
        self.powerups = {
            'invincibility': {'active': False, 'timer': 0, 'duration': 5000},
            'jump_boost': {'active': False, 'timer': 0, 'duration': 8000},
            'magnet': {'active': False, 'timer': 0, 'duration': 10000},
            'speed_boost': {'active': False, 'timer': 0, 'duration': 6000}
        }
        
        # Efectos
        self.jump_particles = []
        self.attack_particles = []
        self.trail_particles = []
        self.trail_timer = 0
        
        # Stats base
        self.normal_speed = PLAYER_SPEED
        self.normal_jump = PLAYER_JUMP
        
    def load_anime_sprites(self):
        """Crear sprites estilo anime programáticamente"""
        # Colores del personaje
        self.hair_color = (200, 220, 255)  # Plateado-azul
        self.skin_color = (255, 220, 180)  # Piel anime
        self.armor_color = (80, 100, 200)  # Azul armadura
        self.cape_color = (60, 80, 180)    # Azul oscuro capa
        self.energy_color = (100, 200, 255) # Azul energía
        
        # Animación IDLE (4 frames)
        self.animations['idle_right'] = [self.create_idle_sprite(i) for i in range(4)]
        self.animations['idle_left'] = [pygame.transform.flip(sprite, True, False) 
                                      for sprite in self.animations['idle_right']]
        
        # Animación RUN (6 frames)
        self.animations['run_right'] = [self.create_run_sprite(i) for i in range(6)]
        self.animations['run_left'] = [pygame.transform.flip(sprite, True, False) 
                                     for sprite in self.animations['run_right']]
        
        # Animación JUMP (3 frames)
        self.animations['jump_right'] = [self.create_jump_sprite(i) for i in range(3)]
        self.animations['jump_left'] = [pygame.transform.flip(sprite, True, False) 
                                      for sprite in self.animations['jump_right']]
        
        # Animación ATTACK (4 frames)
        self.animations['attack_right'] = [self.create_attack_sprite(i) for i in range(4)]
        self.animations['attack_left'] = [pygame.transform.flip(sprite, True, False) 
                                        for sprite in self.animations['attack_right']]
        
        # Animación SLIDE (2 frames)
        self.animations['slide_right'] = [self.create_slide_sprite(i) for i in range(2)]
        self.animations['slide_left'] = [pygame.transform.flip(sprite, True, False) 
                                       for sprite in self.animations['slide_right']]
        
        # Animación HURT (2 frames)
        self.animations['hurt_right'] = [self.create_hurt_sprite(i) for i in range(2)]
        self.animations['hurt_left'] = [pygame.transform.flip(sprite, True, False) 
                                      for sprite in self.animations['hurt_right']]

    def create_idle_sprite(self, frame):
        """Crear sprite idle con animación sutil"""
        surface = pygame.Surface((40, 60), pygame.SRCALPHA)
        
        # Capa (ondea suavemente)
        cape_offset = math.sin(frame * 0.5) * 2
        pygame.draw.ellipse(surface, self.cape_color, (5, 15 + cape_offset, 30, 40))
        
        # Cuerpo
        pygame.draw.ellipse(surface, self.armor_color, (10, 20, 20, 30))
        
        # Cabeza
        pygame.draw.circle(surface, self.skin_color, (20, 15), 8)
        
        # Cabello (con movimiento sutil)
        hair_offset = math.sin(frame * 0.3) * 1
        hair_points = [
            (15, 8), (25, 8),
            (28 + hair_offset, 12), (25, 18),
            (15, 18), (12 + hair_offset, 12)
        ]
        pygame.draw.polygon(surface, self.hair_color, hair_points)
        
        # Ojos anime
        eye_y = 13
        pygame.draw.ellipse(surface, (255, 255, 255), (15, eye_y, 4, 6))
        pygame.draw.ellipse(surface, (255, 255, 255), (21, eye_y, 4, 6))
        pygame.draw.ellipse(surface, (80, 100, 200), (16, eye_y + 1, 2, 4))
        pygame.draw.ellipse(surface, (80, 100, 200), (22, eye_y + 1, 2, 4))
        
        # Brillo ojos
        pygame.draw.ellipse(surface, (255, 255, 255), (16, eye_y + 2, 1, 1))
        pygame.draw.ellipse(surface, (255, 255, 255), (22, eye_y + 2, 1, 1))
        
        # Efecto de energía sutil
        energy_alpha = 30 + int(math.sin(frame) * 10)
        energy_surface = pygame.Surface((40, 60), pygame.SRCALPHA)
        pygame.draw.circle(energy_surface, (*self.energy_color, energy_alpha), (20, 30), 25)
        surface.blit(energy_surface, (0, 0))
        
        return surface

    def create_run_sprite(self, frame):
        """Crear sprite de corrida con movimiento dinámico"""
        surface = pygame.Surface((45, 60), pygame.SRCALPHA)
        
        # Posiciones de brazos y piernas según frame
        arm_angles = [20, 10, 0, -10, -20, -10]
        leg_angles = [-15, -25, -35, -25, -15, -5]
        
        # Capa (movimiento dramático)
        cape_swing = math.sin(frame * 1.2) * 8
        pygame.draw.ellipse(surface, self.cape_color, (5 + cape_swing, 15, 35, 40))
        
        # Cuerpo (inclinado)
        body_tilt = math.sin(frame * 0.8) * 3
        pygame.draw.ellipse(surface, self.armor_color, (12 + body_tilt, 20, 20, 30))
        
        # Cabeza
        pygame.draw.circle(surface, self.skin_color, (22 + body_tilt, 15), 8)
        
        # Brazos en movimiento
        arm_x = 22 + body_tilt
        arm_length = 12
        arm_angle = math.radians(arm_angles[frame])
        arm_end_x = arm_x + math.cos(arm_angle) * arm_length
        arm_end_y = 25 + math.sin(arm_angle) * arm_length
        pygame.draw.line(surface, self.skin_color, (arm_x, 25), (arm_end_x, arm_end_y), 3)
        
        # Piernas en movimiento
        leg_x = 22 + body_tilt
        leg_length = 15
        leg_angle = math.radians(leg_angles[frame])
        leg_end_x = leg_x + math.cos(leg_angle) * leg_length
        leg_end_y = 50 + math.sin(leg_angle) * leg_length
        pygame.draw.line(surface, self.armor_color, (leg_x, 50), (leg_end_x, leg_end_y), 4)
        
        # Cabello (movimiento por velocidad)
        hair_points = [
            (17 + body_tilt, 8), (27 + body_tilt, 8),
            (30 + body_tilt + cape_swing * 0.5, 12), 
            (27 + body_tilt, 18), (17 + body_tilt, 18),
            (14 + body_tilt + cape_swing * 0.5, 12)
        ]
        pygame.draw.polygon(surface, self.hair_color, hair_points)
        
        # Ojos determinados
        eye_y = 13
        pygame.draw.ellipse(surface, (255, 255, 255), (18 + body_tilt, eye_y, 3, 5))
        pygame.draw.ellipse(surface, (255, 255, 255), (24 + body_tilt, eye_y, 3, 5))
        pygame.draw.ellipse(surface, (80, 100, 200), (19 + body_tilt, eye_y + 1, 1, 3))
        pygame.draw.ellipse(surface, (80, 100, 200), (25 + body_tilt, eye_y + 1, 1, 3))
        
        # Efecto de velocidad
        if frame in [2, 3]:
            speed_surface = pygame.Surface((45, 60), pygame.SRCALPHA)
            for i in range(3):
                offset = (frame - 2) * 5 + i * 3
                pygame.draw.ellipse(speed_surface, (*self.energy_color, 100 - i * 30), 
                                  (5 - offset, 20, 35, 25))
            surface.blit(speed_surface, (0, 0))
        
        return surface

    def create_jump_sprite(self, frame):
        """Crear sprite de salto"""
        surface = pygame.Surface((42, 65), pygame.SRCALPHA)
        
        # Altura del salto según frame
        jump_height = [0, -8, -15][frame]
        
        # Capa (ondea hacia arriba)
        pygame.draw.ellipse(surface, self.cape_color, (6, 20 + jump_height, 30, 35))
        
        # Cuerpo (estirado)
        pygame.draw.ellipse(surface, self.armor_color, (11, 25 + jump_height, 20, 25))
        
        # Cabeza
        pygame.draw.circle(surface, self.skin_color, (21, 18 + jump_height), 8)
        
        # Brazos extendidos
        pygame.draw.line(surface, self.skin_color, (21, 28 + jump_height), (15, 35 + jump_height), 3)
        pygame.draw.line(surface, self.skin_color, (21, 28 + jump_height), (27, 35 + jump_height), 3)
        
        # Piernas flexionadas
        pygame.draw.line(surface, self.armor_color, (21, 48 + jump_height), (16, 55 + jump_height), 4)
        pygame.draw.line(surface, self.armor_color, (21, 48 + jump_height), (26, 55 + jump_height), 4)
        
        # Cabello (flotando)
        hair_points = [
            (16, 11 + jump_height), (26, 11 + jump_height),
            (29, 15 + jump_height), (26, 21 + jump_height),
            (16, 21 + jump_height), (13, 15 + jump_height)
        ]
        pygame.draw.polygon(surface, self.hair_color, hair_points)
        
        # Ojos emocionados
        eye_y = 16 + jump_height
        pygame.draw.ellipse(surface, (255, 255, 255), (17, eye_y, 3, 4))
        pygame.draw.ellipse(surface, (255, 255, 255), (23, eye_y, 3, 4))
        pygame.draw.ellipse(surface, (60, 80, 180), (17, eye_y + 1, 2, 2))
        pygame.draw.ellipse(surface, (60, 80, 180), (23, eye_y + 1, 2, 2))
        
        # Partículas de salto
        if frame == 0:
            for i in range(3):
                pygame.draw.circle(surface, self.energy_color, 
                                 (10 + i * 10, 60), 2)
        
        return surface

    def create_attack_sprite(self, frame):
        """Crear sprite de ataque"""
        surface = pygame.Surface((50, 60), pygame.SRCALPHA)
        
        # Intensidad del ataque
        attack_power = [0.3, 0.7, 1.0, 0.5][frame]
        
        # Cuerpo (postura de ataque)
        pygame.draw.ellipse(surface, self.armor_color, (15, 20, 20, 30))
        
        # Cabeza
        pygame.draw.circle(surface, self.skin_color, (25, 15), 8)
        
        # Brazo de ataque
        arm_angle = math.radians(-30 + frame * 25)
        arm_start_x, arm_start_y = 25, 28
        arm_end_x = arm_start_x + math.cos(arm_angle) * 20
        arm_end_y = arm_start_y + math.sin(arm_angle) * 20
        
        pygame.draw.line(surface, self.skin_color, (arm_start_x, arm_start_y), 
                        (arm_end_x, arm_end_y), 4)
        
        # Espada/arma energética
        sword_length = 15 + frame * 5
        sword_angle = arm_angle + math.radians(10)
        sword_end_x = arm_end_x + math.cos(sword_angle) * sword_length
        sword_end_y = arm_end_y + math.sin(sword_angle) * sword_length
        
        pygame.draw.line(surface, self.energy_color, (arm_end_x, arm_end_y),
                        (sword_end_x, sword_end_y), 3)
        
        # Efecto de ataque
        if frame >= 1:
            attack_surface = pygame.Surface((50, 60), pygame.SRCALPHA)
            for i in range(3):
                trail_x = sword_end_x - i * 3
                trail_y = sword_end_y - i * 2
                radius = 5 - i
                alpha = 150 - i * 50
                pygame.draw.circle(attack_surface, (*self.energy_color, alpha),
                                (int(trail_x), int(trail_y)), radius)
            surface.blit(attack_surface, (0, 0))
        
        # Cabello (movimiento por el ataque)
        hair_swing = frame * 3
        hair_points = [
            (20, 8), (30, 8),
            (33 + hair_swing, 12), (30, 18),
            (20, 18), (17 + hair_swing, 12)
        ]
        pygame.draw.polygon(surface, self.hair_color, hair_points)
        
        # Ojos concentrados
        eye_close = min(frame, 1)
        eye_height = 4 - eye_close * 2
        pygame.draw.ellipse(surface, (255, 255, 255), (21, 14, 3, eye_height))
        pygame.draw.ellipse(surface, (255, 255, 255), (27, 14, 3, eye_height))
        
        return surface

    def create_slide_sprite(self, frame):
        """Crear sprite de deslizamiento"""
        surface = pygame.Surface((50, 35), pygame.SRCALPHA)
        
        # Cuerpo bajo y aerodinámico
        pygame.draw.ellipse(surface, self.armor_color, (15, 10, 25, 20))
        
        # Cabeza (bajada)
        head_y = 8 + frame * 2
        pygame.draw.circle(surface, self.skin_color, (25, head_y), 6)
        
        # Cabello (pegado al cuerpo)
        hair_points = [
            (22, head_y - 4), (28, head_y - 4),
            (30, head_y), (28, head_y + 2),
            (22, head_y + 2), (20, head_y)
        ]
        pygame.draw.polygon(surface, self.hair_color, hair_points)
        
        # Brazos extendidos hacia atrás
        pygame.draw.line(surface, self.skin_color, (20, 15), (10, 20), 3)
        pygame.draw.line(surface, self.skin_color, (30, 15), (40, 20), 3)
        
        # Efecto de velocidad
        speed_surface = pygame.Surface((50, 35), pygame.SRCALPHA)
        for i in range(5):
            offset = i * 8 + frame * 4
            alpha = 150 - i * 30
            pygame.draw.ellipse(speed_surface, (*self.energy_color, alpha),
                             (5 - offset, 12, 40, 15))
        surface.blit(speed_surface, (0, 0))
        
        return surface

    def create_hurt_sprite(self, frame):
        """Crear sprite de daño"""
        surface = pygame.Surface((40, 60), pygame.SRCALPHA)
        
        # Cuerpo encogido
        body_shrink = frame * 2
        pygame.draw.ellipse(surface, self.armor_color, 
                          (10 + body_shrink, 20, 20 - body_shrink * 2, 30))
        
        # Cabeza (inclinada)
        head_tilt = frame * 3
        pygame.draw.circle(surface, self.skin_color, (20 + head_tilt, 15), 7)
        
        # Cabello despeinado
        hair_points = [
            (18, 8), (22, 6),
            (26, 8), (24, 12),
            (20, 14), (16, 12)
        ]
        pygame.draw.polygon(surface, self.hair_color, hair_points)
        
        # Ojos cerrados/entrecerrados
        if frame == 0:
            # Ojos entrecerrados
            pygame.draw.line(surface, (80, 100, 200), (17, 14), (19, 14), 2)
            pygame.draw.line(surface, (80, 100, 200), (21, 14), (23, 14), 2)
        else:
            # Ojos completamente cerrados
            pygame.draw.line(surface, (100, 80, 80), (16, 14), (20, 14), 2)
            pygame.draw.line(surface, (100, 80, 80), (20, 14), (24, 14), 2)
        
        # Efecto de daño (rojo)
        if frame == 1:
            hurt_surface = pygame.Surface((40, 60), pygame.SRCALPHA)
            hurt_surface.fill((255, 100, 100, 80))
            surface.blit(hurt_surface, (0, 0))
        
        return surface

    def update_powerups(self):
        """Actualizar temporizadores de power-ups activos"""
        current_time = pygame.time.get_ticks()
        
        for powerup_type, data in self.powerups.items():
            if data['active']:
                # Reducir timer y desactivar si se acaba el tiempo
                if current_time - data['timer'] > data['duration']:
                    self.deactivate_powerup(powerup_type)

    def activate_powerup(self, powerup_type, duration=None):
        """Activar un power-up"""
        if duration is None:
            duration = self.powerups[powerup_type]['duration']
            
        self.powerups[powerup_type]['active'] = True
        self.powerups[powerup_type]['timer'] = pygame.time.get_ticks()
        self.powerups[powerup_type]['duration'] = duration
        
        # Aplicar efectos inmediatos
        if powerup_type == 'speed_boost':
            self.normal_speed = PLAYER_SPEED
        elif powerup_type == 'jump_boost':
            self.normal_jump = PLAYER_JUMP
            
        print(f"✨ Power-up activado: {powerup_type}")

    def deactivate_powerup(self, powerup_type):
        """Desactivar un power-up"""
        self.powerups[powerup_type]['active'] = False
        
        # Remover efectos
        if powerup_type == 'speed_boost':
            self.normal_speed = PLAYER_SPEED
        elif powerup_type == 'jump_boost':
            self.normal_jump = PLAYER_JUMP
            
        print(f"🔚 Power-up desactivado: {powerup_type}")

    def has_powerup(self, powerup_type):
        """Verificar si un power-up está activo"""
        return self.powerups[powerup_type]['active']

    def get_powerup_time_left(self, powerup_type):
        """Obtener tiempo restante del power-up en segundos"""
        if not self.powerups[powerup_type]['active']:
            return 0
            
        current_time = pygame.time.get_ticks()
        time_passed = current_time - self.powerups[powerup_type]['timer']
        time_left = max(0, self.powerups[powerup_type]['duration'] - time_passed)
        return time_left / 1000  # Convertir a segundos

    def update(self):
        """Actualizar animación y estado"""
        self.handle_movement()
        self.apply_physics()
        self.animate()
        self.update_powerups()
        self.update_attack()
        self.update_particles()
        
        # Cooldown de ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Timer de daño
        if self.hurt_timer > 0:
            self.hurt_timer -= 1

    def handle_movement(self):
        """Manejar entrada del jugador"""
        self.acc_x = 0
        keys = pygame.key.get_pressed()
        
        moving = False
        
        # Movimiento izquierda/derecha
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc_x = -PLAYER_ACCELERATION
            self.facing_right = False
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc_x = PLAYER_ACCELERATION
            self.facing_right = True
            moving = True
            
        # Deslizarse
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.sliding = True
        else:
            self.sliding = False
            
        # Saltar
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
            self.jump()
            
        # Atacar
        if keys[pygame.K_x] and self.attack_cooldown == 0:
            self.attack()

    def animate(self):
        """Seleccionar y actualizar animación actual"""
        direction = 'right' if self.facing_right else 'left'
        
        # Prioridad de animaciones
        if self.hurt_timer > 0:
            new_animation = 'hurt'
        elif self.attacking:
            new_animation = 'attack'
        elif self.sliding and self.on_ground:
            new_animation = 'slide'
        elif not self.on_ground:
            new_animation = 'jump'
        elif abs(self.vel_x) > 0.5:
            new_animation = 'run'
        else:
            new_animation = 'idle'
        
        # Cambiar animación si es necesario
        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.current_frame = 0
        
        # Actualizar frame
        animation_key = f"{self.current_animation}_{direction}"
        animation = self.animations[animation_key]
        
        self.current_frame += self.animation_speed
        if self.current_frame >= len(animation):
            if self.current_animation == 'attack':
                self.attacking = False
                self.current_animation = 'idle'
                animation_key = f"idle_{direction}"
                animation = self.animations[animation_key]
            self.current_frame = 0
        
        self.image = animation[int(self.current_frame)]
        
        # Efecto de invencibilidad (parpadeo)
        if self.powerups['invincibility']['active']:
            if pygame.time.get_ticks() % 200 < 100:
                invincible_surface = self.image.copy()
                invincible_surface.fill((255, 255, 100, 128), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = invincible_surface

    def jump(self):
        """Manejar salto"""
        jump_power = self.normal_jump
        
        if self.powerups['jump_boost']['active']:
            jump_power *= 1.5
        
        if self.on_ground:
            self.vel_y = jump_power
            self.on_ground = False
            self.double_jump_available = True
            self.create_jump_particles()
        elif self.double_jump_available and self.vel_y < 0:
            self.vel_y = jump_power * 0.8
            self.double_jump_available = False
            self.create_jump_particles()

    def attack(self):
        """Realizar ataque"""
        self.attacking = True
        self.attack_cooldown = 20  # 20 frames de cooldown
        self.create_attack_particles()
        print("⚔️ Ataque realizado!")

    def update_attack(self):
        """Actualizar estado de ataque"""
        pass  # La lógica de colisión de ataque se maneja en game.py

    def create_jump_particles(self):
        """Crear partículas de salto"""
        for i in range(8):
            self.jump_particles.append({
                'x': self.rect.centerx,
                'y': self.rect.bottom,
                'vel_x': random.uniform(-2, 2),
                'vel_y': random.uniform(-4, -2),
                'color': self.energy_color,
                'life': 20,
                'size': random.randint(2, 4)
            })

    def create_attack_particles(self):
        """Crear partículas de ataque"""
        direction = 1 if self.facing_right else -1
        for i in range(12):
            self.attack_particles.append({
                'x': self.rect.centerx + direction * 20,
                'y': self.rect.centery,
                'vel_x': direction * random.uniform(3, 6) + random.uniform(-1, 1),
                'vel_y': random.uniform(-2, 2),
                'color': self.energy_color,
                'life': 15,
                'size': random.randint(2, 5)
            })

    def update_particles(self):
        """Actualizar partículas (se dibujan en game.py)"""
        # Partículas de salto
        for particle in self.jump_particles[:]:
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.jump_particles.remove(particle)
        
        # Partículas de ataque
        for particle in self.attack_particles[:]:
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.attack_particles.remove(particle)

    def apply_physics(self):
        """Aplicar física al jugador"""
        # Aplicar fricción
        self.acc_x += self.vel_x * PLAYER_FRICTION
        
        # Actualizar velocidad
        self.vel_x += self.acc_x
        self.vel_y += PLAYER_GRAVITY
        
        # Limitar velocidad máxima
        speed_multiplier = 1.5 if self.powerups['speed_boost']['active'] else 1.0
        max_speed = self.normal_speed * speed_multiplier
        self.vel_x = max(-max_speed, min(self.vel_x, max_speed))
        
        # Actualizar posición
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Limitar al área de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.vel_x = 0
            
        # Resetear si cae fuera de la pantalla
        if self.rect.top > SCREEN_HEIGHT:
            self.take_damage()

    def take_damage(self):
        """Recibir daño"""
        if self.hurt_timer == 0 and not self.powerups['invincibility']['active']:
            self.lives -= 1
            self.hurt_timer = 60  # 1 segundo de invencibilidad
            self.vel_y = -10  # Retroceso
            print(f"💔 Daño recibido! Vidas: {self.lives}")
            
            if self.lives <= 0:
                self.respawn()

    def respawn(self):
        """Reaparecer después de morir"""
        self.rect.x = 100
        self.rect.y = 300
        self.vel_x = 0
        self.vel_y = 0
        self.lives = 3
        self.coins = 0
        # Desactivar todos los power-ups al respawn
        for powerup_type in self.powerups:
            self.powerups[powerup_type]['active'] = False
        print("🔄 Respawn del jugador")

    def add_coin(self):
        """Agregar moneda"""
        self.coins += 1
        self.score += 100
        print(f"💰 Moneda obtenida! Total: {self.coins}")

    def add_score(self, points):
        """Agregar puntos al score"""
        self.score += points

    def draw_health_bar(self, surface):
        """Dibujar barra de vida"""
        bar_width = 100
        bar_height = 10
        x = 10
        y = 10
        
        # Fondo de la barra
        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))
        
        # Vida actual
        health_width = (self.lives / 3) * bar_width
        pygame.draw.rect(surface, (0, 255, 0), (x, y, health_width, bar_height))
        
        # Borde
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 2)

    def draw_powerup_indicators(self, surface):
        """Dibujar indicadores de power-ups activos"""
        x = 10
        y = 30
        icon_size = 20
        
        powerup_icons = {
            'invincibility': '🛡️',
            'jump_boost': '👟', 
            'magnet': '🧲',
            'speed_boost': '⚡'
        }
        
        for i, (powerup_type, data) in enumerate(self.powerups.items()):
            if data['active']:
                # Dibujar icono
                font = pygame.font.Font(None, 24)
                text = font.render(powerup_icons[powerup_type], True, (255, 255, 255))
                surface.blit(text, (x, y + i * 25))
                
                # Dibujar barra de tiempo
                time_left = self.get_powerup_time_left(powerup_type)
                max_time = data['duration'] / 1000
                bar_width = 60
                bar_height = 5
                time_width = (time_left / max_time) * bar_width
                
                pygame.draw.rect(surface, (100, 100, 100), (x + 25, y + 15 + i * 25, bar_width, bar_height))
                pygame.draw.rect(surface, (255, 255, 0), (x + 25, y + 15 + i * 25, time_width, bar_height))

    def get_attack_hitbox(self):
        """Obtener el área de ataque del jugador"""
        direction = 1 if self.facing_right else -1
        attack_width = 30
        attack_height = 20
        
        if self.facing_right:
            attack_rect = pygame.Rect(
                self.rect.right,
                self.rect.centery - attack_height // 2,
                attack_width,
                attack_height
            )
        else:
            attack_rect = pygame.Rect(
                self.rect.left - attack_width,
                self.rect.centery - attack_height // 2,
                attack_width,
                attack_height
            )
        
        return attack_rect