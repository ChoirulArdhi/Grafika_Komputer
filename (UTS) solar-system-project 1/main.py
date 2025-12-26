import pygame
import math
import random
import os
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60

# Colors for planets (if images not found)
SUN_COLOR = (255, 223, 0)
MERCURY_COLOR = (169, 169, 169)
VENUS_COLOR = (255, 165, 0)
EARTH_COLOR = (100, 149, 237)
MARS_COLOR = (188, 39, 50)
JUPITER_COLOR = (218, 165, 32)
SATURN_COLOR = (244, 214, 49)
URANUS_COLOR = (173, 216, 230)
NEPTUNE_COLOR = (65, 105, 225)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SISTEM TATA SURYA 2D - UTS GRAFIKA KOMPUTER")
clock = pygame.time.Clock()

# ==================== ALGORITMA MANUAL ====================

def bresenham_line(x1, y1, x2, y2):
    """Bresenham Line Algorithm"""
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    
    if dx > dy:
        err = dx / 2.0
        while x != x2:
            points.append((int(x), int(y)))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            points.append((int(x), int(y)))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    
    points.append((int(x), int(y)))
    return points

def midpoint_circle(cx, cy, radius, fill=True):
    """Midpoint Circle Algorithm"""
    points = []
    x = radius
    y = 0
    err = 0
    
    while x >= y:
        points.extend([
            (cx + x, cy + y), (cx + y, cy + x), (cx - y, cy + x), (cx - x, cy + y),
            (cx - x, cy - y), (cx - y, cy - x), (cx + y, cy - x), (cx + x, cy - y)
        ])
        
        if fill:
            for px in range(cx - x, cx + x + 1):
                points.append((px, cy + y))
                points.append((px, cy - y))
            for px in range(cx - y, cx + y + 1):
                points.append((px, cy + x))
                points.append((px, cy - x))
        
        y += 1
        err += 1 + 2*y
        if 2*(err - x) + 1 > 0:
            x -= 1
            err += 1 - 2*x
    
    return list(set(points))

def scanline_polygon(polygon_points, color):
    """Scanline Polygon Algorithm"""
    if len(polygon_points) < 3:
        return
    
    # Find y min and max
    y_min = min(p[1] for p in polygon_points)
    y_max = max(p[1] for p in polygon_points)
    
    # Process each scanline
    for y in range(int(y_min), int(y_max) + 1):
        intersections = []
        
        # Find intersections with each edge
        for i in range(len(polygon_points)):
            p1 = polygon_points[i]
            p2 = polygon_points[(i + 1) % len(polygon_points)]
            
            # Skip horizontal edges
            if p1[1] == p2[1]:
                continue
            
            # Ensure p1 is above p2
            if p1[1] > p2[1]:
                p1, p2 = p2, p1
            
            # Check if scanline intersects this edge
            if p1[1] <= y < p2[1]:
                # Calculate intersection x
                x_intersect = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                intersections.append(x_intersect)
        
        # Sort intersections and fill between pairs
        intersections.sort()
        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_start = int(intersections[i])
                x_end = int(intersections[i + 1])
                for x in range(x_start, x_end + 1):
                    pygame.draw.circle(screen, color, (x, y), 1)

class Starfield:
    def __init__(self, num_stars=200):
        self.stars = []
        for _ in range(num_stars):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.uniform(0.1, 1.5)
            speed = random.uniform(0.01, 0.05)
            twinkle_speed = random.uniform(0.01, 0.03)
            self.stars.append([x, y, size, speed, twinkle_speed, 1.0, 0])
    
    def update(self):
        for star in self.stars:
            # Twinkle effect
            star[5] = 0.5 + 0.5 * math.sin(star[6])
            star[6] += star[4]
    
    def draw(self, offset_x=0, offset_y=0):
        for x, y, size, speed, _, alpha, _ in self.stars:
            # Apply parallax based on offset
            parallax_x = x + offset_x * speed * 0.5
            parallax_y = y + offset_y * speed * 0.5
            
            # Wrap around screen
            parallax_x %= WIDTH
            parallax_y %= HEIGHT
            
            # Draw star with alpha
            color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
            if size < 0.5:
                screen.set_at((int(parallax_x), int(parallax_y)), color)
            else:
                pygame.draw.circle(screen, color, (int(parallax_x), int(parallax_y)), int(size))

class CelestialBody:
    def __init__(self, name, radius, color, orbit_radius, orbit_speed, rotation_speed=1.0, image_name=None):
        self.name = name
        self.radius = radius
        self.color = color
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.rotation_speed = rotation_speed
        self.orbit_angle = random.uniform(0, 2 * math.pi)
        self.rotation_angle = random.uniform(0, 2 * math.pi)
        self.trail = []
        self.max_trail_length = 100
        self.selected = False
        self.image_name = image_name
        self.image = None
        self.texture = None
        self.load_image()
        self.create_texture()
        
        # For rotation visualization
        self.rotation_markers = []
        self.create_rotation_markers()
    
    def load_image(self):
        """Load planet image from assets folder"""
        if self.image_name:
            asset_path = f"assets/{self.image_name}"
            if os.path.exists(asset_path):
                try:
                    original_image = pygame.image.load(asset_path).convert_alpha()
                    # Scale image to appropriate size
                    scaled_size = int(self.radius * 4)  # Larger for better quality
                    self.image = pygame.transform.smoothscale(original_image, (scaled_size, scaled_size))
                except:
                    self.image = None
                    print(f"Gambar {asset_path} tidak bisa dimuat, menggunakan warna default")
    
    def create_texture(self):
        """Create a textured surface for rotation visualization"""
        size = int(self.radius * 2 * 2)  # Double size for rotation
        self.texture = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Create a pattern based on planet color
        base_color = self.color
        darker_color = tuple(max(0, c - 40) for c in base_color)
        lighter_color = tuple(min(255, c + 40) for c in base_color)
        
        # Draw concentric circles for texture
        for i in range(5):
            radius_ratio = 1.0 - (i * 0.15)
            color_ratio = i / 4.0
            current_color = (
                int(base_color[0] * (1 - color_ratio) + lighter_color[0] * color_ratio),
                int(base_color[1] * (1 - color_ratio) + lighter_color[1] * color_ratio),
                int(base_color[2] * (1 - color_ratio) + lighter_color[2] * color_ratio)
            )
            
            # Use midpoint_circle algorithm to draw textured circles
            points = midpoint_circle(size // 2, size // 2, int(self.radius * radius_ratio))
            for px, py in points:
                if 0 <= px < size and 0 <= py < size:
                    # Add some variation
                    if random.random() > 0.7:
                        self.texture.set_at((px, py), current_color)
        
        # Add rotation indicator lines
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x1 = size // 2 + int((self.radius * 0.7) * math.cos(rad))
            y1 = size // 2 + int((self.radius * 0.7) * math.sin(rad))
            x2 = size // 2 + int(self.radius * math.cos(rad))
            y2 = size // 2 + int(self.radius * math.sin(rad))
            
            # Draw faint lines
            for px, py in bresenham_line(x1, y1, x2, y2):
                if 0 <= px < self.texture.get_width() and 0 <= py < self.texture.get_height():
                    current_pixel = self.texture.get_at((px, py))
                    new_color = (
                        min(255, current_pixel[0] + 30),
                        min(255, current_pixel[1] + 30),
                        min(255, current_pixel[2] + 30),
                        255
                    )
                    self.texture.set_at((px, py), new_color)
    
    def create_rotation_markers(self):
        """Create markers to visualize rotation"""
        self.rotation_markers = []
        for i in range(8):  # 8 markers around the planet
            angle = (i / 8.0) * 2 * math.pi
            marker_radius = self.radius * 0.8
            self.rotation_markers.append({
                'angle': angle,
                'radius': marker_radius,
                'color': (255, 255, 255, 100) if i % 2 == 0 else (200, 200, 255, 100)
            })
    
    def update(self, dt, time_scale):
        # Orbit position (perfect circle orbit)
        self.orbit_angle += self.orbit_speed * dt * time_scale
        self.orbit_angle %= 2 * math.pi
        
        # Rotation angle
        self.rotation_angle += self.rotation_speed * dt * time_scale * 2.0  # Faster rotation for visibility
        self.rotation_angle %= 2 * math.pi
        
        # Update trail
        x = self.orbit_radius * math.cos(self.orbit_angle)
        y = self.orbit_radius * math.sin(self.orbit_angle)
        self.trail.append((x, y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Update rotation markers
        for marker in self.rotation_markers:
            marker['angle'] += self.rotation_speed * dt * time_scale * 1.5
    
    def get_position(self, camera_x=0, camera_y=0, zoom=1.0):
        x = self.orbit_radius * math.cos(self.orbit_angle)
        y = self.orbit_radius * math.sin(self.orbit_angle)
        screen_x = CENTER_X + (x - camera_x) * zoom
        screen_y = CENTER_Y + (y - camera_y) * zoom
        return screen_x, screen_y
    
    def draw_sun_glow(self, screen_x, screen_y, scaled_radius):
        """Draw sun dengan glow effect untuk menghindari kotak"""
        # Draw multiple layers untuk glow effect
        glow_layers = [
            (scaled_radius * 2.5, (255, 255, 200, 30)),
            (scaled_radius * 2.0, (255, 255, 180, 50)),
            (scaled_radius * 1.5, (255, 255, 150, 80)),
            (scaled_radius, (255, 255, 100, 150)),
            (scaled_radius * 0.7, (255, 255, 50, 200))
        ]
        
        for glow_radius, glow_color in glow_layers:
            if glow_radius >= 1:  # Hanya draw jika radius cukup besar
                # Gunakan algoritma midpoint_circle untuk glow
                points = midpoint_circle(int(screen_x), int(screen_y), int(glow_radius))
                for px, py in points:
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        screen.set_at((px, py), glow_color)
    
    def draw_planet_simple(self, screen_x, screen_y, scaled_radius):
        """Draw planet sederhana untuk zoom kecil"""
        # Gunakan algoritma manual langsung ke screen
        points = midpoint_circle(int(screen_x), int(screen_y), int(scaled_radius))
        for px, py in points:
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                screen.set_at((px, py), self.color)
        
        # Tambahkan highlight kecil
        highlight_x = int(screen_x - scaled_radius * 0.3)
        highlight_y = int(screen_y - scaled_radius * 0.3)
        highlight_points = midpoint_circle(highlight_x, highlight_y, max(1, int(scaled_radius * 0.3)))
        for px, py in highlight_points:
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                screen.set_at((px, py), (255, 255, 255, 150))
    
    def draw_planet_detailed(self, screen_x, screen_y, scaled_radius, zoom):
        """Draw planet dengan detail lengkap"""
        # Create surface for planet with alpha
        surface_size = max(10, int(scaled_radius * 2) + 4)  # Minimal 10x10 pixel
        planet_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        center = surface_size // 2
        
        if self.image and zoom > 0.3:  # Use image for high zoom
            # Rotate the image
            rotated_image = pygame.transform.rotate(self.image, math.degrees(self.rotation_angle))
            img_rect = rotated_image.get_rect(center=(center, center))
            planet_surface.blit(rotated_image, img_rect)
        else:
            # Draw textured planet with manual algorithms
            # Draw main circle
            points = midpoint_circle(center, center, int(scaled_radius))
            for px, py in points:
                # Calculate position in texture
                if self.texture and scaled_radius > 0:
                    tex_x = int((px - center) / scaled_radius * self.radius) % self.texture.get_width()
                    tex_y = int((py - center) / scaled_radius * self.radius) % self.texture.get_height()
                    
                    if 0 <= tex_x < self.texture.get_width() and 0 <= tex_y < self.texture.get_height():
                        tex_color = self.texture.get_at((tex_x, tex_y))
                        # Apply rotation effect
                        angle = math.atan2(py - center, px - center)
                        rotated_angle = angle + self.rotation_angle
                        shade = 0.8 + 0.2 * math.sin(rotated_angle * 2)
                        
                        final_color = (
                            min(255, int(tex_color[0] * shade)),
                            min(255, int(tex_color[1] * shade)),
                            min(255, int(tex_color[2] * shade)),
                            255
                        )
                        planet_surface.set_at((px, py), final_color)
            
            # Draw rotation markers (clearly visible features)
            for marker in self.rotation_markers:
                marker_x = int(center + marker['radius'] * zoom * math.cos(marker['angle']))
                marker_y = int(center + marker['radius'] * zoom * math.sin(marker['angle']))
                
                # Draw a small circle for the marker
                marker_points = midpoint_circle(marker_x, marker_y, max(1, int(scaled_radius * 0.1)))
                for px, py in marker_points:
                    if 0 <= px < planet_surface.get_width() and 0 <= py < planet_surface.get_height():
                        current = planet_surface.get_at((px, py))
                        blended = (
                            (current[0] + marker['color'][0]) // 2,
                            (current[1] + marker['color'][1]) // 2,
                            (current[2] + marker['color'][2]) // 2,
                            255
                        )
                        planet_surface.set_at((px, py), blended)
        
        # Apply REFLECTION: Highlight effect (top-left light source)
        if scaled_radius > 3:  # Only add highlight if planet is large enough
            highlight_radius = max(1, int(scaled_radius * 0.3))
            highlight_x = int(center - scaled_radius * 0.3)
            highlight_y = int(center - scaled_radius * 0.3)
            
            highlight_points = midpoint_circle(highlight_x, highlight_y, highlight_radius)
            for px, py in highlight_points:
                if 0 <= px < planet_surface.get_width() and 0 <= py < planet_surface.get_height():
                    dist = math.sqrt((px - highlight_x)**2 + (py - highlight_y)**2)
                    if dist <= highlight_radius:
                        alpha = int(200 * (1 - dist / highlight_radius))
                        planet_surface.set_at((px, py), (255, 255, 255, alpha))
        
        # Apply REFLECTION: Ground shadow (bottom) - PERBAIKAN: hindari ZeroDivisionError
        if scaled_radius > 4:  # Only add shadow if planet is large enough
            shadow_height = max(1, int(scaled_radius * 0.2))
            for y in range(int(center + scaled_radius * 0.5), int(center + scaled_radius) + 2):
                if y < planet_surface.get_height():
                    # PERBAIKAN: Cegah pembagian dengan 0
                    if shadow_height > 0:
                        alpha = int(100 * (1 - (y - (center + scaled_radius * 0.5)) / shadow_height))
                        if alpha > 0:
                            for x in range(planet_surface.get_width()):
                                # Check if within circle
                                dx = x - center
                                dy = y - center
                                if dx*dx + dy*dy <= scaled_radius*scaled_radius:
                                    current = planet_surface.get_at((x, y))
                                    shadowed = (
                                        max(0, current[0] - 30),
                                        max(0, current[1] - 30),
                                        max(0, current[2] - 30),
                                        current[3]
                                    )
                                    planet_surface.set_at((x, y), shadowed)
        
        # Draw the planet surface to screen
        screen.blit(planet_surface, (screen_x - center, screen_y - center))
    
    def draw(self, camera_x=0, camera_y=0, zoom=1.0, draw_trail=False):
        screen_x, screen_y = self.get_position(camera_x, camera_y, zoom)
        scaled_radius = max(1, self.radius * zoom)  # Minimal radius 1 pixel
        
        # Draw orbit line
        if self.orbit_radius > 0 and zoom > 0.05:
            orbit_points = []
            for angle in range(0, 360, max(1, int(5 / zoom))):  # Kurangi titik saat zoom kecil
                rad = math.radians(angle)
                ox = CENTER_X + (self.orbit_radius * math.cos(rad) - camera_x) * zoom
                oy = CENTER_Y + (self.orbit_radius * math.sin(rad) - camera_y) * zoom
                orbit_points.append((ox, oy))
            
            # Draw orbit using Bresenham lines
            if len(orbit_points) > 1:
                for i in range(len(orbit_points) - 1):
                    for px, py in bresenham_line(
                        int(orbit_points[i][0]), int(orbit_points[i][1]),
                        int(orbit_points[i+1][0]), int(orbit_points[i+1][1])
                    ):
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            alpha = 50
                            color = (100, 100, 150, alpha)
                            screen.set_at((px, py), color)
        
        # Draw trail
        if draw_trail and len(self.trail) > 2 and zoom > 0.1:
            for i in range(len(self.trail) - 1):
                x1 = CENTER_X + (self.trail[i][0] - camera_x) * zoom
                y1 = CENTER_Y + (self.trail[i][1] - camera_y) * zoom
                x2 = CENTER_X + (self.trail[i+1][0] - camera_x) * zoom
                y2 = CENTER_Y + (self.trail[i+1][1] - camera_y) * zoom
                
                # Fade trail based on age
                alpha = int(255 * (i / len(self.trail)))
                color = (*self.color[:3], alpha) if len(self.color) == 4 else (*self.color, alpha)
                
                for px, py in bresenham_line(int(x1), int(y1), int(x2), int(y2)):
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        screen.set_at((px, py), color)
        
        # PERBAIKAN UTAMA: Gambar matahari dan planet dengan cara berbeda
        if scaled_radius > 0.5:  # Only draw if visible
            if self.name == "Matahari":
                # Gambar matahari dengan glow effect
                self.draw_sun_glow(screen_x, screen_y, scaled_radius)
                
                # Gambar inti matahari
                if scaled_radius < 5:
                    # Untuk zoom kecil, gunakan algoritma manual
                    self.draw_planet_simple(screen_x, screen_y, scaled_radius)
                else:
                    # Untuk zoom besar, gunakan surface dengan detail
                    self.draw_planet_detailed(screen_x, screen_y, scaled_radius, zoom)
            
            elif scaled_radius < 3:  # Planet kecil saat zoom out
                self.draw_planet_simple(screen_x, screen_y, scaled_radius)
            
            else:  # Planet normal
                self.draw_planet_detailed(screen_x, screen_y, scaled_radius, zoom)
        
        # Draw selection circle
        if self.selected and scaled_radius > 2:
            selection_radius = scaled_radius + 5
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                px = int(screen_x + selection_radius * math.cos(rad))
                py = int(screen_y + selection_radius * math.sin(rad))
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    screen.set_at((px, py), WHITE)
        
        # Draw planet name
        if zoom > 0.2 and scaled_radius > 3:
            font = pygame.font.SysFont(None, 24)
            text = font.render(self.name, True, WHITE)
            text_width = text.get_width()
            
            # Cari posisi yang tidak overlap dengan UI
            text_x = screen_x - text_width // 2
            text_y = screen_y - scaled_radius - 20
            
            # Jika overlap dengan panel kiri, pindah ke kanan
            if text_x < 320:  # Panel kiri lebar ~300px
                text_x = screen_x + scaled_radius + 10
                text_y = screen_y
            
            # Jika overlap dengan panel kanan, pindah ke kiri
            elif text_x + text_width > WIDTH - 320:
                text_x = screen_x - scaled_radius - text_width - 10
                text_y = screen_y
            
            # Gambar background untuk teks agar terbaca
            pygame.draw.rect(screen, (0, 0, 0, 180), 
                           (text_x - 2, text_y - 2, text_width + 4, 24))
            
            screen.blit(text, (text_x, text_y))

class Comet:
    def __init__(self):
        # Start from random edge
        side = random.choice(['left', 'right', 'top', 'bottom'])
        if side == 'left':
            self.x = -100
            self.y = random.uniform(0, HEIGHT)
            self.vx = random.uniform(1, 3)
            self.vy = random.uniform(-1, 1)
        elif side == 'right':
            self.x = WIDTH + 100
            self.y = random.uniform(0, HEIGHT)
            self.vx = random.uniform(-3, -1)
            self.vy = random.uniform(-1, 1)
        elif side == 'top':
            self.x = random.uniform(0, WIDTH)
            self.y = -100
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(1, 3)
        else:  # bottom
            self.x = random.uniform(0, WIDTH)
            self.y = HEIGHT + 100
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-3, -1)
        
        self.size = random.uniform(2, 5)
        self.rotation = 0
        self.rotation_speed = random.uniform(0.02, 0.05)
        self.trail = []
        self.max_trail_length = 50
        self.color = (200, 230, 255)
    
    def update(self, dt, time_scale):
        # TRANSLATION: Move comet
        self.x += self.vx * dt * time_scale
        self.y += self.vy * dt * time_scale
        
        # ROTATION: Rotate comet
        self.rotation += self.rotation_speed * dt * time_scale
        
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
    
    def draw(self, camera_x=0, camera_y=0, zoom=1.0):
        # Draw trail
        if len(self.trail) > 1:
            for i in range(len(self.trail) - 1):
                x1 = self.trail[i][0]
                y1 = self.trail[i][1]
                x2 = self.trail[i+1][0]
                y2 = self.trail[i+1][1]
                
                alpha = int(255 * (i / len(self.trail)))
                trail_color = (150, 200, 255, alpha)
                
                for px, py in bresenham_line(int(x1), int(y1), int(x2), int(y2)):
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        screen.set_at((px, py), trail_color)
        
        # Draw comet with ROTATION
        screen_x = CENTER_X + (self.x - camera_x - CENTER_X) * zoom
        screen_y = CENTER_Y + (self.y - camera_y - CENTER_Y) * zoom
        scaled_size = max(1, self.size * zoom)
        
        # Create comet shape (triangle)
        comet_points = []
        for i in range(3):
            angle = self.rotation + i * (2 * math.pi / 3)
            px = screen_x + scaled_size * 2 * math.cos(angle)
            py = screen_y + scaled_size * 2 * math.sin(angle)
            comet_points.append((px, py))
        
        # Draw comet using scanline polygon algorithm
        if scaled_size > 0.5:
            scanline_polygon(comet_points, self.color)
        
        # Add highlight (REFLECTION)
        if scaled_size > 1:
            highlight_points = midpoint_circle(
                int(screen_x + scaled_size * 0.5 * math.cos(self.rotation)),
                int(screen_y + scaled_size * 0.5 * math.sin(self.rotation)),
                int(scaled_size * 0.5)
            )
            for px, py in highlight_points:
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    screen.set_at((px, py), (255, 255, 255, 150))

class SaturnRing:
    def __init__(self, planet):
        self.planet = planet
        self.inner_radius = planet.radius * 1.5
        self.outer_radius = planet.radius * 2.5
        self.rotation_angle = 0
        self.rotation_speed = planet.rotation_speed * 0.5
    
    def update(self, dt, time_scale):
        # ROTATION: Ring rotates
        self.rotation_angle += self.rotation_speed * dt * time_scale
    
    def draw(self, camera_x=0, camera_y=0, zoom=1.0):
        planet_x, planet_y = self.planet.get_position(camera_x, camera_y, zoom)
        scaled_inner = max(1, self.inner_radius * zoom)
        scaled_outer = max(2, self.outer_radius * zoom)
        
        # Only draw if ring is visible
        if scaled_outer < 1:
            return
        
        # Create ring as a polygon (ellipse)
        ring_points = []
        num_points = max(20, min(60, int(scaled_outer * 2)))  # Sesuaikan jumlah titik dengan ukuran
        
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi + self.rotation_angle
            # Elliptical ring (slightly flattened)
            radius = scaled_inner + (scaled_outer - scaled_inner) * abs(math.sin(angle * 2))
            x = planet_x + radius * math.cos(angle)
            y = planet_y + radius * math.sin(angle) * 0.3  # Flatten in y-direction
            ring_points.append((x, y))
        
        # Draw ring with gradient colors using scanline algorithm
        if len(ring_points) > 2:
            colors = [
                (210, 180, 140, 200),  # Light brown
                (185, 155, 115, 180),  # Medium brown
                (160, 130, 90, 160),   # Dark brown
                (135, 105, 65, 140)    # Darker brown
            ]
            
            # Draw multiple layers for gradient effect
            for layer in range(min(4, int(scaled_outer))):
                layer_points = []
                layer_offset = layer * 0.1 * zoom
                
                for i in range(len(ring_points)):
                    angle = (i / len(ring_points)) * 2 * math.pi + self.rotation_angle
                    # Calculate normal for offset
                    nx = math.cos(angle)
                    ny = math.sin(angle) * 0.3
                    length = math.sqrt(nx*nx + ny*ny)
                    if length > 0:
                        nx /= length
                        ny /= length
                    
                    x = ring_points[i][0] + nx * layer_offset
                    y = ring_points[i][1] + ny * layer_offset
                    layer_points.append((x, y))
                
                # Draw this layer
                scanline_polygon(layer_points, colors[layer])

class UISystem:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)
        self.small_font = pygame.font.SysFont(None, 20)
        self.title_font = pygame.font.SysFont(None, 32)
        self.panel_width = 300
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width, _ = font.size(test_line)
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def draw_panel_left(self, paused, zoom, time_scale, selected_planet, fps):
        # Draw semi-transparent panel
        panel_surface = pygame.Surface((self.panel_width, HEIGHT), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 200))
        screen.blit(panel_surface, (0, 0))
        
        y_offset = 20
        
        # Title
        title = self.title_font.render("SISTEM TATA SURYA 2D", True, (255, 255, 0))
        screen.blit(title, (20, y_offset))
        y_offset += 50
        
        # Status
        status_color = (0, 255, 0) if not paused else (255, 100, 100)
        status_text = self.font.render(f"Status: {'RUNNING' if not paused else 'PAUSED'}", True, status_color)
        screen.blit(status_text, (20, y_offset))
        y_offset += 40
        
        # Zoom info
        zoom_text = self.font.render(f"Zoom: {zoom:.2f}x", True, WHITE)
        screen.blit(zoom_text, (20, y_offset))
        y_offset += 30
        
        # Time scale
        time_text = self.font.render(f"Time Scale: {time_scale:.1f}x", True, WHITE)
        screen.blit(time_text, (20, y_offset))
        y_offset += 30
        
        # FPS
        fps_text = self.font.render(f"FPS: {fps:.1f}", True, WHITE)
        screen.blit(fps_text, (20, y_offset))
        y_offset += 40
        
        # Separator line
        pygame.draw.line(screen, (100, 100, 100), (20, y_offset), (self.panel_width - 20, y_offset), 2)
        y_offset += 20
        
        # Selected planet info
        if selected_planet:
            # Background for planet info
            pygame.draw.rect(screen, (30, 30, 60), (10, y_offset, self.panel_width - 20, 120), border_radius=5)
            pygame.draw.rect(screen, (60, 60, 100), (10, y_offset, self.panel_width - 20, 120), 2, border_radius=5)
            
            planet_text = self.font.render(f"Planet: {selected_planet.name}", True, selected_planet.color)
            screen.blit(planet_text, (20, y_offset + 10))
            
            radius_text = self.small_font.render(f"Radius: {selected_planet.radius:.1f}", True, WHITE)
            screen.blit(radius_text, (20, y_offset + 40))
            
            orbit_text = self.small_font.render(f"Orbit Radius: {selected_planet.orbit_radius:.0f}", True, WHITE)
            screen.blit(orbit_text, (20, y_offset + 60))
            
            speed_text = self.small_font.render(f"Speed: {selected_planet.orbit_speed:.3f}", True, WHITE)
            screen.blit(speed_text, (20, y_offset + 80))
            
            y_offset += 130
        
        # Separator line
        pygame.draw.line(screen, (100, 100, 100), (20, y_offset), (self.panel_width - 20, y_offset), 2)
        y_offset += 20
        
        # Transformations section
        trans_title = self.font.render("TRANSFORMASI GEOMETRI:", True, (100, 255, 255))
        screen.blit(trans_title, (20, y_offset))
        y_offset += 30
        
        transformations = [
            ("1. TRANSLASI", "Orbit planet & pergerakan kamera"),
            ("2. ROTASI", "Planet berputar pada porosnya"),
            ("3. SKALA", "Zoom sistem (0.1x - 3.0x)"),
            ("4. REFLEKSI", "Highlight & ground shadow")
        ]
        
        for i, (title, desc) in enumerate(transformations):
            title_text = self.small_font.render(title, True, (200, 200, 100))
            screen.blit(title_text, (30, y_offset))
            y_offset += 25
            
            desc_lines = self.wrap_text(desc, self.small_font, self.panel_width - 50)
            for line in desc_lines:
                desc_text = self.small_font.render(line, True, (200, 200, 200))
                screen.blit(desc_text, (40, y_offset))
                y_offset += 22
            y_offset += 5
        
        # Separator line
        pygame.draw.line(screen, (100, 100, 100), (20, y_offset), (self.panel_width - 20, y_offset), 2)
        y_offset += 20
        
        # Algorithms section
        algo_title = self.font.render("ALGORITMA MANUAL:", True, (255, 100, 255))
        screen.blit(algo_title, (20, y_offset))
        y_offset += 30
        
        algorithms = [
            "• Bresenham Line (orbit & trails)",
            "• Midpoint Circle (planet & bintang)",
            "• Scanline Polygon (cincin & komet)",
            "• Transformasi 2D Manual"
        ]
        
        for algo in algorithms:
            algo_text = self.small_font.render(algo, True, (200, 200, 255))
            screen.blit(algo_text, (30, y_offset))
            y_offset += 25
        
        # Separator line
        if y_offset < HEIGHT - 280:
            pygame.draw.line(screen, (100, 100, 100), (20, y_offset), (self.panel_width - 20, y_offset), 2)
            y_offset += 20
    
    def draw_panel_right(self, show_trails, show_orbits, asteroid_belt_visible, num_comets):
        # Draw semi-transparent panel di kanan
        panel_surface = pygame.Surface((self.panel_width, HEIGHT), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 200))
        screen.blit(panel_surface, (WIDTH - self.panel_width, 0))
        
        y_offset = 20
        
        # Title
        title = self.font.render("KONTROL & INFORMASI", True, (100, 255, 100))
        screen.blit(title, (WIDTH - self.panel_width + 20, y_offset))
        y_offset += 40
        
        # Visual Settings
        settings_title = self.font.render("SETTINGS VISUAL:", True, (200, 200, 100))
        screen.blit(settings_title, (WIDTH - self.panel_width + 20, y_offset))
        y_offset += 30
        
        # Show trails status
        trails_color = (0, 255, 0) if show_trails else (255, 100, 100)
        trails_text = self.small_font.render(f"Trails: {'ON' if show_trails else 'OFF'}", True, trails_color)
        screen.blit(trails_text, (WIDTH - self.panel_width + 40, y_offset))
        y_offset += 25
        
        # Show orbits status
        orbits_color = (0, 255, 0) if show_orbits else (255, 100, 100)
        orbits_text = self.small_font.render(f"Orbit Lines: {'ON' if show_orbits else 'OFF'}", True, orbits_color)
        screen.blit(orbits_text, (WIDTH - self.panel_width + 40, y_offset))
        y_offset += 25
        
        # Asteroid belt status
        asteroid_color = (0, 255, 0) if asteroid_belt_visible else (255, 100, 100)
        asteroid_text = self.small_font.render(f"Asteroid Belt: {'ON' if asteroid_belt_visible else 'OFF'}", True, asteroid_color)
        screen.blit(asteroid_text, (WIDTH - self.panel_width + 40, y_offset))
        y_offset += 25
        
        # Comet count
        comet_text = self.small_font.render(f"Active Comets: {num_comets}", True, (150, 200, 255))
        screen.blit(comet_text, (WIDTH - self.panel_width + 40, y_offset))
        y_offset += 40
        
        # Separator line
        pygame.draw.line(screen, (100, 100, 100), 
                        (WIDTH - self.panel_width + 20, y_offset),
                        (WIDTH - 20, y_offset), 2)
        y_offset += 20
        
        # Controls section
        controls_title = self.font.render("KONTROL KEYBOARD:", True, (255, 150, 100))
        screen.blit(controls_title, (WIDTH - self.panel_width + 20, y_offset))
        y_offset += 30
        
        controls = [
            ("Spasi", "Pause/Resume"),
            ("R", "Reset Simulasi"),
            ("+/-", "Kecepatan Waktu"),
            ("K", "Tambah Komet"),
            ("C", "Toggle Asteroid Belt"),
            ("T", "Toggle Trails"),
            ("O", "Toggle Orbit Lines"),
            ("ESC", "Keluar")
        ]
        
        for key, desc in controls:
            key_text = self.small_font.render(key, True, (255, 255, 100))
            screen.blit(key_text, (WIDTH - self.panel_width + 40, y_offset))
            
            desc_text = self.small_font.render(desc, True, (200, 200, 200))
            screen.blit(desc_text, (WIDTH - self.panel_width + 100, y_offset))
            
            y_offset += 25
        
        # Separator line
        pygame.draw.line(screen, (100, 100, 100), 
                        (WIDTH - self.panel_width + 20, y_offset),
                        (WIDTH - 20, y_offset), 2)
        y_offset += 20
        
        # Mouse controls
        mouse_title = self.font.render("KONTROL MOUSE:", True, (100, 200, 255))
        screen.blit(mouse_title, (WIDTH - self.panel_width + 20, y_offset))
        y_offset += 30
        
        mouse_controls = [
            "Scroll: Zoom In/Out",
            "Drag: Geser Kamera",
            "Klik Planet: Pilih Planet"
        ]
        
        for control in mouse_controls:
            control_text = self.small_font.render(control, True, (200, 220, 255))
            screen.blit(control_text, (WIDTH - self.panel_width + 40, y_offset))
            y_offset += 25
        
        # Separator line
        pygame.draw.line(screen, (100, 100, 100), 
                        (WIDTH - self.panel_width + 20, HEIGHT - 80),
                        (WIDTH - 20, HEIGHT - 80), 2)
        
        # Info footer
        footer = self.small_font.render("UTS GRAFIKA KOMPUTER - SIMULASI TATA SURYA", True, (150, 150, 255))
        screen.blit(footer, (WIDTH - self.panel_width + 20, HEIGHT - 50))

class AsteroidBelt:
    def __init__(self, inner_radius, outer_radius, num_asteroids=100):
        self.asteroids = []
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.visible = True
        
        for _ in range(num_asteroids):
            radius = random.uniform(inner_radius, outer_radius)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.001, 0.003) * (inner_radius / radius)  # Kepler's third law
            size = random.uniform(0.5, 2.0)
            self.asteroids.append({
                'radius': radius,
                'angle': angle,
                'speed': speed,
                'size': size,
                'color': (150, 150, 150, 200)
            })
    
    def update(self, dt, time_scale):
        if not self.visible:
            return
        
        for asteroid in self.asteroids:
            asteroid['angle'] += asteroid['speed'] * dt * time_scale
    
    def draw(self, camera_x=0, camera_y=0, zoom=1.0):
        if not self.visible or zoom < 0.2:
            return
        
        for asteroid in self.asteroids:
            x = asteroid['radius'] * math.cos(asteroid['angle'])
            y = asteroid['radius'] * math.sin(asteroid['angle'])
            
            screen_x = CENTER_X + (x - camera_x) * zoom
            screen_y = CENTER_Y + (y - camera_y) * zoom
            scaled_size = max(0.5, asteroid['size'] * zoom)
            
            if scaled_size > 0.3:
                # Draw asteroid using midpoint circle
                points = midpoint_circle(int(screen_x), int(screen_y), int(scaled_size))
                for px, py in points:
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        screen.set_at((px, py), asteroid['color'])

# ==================== MAIN GAME LOOP ====================

def main():
    # Create celestial bodies
    sun = CelestialBody("Matahari", 30, SUN_COLOR, 0, 0, 0.005, "sun.png")
    
    planets = [
        CelestialBody("Merkurius", 5, MERCURY_COLOR, 100, 0.04, 0.01, "mercury.png"),
        CelestialBody("Venus", 8, VENUS_COLOR, 150, 0.015, 0.008, "venus.png"),
        CelestialBody("Bumi", 9, EARTH_COLOR, 200, 0.01, 0.015, "earth.png"),
        CelestialBody("Mars", 7, MARS_COLOR, 260, 0.008, 0.012, "mars.png"),
        CelestialBody("Jupiter", 20, JUPITER_COLOR, 350, 0.004, 0.02, "jupiter.png"),
        CelestialBody("Saturnus", 18, SATURN_COLOR, 450, 0.003, 0.018, "saturn.png"),
        CelestialBody("Uranus", 12, URANUS_COLOR, 550, 0.002, 0.01, "uranus.png"),
        CelestialBody("Neptunus", 12, NEPTUNE_COLOR, 650, 0.001, 0.009, "neptune.png")
    ]
    
    # Create systems
    starfield = Starfield(300)
    saturn_ring = SaturnRing(planets[5])  # Saturn is index 5
    asteroid_belt = AsteroidBelt(280, 320, 150)
    ui = UISystem()
    
    # Game state
    camera_x, camera_y = 0, 0
    zoom = 1.0
    min_zoom, max_zoom = 0.1, 3.0
    dragging = False
    last_mouse_pos = (0, 0)
    paused = False
    time_scale = 1.0
    comets = []
    show_trails = True
    show_orbits = True
    
    # Create assets folder if it doesn't exist
    if not os.path.exists("assets"):
        os.makedirs("assets")
        print("Folder 'assets' dibuat. Silakan tambahkan gambar planet PNG ke folder tersebut.")
        print("Nama file yang diharapkan: sun.png, mercury.png, venus.png, earth.png,")
        print("mars.png, jupiter.png, saturn.png, uranus.png, neptune.png")
        print("Jika tidak ada gambar, program akan menggunakan warna default.")
    
    running = True
    last_time = pygame.time.get_ticks()
    
    while running:
        current_time = pygame.time.get_ticks()
        dt = (current_time - last_time) / 1000.0  # Delta time in seconds
        last_time = current_time
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()
                    
                    # Check planet selection (hanya di area tengah, bukan panel)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Skip jika klik di panel UI
                    if mouse_x > 300 and mouse_x < WIDTH - 300:
                        for planet in planets + [sun]:
                            px, py = planet.get_position(camera_x, camera_y, zoom)
                            dist = math.sqrt((mouse_x - px)**2 + (mouse_y - py)**2)
                            if dist < planet.radius * zoom:
                                for p in planets + [sun]:
                                    p.selected = False
                                planet.selected = True
                                break
                
                elif event.button == 4:  # Scroll up - zoom in
                    zoom = min(max_zoom, zoom * 1.1)
                
                elif event.button == 5:  # Scroll down - zoom out
                    zoom = max(min_zoom, zoom / 1.1)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = (mouse_x - last_mouse_pos[0]) / zoom
                    dy = (mouse_y - last_mouse_pos[1]) / zoom
                    camera_x -= dx
                    camera_y -= dy
                    last_mouse_pos = (mouse_x, mouse_y)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    # Reset simulation
                    camera_x, camera_y = 0, 0
                    zoom = 1.0
                    time_scale = 1.0
                    for planet in planets:
                        planet.orbit_angle = random.uniform(0, 2 * math.pi)
                        planet.trail.clear()
                    comets.clear()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    time_scale = min(10.0, time_scale * 1.2)
                elif event.key == pygame.K_MINUS:
                    time_scale = max(0.1, time_scale / 1.2)
                elif event.key == pygame.K_k:
                    comets.append(Comet())
                    if len(comets) > 10:
                        comets.pop(0)
                elif event.key == pygame.K_c:
                    asteroid_belt.visible = not asteroid_belt.visible
                elif event.key == pygame.K_t:
                    show_trails = not show_trails
                elif event.key == pygame.K_o:
                    show_orbits = not show_orbits
        
        # Clear screen
        screen.fill(BLACK)
        
        # Update starfield with camera offset for parallax
        starfield.update()
        starfield.draw(camera_x * 0.1, camera_y * 0.1)
        
        if not paused:
            # Update sun
            sun.update(dt, time_scale)
            
            # Update planets
            for planet in planets:
                planet.update(dt, time_scale)
            
            # Update Saturn's ring
            saturn_ring.update(dt, time_scale)
            
            # Update asteroid belt
            asteroid_belt.update(dt, time_scale)
            
            # Update comets
            for comet in comets[:]:
                comet.update(dt, time_scale)
                # Remove comets that are too far away
                if (comet.x < -200 or comet.x > WIDTH + 200 or 
                    comet.y < -200 or comet.y > HEIGHT + 200):
                    comets.remove(comet)
        
        # Draw orbits if enabled
        if show_orbits and zoom > 0.05:
            for planet in planets:
                if planet.orbit_radius > 0:
                    # Draw orbit circle using points
                    for angle in range(0, 360, max(1, int(5 / zoom))):
                        rad = math.radians(angle)
                        x = CENTER_X + (planet.orbit_radius * math.cos(rad) - camera_x) * zoom
                        y = CENTER_Y + (planet.orbit_radius * math.sin(rad) - camera_y) * zoom
                        
                        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                            alpha = 30
                            orbit_color = (100, 100, 150, alpha)
                            screen.set_at((int(x), int(y)), orbit_color)
        
        # Draw sun
        sun.draw(camera_x, camera_y, zoom, show_trails)
        
        # Draw planets
        for planet in planets:
            planet.draw(camera_x, camera_y, zoom, show_trails)
        
        # Draw Saturn's ring
        saturn_ring.draw(camera_x, camera_y, zoom)
        
        # Draw asteroid belt
        asteroid_belt.draw(camera_x, camera_y, zoom)
        
        # Draw comets
        for comet in comets:
            comet.draw(camera_x, camera_y, zoom)
        
        # Draw UI panels (kiri dan kanan)
        selected_planet = None
        for planet in planets + [sun]:
            if planet.selected:
                selected_planet = planet
                break
        
        fps = clock.get_fps()
        ui.draw_panel_left(paused, zoom, time_scale, selected_planet, fps)
        ui.draw_panel_right(show_trails, show_orbits, asteroid_belt.visible, len(comets))
        
        # Draw zoom and time indicators di tengah atas (tidak ketimpa panel)
        indicator_bg = pygame.Surface((200, 50), pygame.SRCALPHA)
        indicator_bg.fill((0, 0, 0, 150))
        screen.blit(indicator_bg, (WIDTH // 2 - 100, 10))
        
        zoom_text = ui.small_font.render(f"Zoom: {zoom:.2f}x", True, WHITE)
        screen.blit(zoom_text, (WIDTH // 2 - 90, 20))
        
        time_text = ui.small_font.render(f"Time: {time_scale:.1f}x", True, WHITE)
        screen.blit(time_text, (WIDTH // 2 - 90, 40))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()