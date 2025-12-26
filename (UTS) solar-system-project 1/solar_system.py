# solar_system.py
import pygame
import math
import random
import os
from algorithms import draw_circle_midpoint, draw_ellipse_orbit

class CelestialBody:
    def __init__(self, name, distance, radius, color, orbital_speed, rotation_speed, 
                 has_atmosphere=False, has_ring=False, image_path=None):
        self.name = name
        self.distance = distance
        self.radius = radius
        self.color = color
        self.orbital_speed = orbital_speed
        self.rotation_speed = rotation_speed
        self.has_atmosphere = has_atmosphere
        self.has_ring = has_ring
        
        # Posisi dan rotasi
        self.angle = random.uniform(0, 2 * math.pi)
        self.rotation = 0
        
        # Animasi smooth
        self.target_scale = 1.0
        self.current_scale = 1.0
        self.scale_speed = 0.1
        
        # Handling gambar
        self.original_image = None
        self.current_image = None
        self.has_image = False
        
        if image_path and os.path.exists(image_path):
            try:
                self.original_image = pygame.image.load(image_path).convert_alpha()
                self.has_image = True
                self.update_image_size()
            except:
                print(f"Could not load image: {image_path}")
                self.has_image = False
    
    def update_image_size(self):
        """Update ukuran gambar dengan smooth scaling"""
        if self.has_image and self.original_image:
            target_size = int(self.radius * 2 * self.current_scale)
            target_size = max(4, min(target_size, 200))  # Batasi ukuran
            self.current_image = pygame.transform.smoothscale(self.original_image, 
                                                             (target_size, target_size))
    
    def update(self, dt):
        """Update dengan delta time untuk smooth animation"""
        # Update posisi orbit
        self.angle += self.orbital_speed * dt
        
        # Update rotasi
        self.rotation += self.rotation_speed * dt
        
        # Smooth scaling
        scale_diff = self.target_scale - self.current_scale
        self.current_scale += scale_diff * self.scale_speed * dt
        
        if self.has_image and abs(scale_diff) > 0.01:
            self.update_image_size()
    
    def get_position(self, center_x, center_y):
        """Get planet position with smooth orbit"""
        x = center_x + self.distance * math.cos(self.angle)
        y = center_y + self.distance * math.sin(self.angle)
        return int(x), int(y)
    
    def draw(self, surface, center_x, center_y):
        """Draw planet with smooth effects"""
        x, y = self.get_position(center_x, center_y)
        display_radius = int(self.radius * self.current_scale)
        
        # Gambar atmosfer (jika ada)
        if self.has_atmosphere and display_radius > 5:
            atmosphere_radius = int(display_radius * 1.3)
            atmosphere_color = (*self.color[:3], 80)  # RGBA dengan alpha
            draw_circle_midpoint(surface, x, y, atmosphere_radius, atmosphere_color)
        
        # Gambar planet utama
        if self.has_image and self.current_image:
            # Rotasi smooth
            if display_radius > 8:  # Hanya rotasi jika cukup besar
                rotation_angle = math.degrees(self.rotation) % 360
                rotated_img = pygame.transform.rotate(self.current_image, rotation_angle)
                img_rect = rotated_img.get_rect(center=(x, y))
                surface.blit(rotated_img, img_rect)
            else:
                img_rect = self.current_image.get_rect(center=(x, y))
                surface.blit(self.current_image, img_rect)
        else:
            # Fallback: lingkaran dengan gradien
            draw_circle_midpoint(surface, x, y, display_radius, self.color)
            
            # Efek cahaya
            if display_radius > 6:
                highlight_radius = display_radius // 3
                highlight_x = x - display_radius // 3
                highlight_y = y - display_radius // 3
                highlight_color = tuple(min(255, c + 50) for c in self.color[:3])
                draw_circle_midpoint(surface, highlight_x, highlight_y, 
                                   highlight_radius, highlight_color)
        
        # Gambar cincin (untuk Saturnus)
        if self.has_ring and display_radius > 8:
            self.draw_ring(surface, x, y, display_radius)
    
    def draw_ring(self, surface, x, y, radius):
        """Draw planetary ring with transparency"""
        ring_width = max(2, radius // 8)
        ring_inner = int(radius * 1.2)
        ring_outer = int(radius * 1.8)
        
        # Gambar ring sebagai elips transparan
        for a in range(0, 360, 5):
            angle = math.radians(a)
            # Outer point
            ox = x + ring_outer * math.cos(angle)
            oy = y + ring_outer * math.sin(angle) * 0.3  # Elips
        
            # Inner point  
            ix = x + ring_inner * math.cos(angle)
            iy = y + ring_inner * math.sin(angle) * 0.3
            
            # Gambar dengan warna transparan
            ring_color = (200, 180, 140, 150)
            # Untuk garis sederhana, kita gunakan pygame.draw
            pygame.draw.line(surface, ring_color[:3], (int(ox), int(oy)), 
                           (int(ix), int(iy)), ring_width)
    
    def set_highlight(self, highlight):
        """Set highlight effect on planet"""
        self.target_scale = 1.2 if highlight else 1.0

class SolarSystem:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        
        # Data planet REALISTIS (skala disesuaikan)
        self.planets = [
            # name, distance, radius, color, orbital_speed, rotation_speed, atmosphere, ring, image
            CelestialBody("Matahari", 0, 40, (255, 255, 100), 0, 0.002, False, False, "assets/sun.png"),
            CelestialBody("Merkurius", 80, 4, (169, 169, 169), 0.04, 0.005, False, False, "assets/mercury.png"),
            CelestialBody("Venus", 120, 9, (255, 165, 50), 0.03, 0.002, True, False, "assets/venus.png"),
            CelestialBody("Bumi", 170, 10, (65, 105, 225), 0.02, 0.01, True, False, "assets/earth.png"),
            CelestialBody("Mars", 220, 7, (220, 80, 60), 0.015, 0.008, False, False, "assets/mars.png"),
            CelestialBody("Jupiter", 320, 22, (218, 165, 105), 0.008, 0.02, True, False, "assets/jupiter.png"),
            CelestialBody("Saturnus", 420, 20, (210, 180, 140), 0.006, 0.015, True, True, "assets/saturn.png"),
            CelestialBody("Uranus", 520, 15, (135, 206, 235), 0.004, 0.012, True, False, "assets/uranus.png"),
            CelestialBody("Neptunus", 620, 15, (30, 144, 255), 0.003, 0.01, True, False, "assets/neptune.png")
        ]
        
        # Bulan (satelit Bumi)
        self.moon = {
            "distance": 25,
            "radius": 3,
            "color": (200, 200, 200),
            "angle": 0,
            "speed": 0.05
        }
        
        # Komet (efek translasi)
        self.comets = []
        self.init_comets()
        
        # Informasi planet yang sedang dihover
        self.hovered_planet = None
        self.info_panel = None
        
        # Zoom dan camera
        self.zoom_level = 1.0
        self.target_zoom = 1.0
        self.camera_x = 0
        self.camera_y = 0
        self.target_camera_x = 0
        self.target_camera_y = 0
        
        # TAMBAH ATTRIBUTE INI
        self.paused = False
    
    def init_comets(self):
        """Initialize comets with realistic trajectories"""
        for _ in range(2):
            self.comets.append({
                "x": random.randint(-200, 1400),
                "y": random.randint(-200, 800),
                "vx": random.uniform(-1.5, -0.5),
                "vy": random.uniform(-0.3, 0.3),
                "size": random.uniform(2, 4),
                "trail": [],
                "max_trail": 15
            })
    
    def update(self, dt):
        """Update semua objek dengan delta time"""
        if self.paused:
            return
            
        # Update planet
        for planet in self.planets[1:]:  # Skip sun
            planet.update(dt)
        
        # Update moon
        self.moon["angle"] += self.moon["speed"] * dt
        
        # Update comets (translasi linear)
        for comet in self.comets:
            # Simpan posisi untuk trail
            comet["trail"].append((comet["x"], comet["y"]))
            if len(comet["trail"]) > comet["max_trail"]:
                comet["trail"].pop(0)
            
            # Translasi posisi
            comet["x"] += comet["vx"] * dt * 60  # Normalize untuk 60 FPS
            comet["y"] += comet["vy"] * dt * 60
            
            # Reset jika keluar layar
            if comet["x"] < -100 or comet["x"] > 1500 or comet["y"] < -100 or comet["y"] > 900:
                comet["x"] = random.randint(1300, 1500)
                comet["y"] = random.randint(100, 700)
                comet["vx"] = random.uniform(-1.5, -0.5)
                comet["vy"] = random.uniform(-0.3, 0.3)
                comet["trail"] = []
        
        # Smooth camera movement
        camera_speed = 0.1 * dt * 60
        self.camera_x += (self.target_camera_x - self.camera_x) * camera_speed
        self.camera_y += (self.target_camera_y - self.camera_y) * camera_speed
        
        # Smooth zoom
        zoom_speed = 0.05 * dt * 60
        self.zoom_level += (self.target_zoom - self.zoom_level) * zoom_speed
        
        # Update hover effect
        self.update_hover_effect()
    
    def update_hover_effect(self):
        """Update highlight pada planet yang dihover"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        self.hovered_planet = None
        for planet in self.planets:
            px, py = planet.get_position(self.center_x + self.camera_x, 
                                        self.center_y + self.camera_y)
            dx = mouse_x - px
            dy = mouse_y - py
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < planet.radius * planet.current_scale * 1.5:
                self.hovered_planet = planet
                planet.set_highlight(True)
                
                # Update info panel
                self.info_panel = {
                    "name": planet.name,
                    "distance": f"{planet.distance:.0f} unit",
                    "radius": f"{planet.radius:.1f} unit",
                    "speed": f"{planet.orbital_speed * 100:.2f}°/s"
                }
                break
            else:
                planet.set_highlight(False)
    
    def draw(self, surface):
        """Draw semua objek dengan efek smooth"""
        # Calculate effective center with camera
        eff_center_x = self.center_x + self.camera_x
        eff_center_y = self.center_y + self.camera_y
        
        # Gambar orbit (hanya untuk planet)
        for planet in self.planets[1:]:
            if planet.distance * self.zoom_level > 20:  # Hanya gambar jika cukup besar
                orbit_color = (80, 80, 120, 50)
                draw_ellipse_orbit(surface, eff_center_x, eff_center_y, 
                                 planet.distance * self.zoom_level, 
                                 planet.distance * self.zoom_level * 0.95,
                                 orbit_color)
        
        # Gambar komet (translasi linear)
        for comet in self.comets:
            # Gambar trail
            for i, (trail_x, trail_y) in enumerate(comet["trail"]):
                alpha = int(100 * (i / len(comet["trail"])))
                size = comet["size"] * (i / len(comet["trail"]))
                if size > 0.5:
                    trail_color = (150, 200, 255, alpha)
                    pygame.draw.circle(surface, trail_color[:3], 
                                     (int(trail_x), int(trail_y)), int(size))
            
            # Gambar kepala komet
            pygame.draw.circle(surface, (200, 230, 255), 
                             (int(comet["x"]), int(comet["y"])), int(comet["size"]))
        
        # Gambar planet dengan zoom
        for planet in self.planets:
            # Apply zoom ke distance untuk posisi
            scaled_distance = planet.distance * self.zoom_level
            angle = planet.angle
            
            # Hitung posisi dengan zoom
            if planet.name == "Matahari":
                px, py = eff_center_x, eff_center_y
            else:
                px = eff_center_x + scaled_distance * math.cos(angle)
                py = eff_center_y + scaled_distance * math.sin(angle)
            
            # Simpan posisi yang sudah di-scale untuk drawing
            planet._temp_pos = (int(px), int(py))
            
            # Apply zoom ke radius untuk drawing
            original_radius = planet.radius
            planet.radius = original_radius * self.zoom_level
            planet.draw(surface, eff_center_x, eff_center_y)
            planet.radius = original_radius  # Kembalikan ke original
        
        # Gambar bulan (mengorbit Bumi)
        earth = self.planets[3]  # Bumi
        earth_pos = earth._temp_pos if hasattr(earth, '_temp_pos') else earth.get_position(eff_center_x, eff_center_y)
        
        moon_angle = self.moon["angle"]
        moon_distance = self.moon["distance"] * self.zoom_level
        moon_x = earth_pos[0] + moon_distance * math.cos(moon_angle)
        moon_y = earth_pos[1] + moon_distance * math.sin(moon_angle)
        
        moon_radius = self.moon["radius"] * self.zoom_level
        if moon_radius > 1:
            pygame.draw.circle(surface, self.moon["color"], 
                             (int(moon_x), int(moon_y)), int(moon_radius))
            
            # Orbit bulan
            moon_orbit_color = (150, 150, 180, 30)
            pygame.draw.circle(surface, moon_orbit_color[:3], earth_pos, 
                             int(moon_distance), 1)
        
        # Gambar informasi jika ada planet dihover
        if self.hovered_planet and self.info_panel:
            self.draw_planet_info(surface, self.hovered_planet._temp_pos)
        
        # Gambar informasi zoom
        self.draw_zoom_info(surface)
    
    def draw_planet_info(self, surface, position):
        """Draw informasi planet dengan efek smooth"""
        x, y = position
        
        # Background panel
        panel_width = 200
        panel_height = 120
        panel_x = x + 20
        panel_y = y - panel_height - 20
        
        # Pastikan panel tidak keluar layar
        if panel_x + panel_width > surface.get_width():
            panel_x = x - panel_width - 20
        if panel_y < 0:
            panel_y = y + 20
        
        # Panel dengan rounded corners
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (20, 20, 40, 230), 
                        panel_surf.get_rect(), border_radius=10)
        pygame.draw.rect(panel_surf, (100, 100, 150, 150), 
                        panel_surf.get_rect(), 2, border_radius=10)
        surface.blit(panel_surf, (panel_x, panel_y))
        
        # Informasi planet
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 20)
        
        info_lines = [
            self.info_panel["name"],
            f"Jarak: {self.info_panel['distance']}",
            f"Radius: {self.info_panel['radius']}",
            f"Kecepatan: {self.info_panel['speed']}"
        ]
        
        for i, line in enumerate(info_lines):
            color = (255, 220, 100) if i == 0 else (220, 220, 240)
            text_font = font if i == 0 else small_font
            text = text_font.render(line, True, color)
            surface.blit(text, (panel_x + 10, panel_y + 10 + i * 28))
    
    def draw_zoom_info(self, surface):
        """Draw informasi zoom level"""
        zoom_text = f"Zoom: {self.zoom_level:.2f}x"
        font = pygame.font.Font(None, 24)
        text = font.render(zoom_text, True, (200, 200, 255))
        surface.blit(text, (20, surface.get_height() - 40))
        
        # Camera position
        cam_text = f"Posisi: ({int(self.camera_x)}, {int(self.camera_y)})"
        cam_text_surf = font.render(cam_text, True, (200, 200, 255))
        surface.blit(cam_text_surf, (20, surface.get_height() - 70))
    
    def zoom_in(self):
        """Zoom in smooth"""
        self.target_zoom = min(2.5, self.target_zoom * 1.2)
    
    def zoom_out(self):
        """Zoom out smooth"""
        self.target_zoom = max(0.5, self.target_zoom / 1.2)
    
    def move_camera(self, dx, dy):
        """Gerakkan kamera dengan smooth"""
        self.target_camera_x += dx
        self.target_camera_y += dy
        
        # Batasi gerakan kamera
        max_move = 500
        self.target_camera_x = max(-max_move, min(max_move, self.target_camera_x))
        self.target_camera_y = max(-max_move, min(max_move, self.target_camera_y))
    
    def reset_view(self):
        """Reset view ke posisi awal"""
        self.target_camera_x = 0
        self.target_camera_y = 0
        self.target_zoom = 1.0