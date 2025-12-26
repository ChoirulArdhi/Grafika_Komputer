# transformations.py
import math

class Transform2D:
    """Clean implementation of 2D transformations"""
    
    @staticmethod
    def translate(point, tx, ty):
        """Simple translation"""
        x, y = point
        return (x + tx, y + ty)
    
    @staticmethod
    def rotate(point, angle, center=(0, 0)):
        """Rotation around center point"""
        x, y = point
        cx, cy = center
        
        # Translate to origin
        x -= cx
        y -= cy
        
        # Rotate
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        x_new = x * cos_a - y * sin_a
        y_new = x * sin_a + y * cos_a
        
        # Translate back
        return (x_new + cx, y_new + cy)
    
    @staticmethod
    def scale(point, sx, sy, center=(0, 0)):
        """Scaling relative to center"""
        x, y = point
        cx, cy = center
        
        # Translate to origin
        x -= cx
        y -= cy
        
        # Scale
        x_new = x * sx
        y_new = y * sy
        
        # Translate back
        return (x_new + cx, y_new + cy)
    
    @staticmethod
    def reflect(point, axis='x', center=(0, 0)):
        """Reflection about axis or point"""
        x, y = point
        cx, cy = center
        
        if axis == 'x':  # Reflect about x-axis through center
            return (x, 2*cy - y)
        elif axis == 'y':  # Reflect about y-axis through center
            return (2*cx - x, y)
        elif axis == 'origin':  # Reflect about origin
            return (-x, -y)
        else:
            return (x, y)
    
    @staticmethod
    def apply_all(point, transformations):
        """Apply multiple transformations in order"""
        result = point
        for transform in transformations:
            result = transform(result)
        return result