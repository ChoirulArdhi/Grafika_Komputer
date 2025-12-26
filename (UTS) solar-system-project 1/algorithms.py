# algorithms.py
import pygame
import math

def draw_circle_midpoint(surface, center_x, center_y, radius, color):
    """Clean circle drawing with anti-aliasing approximation"""
    if radius <= 0:
        return
    
    center_x, center_y, radius = int(center_x), int(center_y), int(radius)
    
    # Untuk radius kecil, gunakan pygame.draw untuk kualitas lebih baik
    if radius < 10:
        if len(color) == 4:  # RGBA
            temp_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, color, (radius, radius), radius)
            surface.blit(temp_surf, (center_x - radius, center_y - radius))
        else:
            pygame.draw.circle(surface, color, (center_x, center_y), radius)
        return
    
    # Untuk radius besar, gunakan algoritma kita dengan smoothing
    x = radius
    y = 0
    err = 0
    
    # Pre-calculate points for smoother circle
    points = []
    while x >= y:
        points.extend([
            (center_x + x, center_y + y),
            (center_x + y, center_y + x),
            (center_x - y, center_y + x),
            (center_x - x, center_y + y),
            (center_x - x, center_y - y),
            (center_x - y, center_y - x),
            (center_x + y, center_y - x),
            (center_x + x, center_y - y)
        ])
        y += 1
        err += 1 + 2 * y
        if 2 * (err - x) + 1 > 0:
            x -= 1
            err += 1 - 2 * x
    
    # Draw all points
    for point in points:
        if 0 <= point[0] < surface.get_width() and 0 <= point[1] < surface.get_height():
            if len(color) == 4:  # Handle alpha
                # Simple alpha blending
                existing = surface.get_at(point)
                alpha = color[3] / 255.0
                blended = (
                    int(color[0] * alpha + existing[0] * (1 - alpha)),
                    int(color[1] * alpha + existing[1] * (1 - alpha)),
                    int(color[2] * alpha + existing[2] * (1 - alpha))
                )
                surface.set_at(point, blended)
            else:
                surface.set_at(point, color)

def draw_ellipse_orbit(surface, center_x, center_y, a, b, color):
    """Draw elliptical orbit with smooth lines"""
    if a <= 0 or b <= 0:
        return
    
    # Generate points along ellipse
    points = []
    steps = max(20, min(100, int((a + b) / 10)))  # Dynamic steps based on size
    
    for i in range(steps + 1):
        angle = 2 * math.pi * i / steps
        x = center_x + a * math.cos(angle)
        y = center_y + b * math.sin(angle)
        points.append((x, y))
    
    # Draw with pygame for smooth lines
    if len(points) > 1:
        if len(color) == 4:  # RGBA
            # Create temporary surface for alpha
            min_x = min(p[0] for p in points)
            max_x = max(p[0] for p in points)
            min_y = min(p[1] for p in points)
            max_y = max(p[1] for p in points)
            width = int(max_x - min_x) + 10
            height = int(max_y - min_y) + 10
            
            if width > 0 and height > 0:
                temp_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.lines(temp_surf, color, True, 
                                [(p[0]-min_x+5, p[1]-min_y+5) for p in points], 1)
                surface.blit(temp_surf, (min_x-5, min_y-5))
        else:
            pygame.draw.lines(surface, color, True, 
                            [(int(p[0]), int(p[1])) for p in points], 1)