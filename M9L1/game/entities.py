import pygame
import random
from game.config import TILE_SIZE, COLORS

class Interactable:
    def __init__(self, x, y, type_name):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.type = type_name
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.interacted = False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def interact(self, player): pass

class Chest(Interactable):
    def __init__(self, x, y):
        super().__init__(x, y, "chest")
        self.color = COLORS.get("chest", (200, 150, 50))

    def interact(self, player):
        if self.interacted:
            print("Сундук пуст.")
            return
        if not player.has_key:
            print("Нужен ключ!")
            return
        
        self.interacted = True
        roll = random.random() * 100
        
        if roll < 50:
            player.add_item("Еда", {"hp": 20})
        elif roll < 65:
            player.add_item("Шлем", {"armor": 1})
        elif roll < 70:
            player.add_item("Меч Героя", {"damage": 15})
        else:
            player.add_item("Кольцо Жизни", {"hp": 50})

class NPC(Interactable):
    def __init__(self, x, y, name="NPC"):
        super().__init__(x, y, "npc")
        self.name = name
        self.color = COLORS.get("npc", (200, 200, 0))

    def interact(self, player):
        if self.name == "Джексон":
            if not player.has_key:
                print(f"{self.name}: 'Вот ключ от сундука!'")
                player.has_key = True
            else:
                print(f"{self.name}: 'Удачи!'")
        else:
            print(f"{self.name}: 'Привет!'")

    def draw(self, screen, camera):
        sx, sy = camera.apply((self.x, self.y))
        pygame.draw.rect(screen, self.color, (sx, sy, self.width, self.height))
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (sx - 10, sy - 20))