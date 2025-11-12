# enemies.py - ENEMIGOS CORREGIDOS (con colisiones)
import pygame
import math
import random
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        
        # Crear sprite VISIBLE
        self.image = self.create_enemy_sprite(enemy_type)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movimiento
        self.vel_x = 0
        self.vel_y = 0
        self.speed = ENEMY_SPEED
        
        # Estados
        self.direction = 1
        self.move_timer = 0
        self.health = 3 if enemy_type == 'SHOOTER' else 1
        self.on_ground = False  # ✅ NUEVO: Para colisiones
        
        # IA específica
        if enemy_type == 'FLOATER':
            self.wave_offset = random.uniform(0, 2 * math.pi)
            self.amplitude = 2
            self.frequency = 0.02
            
        elif enemy_type == 'SHOOTER':
            self.shoot_timer = 0
            self.shoot_interval = 2000  # 2 segundos
            self.projectiles = pygame.sprite.Group()
            
    def create_enemy_sprite(self, enemy_type):
        """Crear sprites VISIBLES para enemigos"""
        if enemy_type == 'FLOATER':
            # 👻 Sombra flotante - MORADO GRANDE Y VISIBLE
            surface = pygame.Surface((35, 35), pygame.SRCALPHA)
            pygame.draw.circle(surface, ENEMY_COLOR_FLOATER, (17, 17), 17)
            pygame.draw.circle(surface, (220, 150, 255), (17, 17), 12)
            pygame.draw.circle(surface, (255, 255, 255), (12, 12), 5)
            pygame.draw.circle(surface, (255, 255, 255), (22, 12), 5)
            pygame.draw.circle(surface, (100, 50, 200), (12, 12), 2)
            pygame.draw.circle(surface, (100, 50, 200), (22, 12), 2)
            
        elif enemy_type == 'SHOOTER':
            # 🔫 Guardián tirador - ROJO GRANDE Y VISIBLE
            surface = pygame.Surface((40, 50), pygame.SRCALPHA)
            pygame.draw.rect(surface, ENEMY_COLOR_SHOOTER, (0, 0, 40, 50), border_radius=10)
            pygame.draw.rect(surface, (255, 100, 100), (5, 5, 30, 20), border_radius=5)
            pygame.draw.circle(surface, (255, 255, 255), (15, 15), 6)
            pygame.draw.circle(surface, (255, 255, 255), (25, 15), 6)
            pygame.draw.circle(surface, (50, 0, 0), (15, 15), 3)
            pygame.draw.circle(surface, (50, 0, 0), (25, 15), 3)
            pygame.draw.rect(surface, (100, 100, 100), (18, 40, 4, 10))
        
        return surface
    
    def update(self, player=None):
        """Actualizar según tipo de enemigo"""
        if self.enemy_type == 'FLOATER':
            self.update_floater()
        elif self.enemy_type == 'SHOOTER':
            self.update_shooter(player)
            
        # ✅ CORREGIDO: Solo aplicar gravedad si no está en el suelo
        if not self.on_ground:
            self.vel_y += PLAYER_GRAVITY * 0.3
        else:
            self.vel_y = 0  # No caer si está en plataforma
            
        self.rect.y += self.vel_y
        self.on_ground = False  # Resetear para siguiente frame
        
    def update_floater(self):
        """IA para sombra flotante"""
        self.move_timer += 1
        
        # Movimiento horizontal suave
        self.rect.x += self.direction * self.speed * 0.7
        
        # Movimiento vertical sinusoidal (más pronunciado)
        wave = math.sin(self.move_timer * self.frequency + self.wave_offset) * self.amplitude
        self.rect.y += wave
        
        # Cambiar dirección cada 3 segundos (180 frames)
        if self.move_timer % 180 == 0:
            self.direction *= -1
            
        # Mantener en pantalla
        if self.rect.left < 50:
            self.direction = 1
        if self.rect.right > SCREEN_WIDTH - 50:
            self.direction = -1
            
    def update_shooter(self, player):
        """IA para guardián tirador"""
        if player:
            self.shoot_timer += 16  # Aprox 1 frame a 60 FPS
            
            # Disparar cada 2 segundos
            if self.shoot_timer >= self.shoot_interval:
                self.shoot_timer = 0
                self.shoot_projectile(player)
                
    def shoot_projectile(self, player):
        """Disparar proyectil hacia el jugador"""
        if player:
            # Calcular dirección
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = max(1, math.sqrt(dx*dx + dy*dy))
            
            # Normalizar
            dx /= distance
            dy /= distance
            
            projectile = Projectile(self.rect.centerx, self.rect.centery, dx, dy)
            self.projectiles.add(projectile)
            return projectile
            
    def draw_projectiles(self, screen):
        """Dibujar proyectiles de este enemigo"""
        self.projectiles.draw(screen)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 50, 50), (6, 6), 6)
        pygame.draw.circle(self.image, (255, 150, 150), (6, 6), 3)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        self.dx = dx * PROJECTILE_SPEED
        self.dy = dy * PROJECTILE_SPEED
        self.lifetime = 180
        
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.lifetime -= 1
        
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.lifetime <= 0):
            self.kill()

class EnemyManager:
    def __init__(self):
        self.enemies = pygame.sprite.Group()
        
    def spawn_enemy(self, x, y, enemy_type='FLOATER'):
        enemy = Enemy(x, y, enemy_type)
        self.enemies.add(enemy)
        return enemy
        
    def update(self, player=None):
        self.enemies.update(player)
        for enemy in self.enemies:
            if hasattr(enemy, 'projectiles'):
                enemy.projectiles.update()
                
    def draw_projectiles(self, screen):
        for enemy in self.enemies:
            if hasattr(enemy, 'projectiles'):
                enemy.draw_projectiles(screen)
                
    def check_projectile_collisions(self, player):
        for enemy in self.enemies:
            if hasattr(enemy, 'projectiles'):
                if pygame.sprite.spritecollide(player, enemy.projectiles, True):
                    return True
        return False
    
    def check_collisions(self, player):
        return pygame.sprite.spritecollide(player, self.enemies, False)