import pygame
from game.config import COLORS, TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT

class World:
    def __init__(self, width=WORLD_WIDTH, height=WORLD_HEIGHT):
        self.width = width
        self.height = height
        self.tiles = []
        self._generate_default_world()

    def _generate_default_world(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Границы
                if x in (0, self.width - 1) or y in (0, self.height - 1):
                    row.append(1)
                # Случайные препятствия
                elif x % 7 == 0 and y % 3 != 0 and 2 < x < self.width - 3:
                    row.append(1)
                elif y % 6 == 0 and x % 4 != 0 and 2 < y < self.height - 3:
                    row.append(1)
                else:
                    row.append(0)
            self.tiles.append(row)

    def draw(self, screen, camera):
        # Оптимизация: рисуем только тайлы в поле зрения камеры
        start_col = max(0, int(camera.x // TILE_SIZE))
        end_col = min(self.width, int((camera.x + camera.width) // TILE_SIZE) + 1)
        start_row = max(0, int(camera.y // TILE_SIZE))
        end_row = min(self.height, int((camera.y + camera.height) // TILE_SIZE) + 1)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                tile = self.tiles[y][x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                screen_x, screen_y = camera.apply((rect.x, rect.y))
                draw_rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
                
                color = COLORS["wall"] if tile else COLORS["floor"]
                pygame.draw.rect(screen, color, draw_rect)
                # Легкая обводка для сетки
                pygame.draw.rect(screen, (30, 30, 36), draw_rect, 1)

    @property
    def pixel_width(self):
        return self.width * TILE_SIZE
    @property
    def pixel_height(self):
        return self.height * TILE_SIZE