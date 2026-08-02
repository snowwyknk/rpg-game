import pygame
from game.config import COLORS

def draw_text(surface, text, x, y, size, color, center=False):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(text_surface, rect)

def draw_menu(surface, title, options, selected_index):
    width = surface.get_width()
    height = surface.get_height()
    # Исправлено: COLORS["text"] без пробелов
    draw_text(surface, title, width // 2, height // 4, 48, COLORS["text"], center=True)
    for index, option in enumerate(options):
        prefix = "> " if index == selected_index else "  "
        color = COLORS["text"] if index == selected_index else (160, 160, 160)
        draw_text(surface, prefix + option, width // 2, height // 3 + index * 50, 32, color, center=True)
        

def draw_settings(surface, title, options, values, selected_index):
    width = surface.get_width()
    height = surface.get_height()
    # Исправлено: убраны пробелы в ключах
    draw_text(surface, title, width // 2, height // 5, 44, COLORS["text"], center=True)
    for index, option in enumerate(options):
        display_value = values.get(option, " ")
        text = f"{option}: {display_value}"
        prefix = " > " if index == selected_index else "   "
        color = COLORS["text"] if index == selected_index else (180, 180, 180)
        draw_text(surface, prefix + text, width // 2, height // 3 + index * 50, 28, color, center=True)
    draw_text(surface, "Press Enter to toggle, Esc to return", width // 2, height - 80, 20, (200, 200, 200), center=True)
    
def draw_hud(surface, player):
    font = pygame.font.Font(None, 24)
    hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, (255, 50, 50))
    armor_text = font.render(f"Armor: {player.armor}", True, (100, 100, 255))
    dmg_text = font.render(f"Dmg: {player.damage}", True, (255, 255, 50))
    
    surface.blit(hp_text, (10, 10))
    surface.blit(armor_text, (10, 35))
    surface.blit(dmg_text, (10, 60))
    
    if player.has_key:
        key_text = font.render("Key: YES", True, (255, 215, 0))
        surface.blit(key_text, (10, 85))