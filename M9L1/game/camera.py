class Camera:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.x = 0
        self.y = 0

    def update(self, target_pos, world_width_px, world_height_px):
        target_x, target_y = target_pos
        max_x = max(0, world_width_px - self.width)
        max_y = max(0, world_height_px - self.height)

        self.x = max(0, min(target_x - self.width // 2, max_x))
        self.y = max(0, min(target_y - self.height // 2, max_y))

    def apply(self, pos):
        x, y = pos
        return x - self.x, y - self.y
