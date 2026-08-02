import pygame
from game.camera import Camera
from game.config import WIDTH, HEIGHT, FPS, COLORS, KEY_BINDINGS
from game.player import Player
from game.ui import draw_menu, draw_settings
from game.world import World
from game.entities import Chest, NPC

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Adventure Prototype")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        self.menu_index = 0
        self.settings_index = 0
        self.settings_values = {"Fullscreen": False, "Volume": 75, "Difficulty": "Normal"}
        self.menu_options = ["Start Game", "Settings", "Quit"]
        self.settings_options = ["Fullscreen", "Volume", "Difficulty"]
        
        self.world = World()
        self.player = Player(200, 200)
        self.camera = Camera(WIDTH, HEIGHT)
        
        # Добавляем Джексона и Сундук
        self.interactables = [
            NPC(10, 10, "Джексон"),
            Chest(15, 15)
        ]

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if self.state == "menu": self._handle_menu_input(event)
                elif self.state == "settings": self._handle_settings_input(event)
                elif self.state == "playing" and event.key == KEY_BINDINGS["menu"]: self.state = "menu"

    def _handle_menu_input(self, event):
        if event.key == pygame.K_UP: self.menu_index = max(0, self.menu_index - 1)
        elif event.key == pygame.K_DOWN: self.menu_index = min(len(self.menu_options) - 1, self.menu_index + 1)
        elif event.key == KEY_BINDINGS["confirm"]:
            sel = self.menu_options[self.menu_index]
            if sel == "Start Game": self.state = "playing"
            elif sel == "Settings": self.state = "settings"
            elif sel == "Quit": self.running = False

    def _handle_settings_input(self, event):
        if event.key == pygame.K_UP: self.settings_index = max(0, self.settings_index - 1)
        elif event.key == pygame.K_DOWN: self.settings_index = min(len(self.settings_options) - 1, self.settings_index + 1)
        elif event.key == KEY_BINDINGS["confirm"]:
            opt = self.settings_options[self.settings_index]
            if opt == "Fullscreen": self.settings_values[opt] = not self.settings_values[opt]
            elif opt == "Volume": self.settings_values[opt] = min(100, self.settings_values[opt] + 5)
            elif opt == "Difficulty": self.settings_values[opt] = "Hard" if self.settings_values[opt] == "Normal" else "Normal"
        elif event.key == KEY_BINDINGS["back"]: self.state = "menu"

    def update(self, dt):
        if self.state != "playing": return
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.world, self.interactables)
        self.camera.update((self.player.x, self.player.y), self.world.pixel_width, self.world.pixel_height)

    def draw(self):
        if self.state == "playing":
            self.screen.fill(COLORS["bg"])
            self.world.draw(self.screen, self.camera)
            for obj in self.interactables:
                if hasattr(obj, 'draw'): obj.draw(self.screen, self.camera)
            self.player.draw(self.screen, self.camera)
            
            # Простой HUD
            font = pygame.font.Font(None, 24)
            hp_txt = font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, (255, 50, 50))
            self.screen.blit(hp_txt, (10, 10))
            if self.player.has_key:
                key_txt = font.render("Key: YES", True, (255, 215, 0))
                self.screen.blit(key_txt, (10, 35))
                
        elif self.state == "menu":
            self.screen.fill((10, 10, 18))
            draw_menu(self.screen, "Main Menu", self.menu_options, self.menu_index)
        elif self.state == "settings":
            self.screen.fill((10, 10, 18))
            draw_settings(self.screen, "Settings", self.settings_options, self.settings_values, self.settings_index)
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()