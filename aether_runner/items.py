# items.py - SISTEMA SIMPLIFICADO Y ROBUSTO
import pygame
import math
import random
from config import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        self.config = ITEM_TYPES[item_type]
        
        # Crear superficie
        self.image = pygame.Surface(self.config['size'], pygame.SRCALPHA)
        self.create_sprite()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Animación simple
        self.float_offset = 0

    def create_sprite(self):
        """Crear sprite básico del item"""
        size = self.config['size']
        color = self.config['color']
        
        if self.item_type == 'FRAGMENT':
            # Cristal azul simple
            pygame.draw.circle(self.image, color, (size[0]//2, size[1]//2), size[0]//2)
            pygame.draw.circle(self.image, (255, 255, 255), (size[0]//2, size[1]//2), size[0]//4)
        else:
            # Power-ups como círculos de colores
            pygame.draw.circle(self.image, color, (size[0]//2, size[1]//2), size[0]//2)
        
    def update(self):
        # Animación simple de flotación
        self.float_offset = math.sin(pygame.time.get_ticks() * 0.005) * 3
        self.rect.y += int(self.float_offset) - int(self.float_offset)

class ItemManager:
    def __init__(self):
        self.items = pygame.sprite.Group()
        
    def spawn_item(self, x, y, item_type='FRAGMENT'):
        """Crear item de forma robusta"""
        try:
            item = Item(x, y, item_type)
            self.items.add(item)
            return item
        except:
            return None
        
    def check_collisions(self, player):
        """Verificar colisiones de forma simple"""
        hits = pygame.sprite.spritecollide(player, self.items, True)
        
        for item in hits:
            if item.item_type == 'FRAGMENT':
                player.score += item.config['points']
            elif item.item_type == 'INVINCIBILITY':
                player.activate_powerup('invincibility', item.config['duration'])
            elif item.item_type == 'JUMP_BOOST':
                player.activate_powerup('jump_boost', item.config['duration'])
            elif item.item_type == 'MAGNET':
                player.activate_powerup('magnet', item.config['duration'])
                
        return len(hits)
    
    def update_particles(self, screen):
        """Partículas simples"""
        pass
    
    def update(self):
        self.items.update()
    
    def draw(self, screen):
        self.items.draw(screen)
        
    def get_fragment_count(self):
        return sum(1 for item in self.items if item.item_type == 'FRAGMENT')