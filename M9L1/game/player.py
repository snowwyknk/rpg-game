import math
import os
import pygame
from game.config import PLAYER_WALK_SPEED, PLAYER_RUN_SPEED, PLAYER_ANIMATION_TIME, TILE_SIZE

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walk_speed = PLAYER_WALK_SPEED
        self.run_speed = PLAYER_RUN_SPEED
        self.current_speed = self.walk_speed
        
        # Stats & Inventory
        self.max_hp = 100
        self.hp = 100
        self.armor = 0
        self.damage = 10
        self.inventory = []
        self.has_key = False

        self.animations = self._load_animation_frames()
        self.state = "idle"
        self.direction = "right"
        self.frame_index = 0
        self.frame_timer = 0.0
        self.frame_duration = PLAYER_ANIMATION_TIME
        
        # Безопасная инициализация изображения
        if self.animations["idle"]:
            self.image = self.animations[self.state][self.frame_index]
            self.width, self.height = self.image.get_size()
        else:
            # Fallback если картинки нет
            self.width, self.height = 24, 24
            self.image = None 

        self.bob_timer = 0.0
        self.bob_offset = 0

    def _load_animation_frames(self):
        base_dir = os.path.dirname(__file__)
        asset_dir = os.path.normpath(os.path.join(base_dir, os.pardir))
        frames = {"idle": [], "walk": [], "run": []}
        
        try:
            for filename in sorted(os.listdir(asset_dir)):
                name = filename.lower()
                if not name.endswith((".png", ".jpg", ".bmp")): continue
                if "hero_idle" in name: frames["idle"].append(filename)
                elif "hero_walk" in name: frames["walk"].append(filename)
                elif "hero_run" in name: frames["run"].append(filename)
                elif name == "hero.png": frames["idle"].append(filename)
        except FileNotFoundError: pass

        if not frames["idle"]: frames["idle"] = ["hero.png"] if os.path.exists(os.path.join(asset_dir, "hero.png")) else []
        if not frames["walk"]: frames["walk"] = frames["idle"]
        if not frames["run"]: frames["run"] = frames["walk"]

        loaded_frames = {"idle": [], "walk": [], "run": []}
        for key in frames:
            for filename in frames[key]:
                path = os.path.join(asset_dir, filename)
                try:
                    image = pygame.image.load(path).convert_alpha()
                    loaded_frames[key].append(image)
                except: continue
            if not loaded_frames[key] and key != "idle": loaded_frames[key] = loaded_frames["idle"]
        return loaded_frames

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def check_collision(self, dx, dy, world):
        new_rect = self.get_rect()
        new_rect.x += dx
        new_rect.y += dy
        
        corners = [
            (new_rect.left, new_rect.top),
            (new_rect.right, new_rect.top),
            (new_rect.left, new_rect.bottom),
            (new_rect.right, new_rect.bottom)
        ]
        
        for cx, cy in corners:
            tx, ty = int(cx // TILE_SIZE), int(cy // TILE_SIZE)
            if tx < 0 or tx >= world.width or ty < 0 or ty >= world.height: return True
            if world.tiles[ty][tx] == 1: return True
        return False

    def _update_animation(self, dt, dx, dy, running):
        moving = dx != 0 or dy != 0
        new_state = "run" if (moving and running) else "walk" if moving else "idle"
        
        if new_state != self.state:
            self.state = new_state
            self.frame_index = 0
            self.frame_timer = 0.0
            self.bob_timer = 0.0
            self.bob_offset = 0

        current_frames = self.animations.get(self.state, [])
        if len(current_frames) > 1:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_duration:
                self.frame_timer -= self.frame_duration
                self.frame_index = (self.frame_index + 1) % len(current_frames)
            self.image = current_frames[self.frame_index]
        elif current_frames:
            self.image = current_frames[0]
        else:
            self.image = None

        if self.state != "idle":
            speed = 5.5 if self.state == "run" else 3.5
            self.bob_timer += dt * speed
            self.bob_offset = int(math.sin(self.bob_timer * 2.0) * (3 if self.state == "walk" else 5))
        else:
            self.bob_offset = 0

    def update(self, dt, keys, world, interactables=None):
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_s]: dy += 1
        if keys[pygame.K_a]: 
            dx -= 1
            self.direction = "left"
        if keys[pygame.K_d]: 
            dx += 1
            self.direction = "right"

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        running = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        self.current_speed = self.run_speed if running and (dx != 0 or dy != 0) else self.walk_speed
        
        self._update_animation(dt, dx, dy, running)

        # Движение с коллизиями по осям отдельно
        if dx != 0:
            move_x = dx * self.current_speed * dt
            if not self.check_collision(move_x, 0, world):
                self.x += move_x
        
        if dy != 0:
            move_y = dy * self.current_speed * dt
            if not self.check_collision(0, move_y, world):
                self.y += move_y

        if interactables and keys[pygame.K_e]:
            self.handle_interaction(interactables)

    def handle_interaction(self, interactables):
        player_rect = self.get_rect().inflate(40, 40)
        for obj in interactables:
            if player_rect.colliderect(obj.get_rect()):
                obj.interact(self)

    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply((self.x, self.y))
        
        if self.image:
            surface = self.image
            if self.direction == "left":
                surface = pygame.transform.flip(self.image, True, False)
            screen.blit(surface, (screen_x, screen_y + self.bob_offset))
        else:
            # Рисуем квадрат если нет картинки
            pygame.draw.rect(screen, (0, 200, 100), (screen_x, screen_y + self.bob_offset, self.width, self.height))

    def add_item(self, name, stats=None):
        self.inventory.append({"name": name, "stats": stats})
        print(f"Получено: {name}")
        if stats:
            if "hp" in stats: self.max_hp += stats["hp"]
            if "armor" in stats: self.armor += stats["armor"]
            if "damage" in stats: self.damage += stats["damage"]