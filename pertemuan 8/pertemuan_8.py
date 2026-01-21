import pygame
import sys
import math
import numpy as np
from pygame.locals import *

class Transformasi3D:
    def __init__(self):
        # Inisialisasi PyGame
        pygame.init()
        
        # Setup window
        self.WIDTH, self.HEIGHT = 1200, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Transformasi 3D - Mini Project Grafika Komputer - UNU Blitar")
        
        # Warna
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 120, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (180, 0, 255)
        self.CYAN = (0, 255, 255)
        self.ORANGE = (255, 165, 0)
        self.GRAY = (128, 128, 128)
        
        # Font
        self.font = pygame.font.SysFont('Arial', 20)
        self.title_font = pygame.font.SysFont('Arial', 28, bold=True)
        
        # Parameter kamera
        self.camera_pos = [0, 0, -800]  # Posisi kamera lebih jauh
        self.camera_angle = [0, 0, 0]
        self.focal_length = 800  # Jarak fokus untuk proyeksi perspektif
        
        # Parameter transformasi
        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]  # Sudut rotasi dalam derajat
        self.scale = [1, 1, 1]
        self.reflection = [1, 1, 1]  # 1 atau -1 untuk refleksi
        
        # Kecepatan transformasi
        self.translation_speed = 5
        self.rotation_speed = 2
        self.scale_speed = 0.1
        
        # Objek 3D: Kubus dengan warna berbeda di setiap sisi
        self.cube_vertices = np.array([
            [-100, -100, -100],  # 0: Back-bottom-left
            [100, -100, -100],   # 1: Back-bottom-right
            [100, 100, -100],    # 2: Back-top-right
            [-100, 100, -100],   # 3: Back-top-left
            [-100, -100, 100],   # 4: Front-bottom-left
            [100, -100, 100],    # 5: Front-bottom-right
            [100, 100, 100],     # 6: Front-top-right
            [-100, 100, 100]     # 7: Front-top-left
        ], dtype=float)
        
        # Warna untuk setiap sisi kubus
        self.face_colors = [
            self.RED,     # Back face
            self.GREEN,   # Front face
            self.BLUE,    # Top face
            self.YELLOW,  # Bottom face
            self.PURPLE,  # Left face
            self.CYAN     # Right face
        ]
        
        # Permukaan (wajah) kubus
        self.faces = [
            [0, 1, 2, 3],  # Back face
            [4, 5, 6, 7],  # Front face
            [3, 2, 6, 7],  # Top face
            [0, 1, 5, 4],  # Bottom face
            [0, 3, 7, 4],  # Left face
            [1, 2, 6, 5]   # Right face
        ]
        
        # Objek 3D: Piramida (limas segitiga)
        self.pyramid_vertices = np.array([
            [0, -150, 0],    # 0: Puncak
            [-120, 100, -120],   # 1: Kiri-belakang
            [120, 100, -120],    # 2: Kanan-belakang
            [120, 100, 120],     # 3: Kanan-depan
            [-120, 100, 120]     # 4: Kiri-depan
        ], dtype=float)
        
        self.pyramid_faces = [
            [1, 2, 0],  # Sisi belakang
            [2, 3, 0],  # Sisi kanan
            [3, 4, 0],  # Sisi depan
            [4, 1, 0],  # Sisi kiri
            [1, 2, 3, 4]  # Alas
        ]
        
        self.pyramid_face_colors = [
            self.RED,
            self.GREEN,
            self.BLUE,
            self.YELLOW,
            self.PURPLE
        ]
        
        # Objek 3D: Prisma segitiga
        self.prism_vertices = np.array([
            [0, -80, -150],   # 0: Kiri-belakang
            [150, -80, -150], # 1: Kanan-belakang
            [75, 80, -150],   # 2: Atas-belakang
            [0, -80, 150],    # 3: Kiri-depan
            [150, -80, 150],  # 4: Kanan-depan
            [75, 80, 150]     # 5: Atas-depan
        ], dtype=float)
        
        self.prism_faces = [
            [0, 1, 2],  # Segitiga belakang
            [3, 4, 5],  # Segitiga depan
            [0, 1, 4, 3],  # Alas
            [0, 2, 5, 3],  # Sisi kiri
            [1, 2, 5, 4]   # Sisi kanan
        ]
        
        self.prism_face_colors = [
            self.RED,
            self.GREEN,
            self.BLUE,
            self.YELLOW,
            self.PURPLE
        ]
        
        # Objek yang aktif (0: Kubus, 1: Piramida, 2: Prisma)
        self.active_object = 0
        
        # Status transformasi
        self.transform_mode = "rotation"  # rotation, translation, scale, reflection
        self.auto_rotate = True
        self.show_wireframe = True
        self.show_faces = True
        self.show_axes = True
        
        # Animasi
        self.animation_time = 0
        self.animation_speed = 0.02
        
        # Deklarasi variabel untuk menghindari error
        self.points = []
        
    def project_3d_to_2d(self, point):
        """Proyeksi 3D ke 2D dengan perspektif sederhana"""
        try:
            # Terapkan transformasi kamera
            x, y, z = point
            
            # Terapkan rotasi kamera
            x, y, z = self.apply_rotation(x, y, z, self.camera_angle)
            
            # Tambahkan posisi kamera
            x += self.camera_pos[0]
            y += self.camera_pos[1]
            z += self.camera_pos[2]
            
            # Proyeksi perspektif dengan handling pembagian nol
            # Tambahkan offset kecil ke z untuk menghindari pembagian nol
            z_adjusted = z + self.focal_length
            
            # Jika terlalu dekat dengan kamera, gunakan proyeksi paralel
            if abs(z_adjusted) < 10:
                factor = 1.0
            else:
                factor = self.focal_length / z_adjusted
                
            x_proj = x * factor + self.WIDTH / 2
            y_proj = -y * factor + self.HEIGHT / 2  # Negatif karena koordinat Y di layar terbalik
            
            return int(x_proj), int(y_proj)
        except Exception as e:
            # Fallback ke proyeksi paralel jika ada error
            x_proj = x + self.WIDTH / 2
            y_proj = -y + self.HEIGHT / 2
            return int(x_proj), int(y_proj)
    
    def apply_rotation(self, x, y, z, angles):
        """Terapkan rotasi pada titik 3D"""
        try:
            rx, ry, rz = np.radians(angles)
            
            # Rotasi terhadap sumbu X
            y1 = y * math.cos(rx) - z * math.sin(rx)
            z1 = y * math.sin(rx) + z * math.cos(rx)
            y, z = y1, z1
            
            # Rotasi terhadap sumbu Y
            x1 = x * math.cos(ry) + z * math.sin(ry)
            z1 = -x * math.sin(ry) + z * math.cos(ry)
            x, z = x1, z1
            
            # Rotasi terhadap sumbu Z
            x1 = x * math.cos(rz) - y * math.sin(rz)
            y1 = x * math.sin(rz) + y * math.cos(rz)
            x, y = x1, y1
            
            return x, y, z
        except:
            return x, y, z
    
    def apply_transformation(self, vertices):
        """Terapkan semua transformasi pada vertices"""
        try:
            transformed_vertices = vertices.copy()
            
            # Terapkan scaling
            transformed_vertices[:, 0] *= self.scale[0]
            transformed_vertices[:, 1] *= self.scale[1]
            transformed_vertices[:, 2] *= self.scale[2]
            
            # Terapkan refleksi
            transformed_vertices[:, 0] *= self.reflection[0]
            transformed_vertices[:, 1] *= self.reflection[1]
            transformed_vertices[:, 2] *= self.reflection[2]
            
            # Terapkan rotasi
            for i in range(len(transformed_vertices)):
                x, y, z = transformed_vertices[i]
                x, y, z = self.apply_rotation(x, y, z, self.rotation)
                transformed_vertices[i] = [x, y, z]
            
            # Terapkan translasi
            transformed_vertices[:, 0] += self.translation[0]
            transformed_vertices[:, 1] += self.translation[1]
            transformed_vertices[:, 2] += self.translation[2]
            
            return transformed_vertices
        except Exception as e:
            print(f"Error in apply_transformation: {e}")
            return vertices
    
    def draw_object(self, vertices, faces, face_colors=None):
        """Gambar objek 3D dengan wireframe dan/atau permukaan berwarna"""
        try:
            # Proyeksi semua vertices ke 2D
            projected = []
            for vertex in vertices:
                projected.append(self.project_3d_to_2d(vertex))
            
            # Gambar permukaan (faces) jika diaktifkan
            if self.show_faces and face_colors is not None:
                for i, face in enumerate(faces):
                    if len(face) >= 3:
                        # Buat daftar titik untuk polygon
                        self.points = [projected[idx] for idx in face]
                        
                        # Hitung normal untuk backface culling sederhana
                        try:
                            if len(face) == 3:
                                p1 = vertices[face[0]]
                                p2 = vertices[face[1]]
                                p3 = vertices[face[2]]
                            else:
                                p1 = vertices[face[0]]
                                p2 = vertices[face[1]]
                                p3 = vertices[face[2]]
                            
                            # Vektor normal
                            v1 = np.array(p2) - np.array(p1)
                            v2 = np.array(p3) - np.array(p1)
                            normal = np.cross(v1, v2)
                            
                            # Vektor dari titik ke kamera
                            view_vector = np.array(self.camera_pos) - np.array(p1)
                            
                            # Backface culling: hanya gambar jika normal menghadap kamera
                            if np.dot(normal, view_vector) > 0:
                                color = face_colors[i % len(face_colors)]
                                # Tambahkan efek pencahayaan sederhana
                                light_factor = max(0.3, min(1.0, normal[2] / 1000))
                                shaded_color = tuple(int(c * light_factor) for c in color)
                                
                                pygame.draw.polygon(self.screen, shaded_color, self.points)
                        except Exception as e:
                            # Jika ada error dalam perhitungan, gambar tanpa backface culling
                            color = face_colors[i % len(face_colors)]
                            pygame.draw.polygon(self.screen, color, self.points)
            
            # Gambar wireframe jika diaktifkan
            if self.show_wireframe:
                for face in faces:
                    for j in range(len(face)):
                        try:
                            start = projected[face[j]]
                            end = projected[face[(j + 1) % len(face)]]
                            pygame.draw.line(self.screen, self.WHITE, start, end, 2)
                        except:
                            continue
            
            # Gambar vertices sebagai titik
            for point in projected:
                try:
                    pygame.draw.circle(self.screen, self.YELLOW, point, 4)
                except:
                    continue
        except Exception as e:
            print(f"Error drawing object: {e}")
    
    def draw_axes(self):
        """Gambar sumbu koordinat 3D"""
        if not self.show_axes:
            return
            
        try:
            origin = [0, 0, 0]
            
            # Sumbu X (Merah) - panjang 200
            x_axis = [200, 0, 0]
            start = self.project_3d_to_2d(origin)
            end = self.project_3d_to_2d(x_axis)
            pygame.draw.line(self.screen, self.RED, start, end, 3)
            
            # Label sumbu X
            if end[0] > 0 and end[1] > 0:
                font = pygame.font.SysFont('Arial', 16, bold=True)
                x_label = font.render('X', True, self.RED)
                self.screen.blit(x_label, (end[0] + 5, end[1] - 10))
            
            # Sumbu Y (Hijau)
            y_axis = [0, 200, 0]
            end = self.project_3d_to_2d(y_axis)
            pygame.draw.line(self.screen, self.GREEN, start, end, 3)
            
            # Label sumbu Y
            if end[0] > 0 and end[1] > 0:
                y_label = font.render('Y', True, self.GREEN)
                self.screen.blit(y_label, (end[0] + 5, end[1] - 10))
            
            # Sumbu Z (Biru)
            z_axis = [0, 0, 200]
            end = self.project_3d_to_2d(z_axis)
            pygame.draw.line(self.screen, self.BLUE, start, end, 3)
            
            # Label sumbu Z
            if end[0] > 0 and end[1] > 0:
                z_label = font.render('Z', True, self.BLUE)
                self.screen.blit(z_label, (end[0] + 5, end[1] - 10))
        except Exception as e:
            print(f"Error drawing axes: {e}")
    
    def draw_control_panel(self):
        """Gambar panel kontrol dan informasi"""
        try:
            # Background panel
            pygame.draw.rect(self.screen, (30, 30, 40), (10, 10, 400, 250), border_radius=10)
            pygame.draw.rect(self.screen, (50, 50, 60), (10, 10, 400, 250), 2, border_radius=10)
            
            # Judul
            title = self.title_font.render("TRANSFORMASI 3D - UNU Blitar", True, self.CYAN)
            self.screen.blit(title, (20, 20))
            
            subtitle = self.font.render("Mini Project Grafika Komputer - Program Studi Ilmu Komputer", True, self.WHITE)
            self.screen.blit(subtitle, (20, 55))
            
            # Informasi objek
            objects = ["KUBUS", "PIRAMIDA", "PRISMA"]
            obj_text = self.font.render(f"OBJEK: {objects[self.active_object]}", True, self.YELLOW)
            self.screen.blit(obj_text, (20, 90))
            
            # Status transformasi
            mode_text = self.font.render(f"MODE: {self.transform_mode.upper()}", True, self.GREEN)
            self.screen.blit(mode_text, (20, 120))
            
            # Parameter transformasi
            trans_text = self.font.render(f"Translasi: X={self.translation[0]:.1f}, Y={self.translation[1]:.1f}, Z={self.translation[2]:.1f}", True, self.WHITE)
            self.screen.blit(trans_text, (20, 150))
            
            rot_text = self.font.render(f"Rotasi: X={self.rotation[0]:.1f}°, Y={self.rotation[1]:.1f}°, Z={self.rotation[2]:.1f}°", True, self.WHITE)
            self.screen.blit(rot_text, (20, 175))
            
            scale_text = self.font.render(f"Skala: X={self.scale[0]:.2f}, Y={self.scale[1]:.2f}, Z={self.scale[2]:.2f}", True, self.WHITE)
            self.screen.blit(scale_text, (20, 200))
            
            refl_text = self.font.render(f"Refleksi: X={'-' if self.reflection[0] < 0 else '+'}, Y={'-' if self.reflection[1] < 0 else '+'}, Z={'-' if self.reflection[2] < 0 else '+'}", True, self.WHITE)
            self.screen.blit(refl_text, (20, 225))
            
            # Panel kontrol di kanan
            pygame.draw.rect(self.screen, (30, 40, 30), (self.WIDTH - 350, 10, 340, 320), border_radius=10)
            pygame.draw.rect(self.screen, (50, 60, 50), (self.WIDTH - 350, 10, 340, 320), 2, border_radius=10)
            
            ctrl_title = self.font.render("KONTROL TRANSFORMASI", True, self.YELLOW)
            self.screen.blit(ctrl_title, (self.WIDTH - 340, 20))
            
            controls = [
                "1-3: Ganti Objek (Kubus/Piramida/Prisma)",
                "T: Mode Translasi   R: Mode Rotasi",
                "S: Mode Skala       F: Mode Refleksi",
                "",
                "TRANSLASI:",
                "  Q/W: X±    A/S: Y±    Z/X: Z±",
                "",
                "ROTASI:",
                "  Q/W: X±    A/S: Y±    Z/X: Z±",
                "",
                "SKALA:",
                "  Q/W: X±    A/S: Y±    Z/X: Z±",
                "",
                "REFLESI: Tekan Q/A/Z untuk toggle",
                "PANAH: Rotasi Kamera",
                "SPACE: Reset semua transformasi",
                "V: Toggle Wireframe  B: Toggle Faces",
                "N: Toggle Sumbu      ESC: Keluar"
            ]
            
            y_offset = 50
            for control in controls:
                ctrl_text = pygame.font.SysFont('Arial', 14).render(control, True, self.WHITE)
                self.screen.blit(ctrl_text, (self.WIDTH - 340, y_offset))
                y_offset += 20
            
            # Panel informasi transformasi di bawah
            pygame.draw.rect(self.screen, (40, 30, 30), (10, self.HEIGHT - 220, 500, 210), border_radius=10)
            pygame.draw.rect(self.screen, (60, 50, 50), (10, self.HEIGHT - 220, 500, 210), 2, border_radius=10)
            
            info_title = self.font.render("INFORMASI TRANSFORMASI 3D", True, self.CYAN)
            self.screen.blit(info_title, (20, self.HEIGHT - 210))
            
            info_text = [
                "1. TRANSLASI 3D: Menggeser objek dalam ruang 3D",
                "   Rumus: P' = P + T  dimana T = (tx, ty, tz)",
                "",
                "2. ROTASI 3D: Memutar objek terhadap sumbu X,Y,Z",
                "   Matriks Rotasi X: Rx(θ) = [[1,0,0],[0,cosθ,-sinθ],[0,sinθ,cosθ]]",
                "",
                "3. SKALA 3D: Mengubah ukuran objek secara proporsional",
                "   Rumus: P' = S × P  dimana S = (sx, sy, sz)",
                "",
                "4. REFLEKSI 3D: Mencerminkan objek terhadap bidang",
                "   Contoh refleksi sumbu X: M = [[-1,0,0],[0,1,0],[0,0,1]]"
            ]
            
            y_offset = self.HEIGHT - 180
            for line in info_text:
                info_line = pygame.font.SysFont('Courier', 12).render(line, True, self.WHITE)
                self.screen.blit(info_line, (20, y_offset))
                y_offset += 18
        except Exception as e:
            print(f"Error drawing control panel: {e}")
    
    def reset_transformations(self):
        """Reset semua transformasi ke nilai default"""
        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]
        self.reflection = [1, 1, 1]
    
    def handle_input(self):
        """Handle input dari keyboard"""
        keys = pygame.key.get_pressed()
        
        # Ganti objek
        if keys[pygame.K_1]:
            self.active_object = 0  # Kubus
        if keys[pygame.K_2]:
            self.active_object = 1  # Piramida
        if keys[pygame.K_3]:
            self.active_object = 2  # Prisma
        
        # Ganti mode transformasi
        if keys[pygame.K_t]:
            self.transform_mode = "translation"
        if keys[pygame.K_r]:
            self.transform_mode = "rotation"
        if keys[pygame.K_s]:
            self.transform_mode = "scale"
        if keys[pygame.K_f]:
            self.transform_mode = "reflection"
        
        # Transformasi berdasarkan mode
        if self.transform_mode == "translation":
            if keys[pygame.K_q]:  # X-
                self.translation[0] -= self.translation_speed
            if keys[pygame.K_w]:  # X+
                self.translation[0] += self.translation_speed
            if keys[pygame.K_a]:  # Y-
                self.translation[1] -= self.translation_speed
            if keys[pygame.K_s]:  # Y+
                self.translation[1] += self.translation_speed
            if keys[pygame.K_z]:  # Z-
                self.translation[2] -= self.translation_speed
            if keys[pygame.K_x]:  # Z+
                self.translation[2] += self.translation_speed
                
        elif self.transform_mode == "rotation":
            if keys[pygame.K_q]:  # X-
                self.rotation[0] -= self.rotation_speed
            if keys[pygame.K_w]:  # X+
                self.rotation[0] += self.rotation_speed
            if keys[pygame.K_a]:  # Y-
                self.rotation[1] -= self.rotation_speed
            if keys[pygame.K_d]:  # Y+
                self.rotation[1] += self.rotation_speed
            if keys[pygame.K_z]:  # Z-
                self.rotation[2] -= self.rotation_speed
            if keys[pygame.K_c]:  # Z+
                self.rotation[2] += self.rotation_speed
                
        elif self.transform_mode == "scale":
            if keys[pygame.K_q]:  # X-
                self.scale[0] = max(0.1, self.scale[0] - self.scale_speed)
            if keys[pygame.K_w]:  # X+
                self.scale[0] += self.scale_speed
            if keys[pygame.K_a]:  # Y-
                self.scale[1] = max(0.1, self.scale[1] - self.scale_speed)
            if keys[pygame.K_d]:  # Y+
                self.scale[1] += self.scale_speed
            if keys[pygame.K_z]:  # Z-
                self.scale[2] = max(0.1, self.scale[2] - self.scale_speed)
            if keys[pygame.K_c]:  # Z+
                self.scale[2] += self.scale_speed
                
        elif self.transform_mode == "reflection":
            if keys[pygame.K_q]:  # Toggle X
                self.reflection[0] *= -1
                pygame.time.delay(200)  # Debounce
            if keys[pygame.K_a]:  # Toggle Y
                self.reflection[1] *= -1
                pygame.time.delay(200)
            if keys[pygame.K_z]:  # Toggle Z
                self.reflection[2] *= -1
                pygame.time.delay(200)
        
        # Kontrol kamera
        if keys[pygame.K_LEFT]:
            self.camera_angle[1] += 1
        if keys[pygame.K_RIGHT]:
            self.camera_angle[1] -= 1
        if keys[pygame.K_UP]:
            self.camera_angle[0] += 1
        if keys[pygame.K_DOWN]:
            self.camera_angle[0] -= 1
        
        # Reset
        if keys[pygame.K_SPACE]:
            self.reset_transformations()
        
        # Toggle wireframe dan faces
        if keys[pygame.K_v]:
            self.show_wireframe = not self.show_wireframe
            pygame.time.delay(200)
        if keys[pygame.K_b]:
            self.show_faces = not self.show_faces
            pygame.time.delay(200)
        if keys[pygame.K_n]:
            self.show_axes = not self.show_axes
            pygame.time.delay(200)
    
    def update_animation(self):
        """Update animasi transformasi otomatis"""
        if self.auto_rotate:
            self.animation_time += self.animation_speed
            
            # Rotasi otomatis
            self.rotation[0] = math.sin(self.animation_time * 0.5) * 30
            self.rotation[1] = math.sin(self.animation_time * 0.7) * 45
            self.rotation[2] = self.animation_time * 20
            
            # Translasi bergelombang
            self.translation[0] = math.sin(self.animation_time * 0.3) * 100
            self.translation[1] = math.cos(self.animation_time * 0.4) * 50
            
            # Scaling berdenyut
            pulse = 0.5 * math.sin(self.animation_time) + 1.0
            self.scale = [pulse, pulse, pulse]
    
    def run(self):
        """Main loop"""
        clock = pygame.time.Clock()
        
        print("=" * 70)
        print("PRAKTIKUM TRANSFORMASI 3D - GRAFIKA KOMPUTER")
        print("Program Studi Ilmu Komputer")
        print("Universitas Nahdlatul Ulama Blitar")
        print("=" * 70)
        print("\nMini Project: Sistem Transformasi 3D Interaktif")
        print("Menerapkan 4 transformasi: Translasi, Rotasi, Skala, Refleksi")
        print("\nKontrol:")
        print("1-3: Ganti objek (Kubus/Piramida/Prisma)")
        print("T/R/S/F: Mode transformasi")
        print("Q/W, A/S, Z/X: Kontrol transformasi")
        print("Panah: Rotasi Kamera")
        print("SPACE: Reset  V: Wireframe  B: Faces  N: Sumbu")
        print("ESC: Keluar")
        print("-" * 70)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
            
            # Handle input keyboard
            self.handle_input()
            
            # Update animasi
            self.update_animation()
            
            # Bersihkan layar
            self.screen.fill(self.BLACK)
            
            # Gambar sumbu koordinat
            self.draw_axes()
            
            # Pilih dan gambar objek aktif
            try:
                if self.active_object == 0:  # Kubus
                    transformed_vertices = self.apply_transformation(self.cube_vertices)
                    self.draw_object(transformed_vertices, self.faces, self.face_colors)
                elif self.active_object == 1:  # Piramida
                    transformed_vertices = self.apply_transformation(self.pyramid_vertices)
                    self.draw_object(transformed_vertices, self.pyramid_faces, self.pyramid_face_colors)
                elif self.active_object == 2:  # Prisma
                    transformed_vertices = self.apply_transformation(self.prism_vertices)
                    self.draw_object(transformed_vertices, self.prism_faces, self.prism_face_colors)
            except Exception as e:
                print(f"Error drawing active object: {e}")
            
            # Gambar panel kontrol
            self.draw_control_panel()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = Transformasi3D()
    app.run()