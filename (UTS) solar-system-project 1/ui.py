# ui.py
import pygame

class Button:
    def __init__(self, x, y, width, height, text, color=(60, 60, 80), hover_color=(90, 90, 110)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_active = False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        if self.is_active:
            color = (120, 120, 180)
        
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (180, 180, 200), self.rect, 2, border_radius=8)
        
        try:
            font = pygame.font.Font(None, 22)
            text_surf = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
        except:
            pass
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

class UI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Buttons
        button_width = 140
        button_height = 35
        start_x = width - button_width - 30
        
        self.buttons = [
            Button(start_x, 30, button_width, button_height, "⏸️ Pause"),
            Button(start_x, 75, button_width, button_height, "↺ Reset All"),
            Button(start_x, 120, button_width, button_height, "📐 Translasi"),
            Button(start_x, 165, button_width, button_height, "⚖️ Skala"),
            Button(start_x, 210, button_width//2 - 5, button_height, "➕ Speed"),
            Button(start_x + button_width//2 + 5, 210, button_width//2 - 5, button_height, "➖ Speed"),
            Button(start_x, 255, button_width, button_height, "🔄 Toggle Grid"),
            Button(start_x, 300, button_width, button_height, "🎯 Toggle Orbit")
        ]
        
        self.paused = False
        self.speed_multiplier = 1.0
        self.translation_mode = True  # Default aktif
        self.scale_mode = True  # Default aktif
    
    def draw(self, surface, tx, ty, scale):
        # Panel background dengan transparansi
        panel = pygame.Surface((180, self.height), pygame.SRCALPHA)
        panel.fill((20, 20, 40, 220))
        surface.blit(panel, (self.width - 180, 0))
        
        # Update button states
        self.buttons[0].text = "▶️ Resume" if self.paused else "⏸️ Pause"
        self.buttons[2].is_active = self.translation_mode
        self.buttons[3].is_active = self.scale_mode
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
        
        # Draw info panel
        try:
            font = pygame.font.Font(None, 24)
            small_font = pygame.font.Font(None, 18)
            
            info_x = self.width - 170
            info = [
                "STATUS SISTEM:",
                f"Translasi: ({tx:.0f}, {ty:.0f})",
                f"Skala: {scale:.2f}x",
                f"Kecepatan: {self.speed_multiplier:.1f}x",
                f"Status: {'PAUSED' if self.paused else 'RUNNING'}",
                "",
                "MODE AKTIF:",
                f"{'✓' if self.translation_mode else '✗'} Translasi",
                f"{'✓' if self.scale_mode else '✗'} Skala"
            ]
            
            for i, text in enumerate(info):
                if "STATUS" in text or "MODE" in text:
                    color = (255, 220, 100)
                    text_surf = font.render(text, True, color)
                elif "PAUSED" in text:
                    color = (255, 100, 100)
                    text_surf = small_font.render(text, True, color)
                elif "RUNNING" in text:
                    color = (100, 255, 100)
                    text_surf = small_font.render(text, True, color)
                elif "✓" in text:
                    color = (100, 255, 100)
                    text_surf = small_font.render(text, True, color)
                elif "✗" in text:
                    color = (255, 100, 100)
                    text_surf = small_font.render(text, True, color)
                else:
                    color = (200, 200, 220)
                    text_surf = small_font.render(text, True, color)
                
                surface.blit(text_surf, (info_x, 350 + i * 24))
        except:
            pass
    
    def update(self, mouse_pos):
        for button in self.buttons:
            button.check_hover(mouse_pos)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            for i, button in enumerate(self.buttons):
                if button.rect.collidepoint(mouse_pos):
                    self.handle_button_click(i)
                    break
    
    def handle_button_click(self, button_index):
        if button_index == 0:  # Pause/Resume
            self.paused = not self.paused
        elif button_index == 1:  # Reset All
            # Akan dihandle di main.py
            pass
        elif button_index == 2:  # Translasi
            self.translation_mode = not self.translation_mode
        elif button_index == 3:  # Skala
            self.scale_mode = not self.scale_mode
        elif button_index == 4:  # Speed +
            self.speed_multiplier = min(5.0, self.speed_multiplier + 0.5)
        elif button_index == 5:  # Speed -
            self.speed_multiplier = max(0.1, self.speed_multiplier - 0.5)
        elif button_index == 6:  # Toggle Grid
            # Akan dihandle di main.py
            pass
        elif button_index == 7:  # Toggle Orbit
            # Akan dihandle di main.py
            pass
    
    def reset_modes(self):
        """Reset mode ke default"""
        self.translation_mode = True
        self.scale_mode = True
        self.speed_multiplier = 1.0