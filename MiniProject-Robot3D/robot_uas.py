"""
MINI PROJECT GRAFIKA KOMPUTER 3D - VERSION CORRECTED
Robot 3D dengan Transformasi Hierarkis yang BENAR
"""

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

class Robot3D:
    def __init__(self):
        # Transformasi global
        self.pos = [0.0, 2.0, 0.0]  # Robot di atas ground
        self.rot = [0.0, 0.0, 0.0]
        self.scale = 0.5  # Skala lebih kecil
        
        # Parameter animasi
        self.arm_angle = 0.0
        self.leg_angle = 0.0
        self.animating = True
        
        # Kamera
        self.cam_distance = 8.0
        self.cam_angle = 45.0
        
        # Warna modern (Silver, Blue, Cyan)
        self.colors = {
            'head': (0.7, 0.7, 0.75),    # Light Metal
            'body': (0.2, 0.4, 0.7),    # Deep Blue
            'arm': (0.6, 0.6, 0.65),    # Chrome
            'leg': (0.6, 0.6, 0.65),    # Chrome
            'visor': (0.0, 0.8, 1.0),   # Cyan Glow
            'joint': (0.3, 0.3, 0.3),   # Dark Metal
            'cargo': (0.8, 0.5, 0.0)    # Orange (Courier standard)
        }

    def init_gl(self):
        """Setup OpenGL dengan pencahayaan yang lebih terang"""
        glClearColor(0.6, 0.8, 1.0, 1.0) # Langit biru cerah
        glEnable(GL_DEPTH_TEST)
        
        # Lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        # Tambahkan cahaya ambient agar bayangan tidak terlalu hitam/gelap
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.5, 0.5, 0.5, 1.0])
        
        light_pos = [5.0, 10.0, 5.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0]) # Cahaya putih terang
        
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Enable blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def draw_cube(self, size_x=1.0, size_y=1.0, size_z=1.0):
        """Draw cube dengan ukuran tertentu - lebih sederhana"""
        sx, sy, sz = size_x/2, size_y/2, size_z/2
        
        glBegin(GL_QUADS)
        # Front
        glNormal3f(0, 0, 1)
        glVertex3f(-sx, -sy, sz); glVertex3f(sx, -sy, sz)
        glVertex3f(sx, sy, sz); glVertex3f(-sx, sy, sz)
        
        # Back
        glNormal3f(0, 0, -1)
        glVertex3f(-sx, -sy, -sz); glVertex3f(-sx, sy, -sz)
        glVertex3f(sx, sy, -sz); glVertex3f(sx, -sy, -sz)
        
        # Top
        glNormal3f(0, 1, 0)
        glVertex3f(-sx, sy, -sz); glVertex3f(-sx, sy, sz)
        glVertex3f(sx, sy, sz); glVertex3f(sx, sy, -sz)
        
        # Bottom
        glNormal3f(0, -1, 0)
        glVertex3f(-sx, -sy, -sz); glVertex3f(sx, -sy, -sz)
        glVertex3f(sx, -sy, sz); glVertex3f(-sx, -sy, sz)
        
        # Right
        glNormal3f(1, 0, 0)
        glVertex3f(sx, -sy, -sz); glVertex3f(sx, sy, -sz)
        glVertex3f(sx, sy, sz); glVertex3f(sx, -sy, sz)
        
        # Left
        glNormal3f(-1, 0, 0)
        glVertex3f(-sx, -sy, -sz); glVertex3f(-sx, -sy, sz)
        glVertex3f(-sx, sy, sz); glVertex3f(-sx, sy, -sz)
        glEnd()

    def draw_head(self):
        """Draw kepala dengan Visor"""
        glColor3fv(self.colors['head'])
        self.draw_cube(0.5, 0.5, 0.5)
        
        # Visor (Sensor Mata)
        glPushMatrix()
        glColor3fv(self.colors['visor'])
        glTranslatef(0, 0.1, 0.2)
        self.draw_cube(0.4, 0.15, 0.15)
        glPopMatrix()
        
        # Detail kecil di atas kepala (Antena)
        glPushMatrix()
        glColor3fv(self.colors['joint'])
        glTranslatef(0.15, 0.3, 0)
        self.draw_cube(0.05, 0.2, 0.05)
        glPopMatrix()

    def draw_arm(self, side=1):
        """Draw lengan (side: -1=kiri, 1=kanan)"""
        glColor3fv(self.colors['arm'])
        
        # Lengan atas
        glPushMatrix()
        glTranslatef(0, -0.5, 0)
        self.draw_cube(0.2, 1.0, 0.2)
        
        # Lengan bawah
        glTranslatef(0, -0.6, 0)
        self.draw_cube(0.18, 0.8, 0.18)
        glPopMatrix()

    def draw_leg(self, side=1):
        """Draw kaki"""
        glColor3fv(self.colors['leg'])
        
        # Paha
        glPushMatrix()
        glTranslatef(0, -0.6, 0)
        self.draw_cube(0.25, 1.0, 0.25)
        
        # Betis
        glTranslatef(0, -0.7, 0)
        self.draw_cube(0.22, 0.9, 0.22)
        
        # Kaki
        glTranslatef(0, -0.55, 0.1)
        self.draw_cube(0.3, 0.2, 0.5)
        glPopMatrix()

    def draw_details(self):
        """Atribut tambahan: Lampu status dan Logo"""
        # Lampu di bahu (Blinking)
        glPushMatrix()
        t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        if int(t * 2) % 2 == 0:
            glColor3f(1, 0, 0) # Merah menyala
        else:
            glColor3f(0.3, 0, 0) # Merah redup
        
        glTranslatef(0.6, 0.8, 0)
        self.draw_cube(0.1, 0.1, 0.1)
        glTranslatef(-1.2, 0, 0)
        self.draw_cube(0.1, 0.1, 0.1)
        glPopMatrix()

        # Simbol pada Cargo (X)
        glPushMatrix()
        glColor3f(1, 1, 1)
        glTranslatef(0, 0, -0.61)
        self.draw_cube(0.4, 0.1, 0.01)
        glRotatef(90, 0, 0, 1)
        self.draw_cube(0.4, 0.1, 0.01)
        glPopMatrix()

    def draw_robot(self):
        """
        HIERARCHY YANG BENAR:
        1. Global transforms (posisi, rotasi, skala robot)
        2. Body sebagai root
        3. Head sebagai child dari body
        4. Arms sebagai child dari body (dengan rotasi di bahu)
        5. Legs sebagai child dari body (dengan rotasi di pinggul)
        """
        
        # GLOBAL TRANSFORMS
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        
        # --- IMPLEMENTASI ROTASI ---
        # self.rot[1] nilainya diatur di fungsi keyboard (0, 90, 180, 270)
        glRotatef(self.rot[1], 0, 1, 0)  
        
        glScalef(self.scale, self.scale, self.scale)
        
        # BODY (ROOT)
        glPushMatrix()
        glColor3fv(self.colors['body'])
        self.draw_cube(1.0, 1.5, 0.5)
        
        # CARGO BOX (Indeks Fungsi Kurir)
        glPushMatrix()
        glColor3fv(self.colors['cargo'])
        glTranslatef(0, 0, -0.4) # Di punggung
        self.draw_cube(0.8, 1.0, 0.4)
        glPopMatrix()
        
        # HEAD (child of body)
        glPushMatrix()
        glTranslatef(0, 1.1, 0)  # Di atas badan
        self.draw_head()
        glPopMatrix()
        
        # LEFT ARM (child of body) - dengan rotasi di BAHU
        glPushMatrix()
        # Posisi bahu kiri
        glTranslatef(-0.6, 0.5, 0)
        # Rotasi di bahu (pusat rotasi di sini)
        glRotatef(self.arm_angle, 1, 0, 0)
        self.draw_arm(-1)
        glPopMatrix()
        
        # RIGHT ARM (child of body)
        glPushMatrix()
        glTranslatef(0.6, 0.5, 0)
        glRotatef(-self.arm_angle, 1, 0, 0)
        self.draw_arm(1)
        glPopMatrix()
        
        # LEFT LEG (child of body) - dengan rotasi di PINGGUL
        glPushMatrix()
        glTranslatef(-0.25, -0.9, 0)
        glRotatef(self.leg_angle, 1, 0, 0)
        self.draw_leg(-1)
        glPopMatrix()
        
        # RIGHT LEG (child of body)
        glPushMatrix()
        glTranslatef(0.25, -0.9, 0)
        glRotatef(-self.leg_angle, 1, 0, 0)
        self.draw_leg(1)
        glPopMatrix()
        
        self.draw_details()
        
        glPopMatrix()  # Back to global transforms

    def draw_sky(self):
        """Draw a large sky dome/box"""
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glScalef(50, 50, 50)
        
        # Top
        glBegin(GL_QUADS)
        glColor3f(0.4, 0.7, 1.0) # Light blue
        glVertex3f(-1, 1, -1); glVertex3f(-1, 1, 1)
        glVertex3f(1, 1, 1); glVertex3f(1, 1, -1)
        glEnd()
        
        # Sides (Gradient-ish)
        for i in range(4):
            glPushMatrix()
            glRotatef(90 * i, 0, 1, 0)
            glBegin(GL_QUADS)
            glColor3f(0.4, 0.7, 1.0)
            glVertex3f(-1, 1, 1); glVertex3f(1, 1, 1)
            glColor3f(0.7, 0.9, 1.0)
            glVertex3f(1, -0.1, 1); glVertex3f(-1, -0.1, 1)
            glEnd()
            glPopMatrix()
            
        glPopMatrix()
        glEnable(GL_LIGHTING)

    def draw_terrain(self):
        """Draw realistic layout: Road -> Dirt -> Water"""
        # 1. Road (Aspal) - Tengah (Paling tinggi)
        glColor3f(0.15, 0.15, 0.15)
        glBegin(GL_QUADS)
        glVertex3f(-2.5, 0.1, -30); glVertex3f(-2.5, 0.1, 30)
        glVertex3f(2.5, 0.1, 30); glVertex3f(2.5, 0.1, -30)
        glEnd()
        
        # Marka Tengah
        glColor3f(1, 1, 1)
        for z in range(-30, 30, 4):
            glBegin(GL_QUADS)
            glVertex3f(-0.1, 0.11, z); glVertex3f(-0.1, 0.11, z+2)
            glVertex3f(0.1, 0.11, z+2); glVertex3f(0.1, 0.11, z)
            glEnd()

        # 2. Shoulder (Tanah/Cokelat) - Samping Jalan (Sedikit di bawah jalan)
        glColor3f(0.4, 0.3, 0.2)
        glBegin(GL_QUADS)
        # Kiri
        glVertex3f(-6, 0.08, -30); glVertex3f(-6, 0.08, 30)
        glVertex3f(-2.5, 0.08, 30); glVertex3f(-2.5, 0.08, -30)
        # Kanan
        glVertex3f(2.5, 0.08, -30); glVertex3f(2.5, 0.08, 30)
        glVertex3f(6, 0.08, 30); glVertex3f(6, 0.08, -30)
        glEnd()

        # 3. Water (Genangan) - Di luar bahu jalan
        self.draw_water()

    def draw_water(self):
        """Draw animated water beyond dirt shoulders"""
        t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.4, 0.7, 0.7)
        
        size = 40
        res = 20
        step = (size * 2) / res
        
        for i in range(res):
            for j in range(res):
                x = -size + i * step
                z = -size + j * step
                
                # Hanya gambar air jika di luar area tanah (di luar x = -6 sampai 6)
                if x < -6 or x + step > 6:
                    # Ketinggian air tetap di y=0 agar tidak menutupi tanah/jalan
                    y1 = 0.05 * math.sin(t + x * 0.5)
                    y2 = 0.05 * math.sin(t + (x + step) * 0.5)
                    
                    glBegin(GL_QUADS)
                    glVertex3f(x, y1, z)
                    glVertex3f(x, y1, z+step)
                    glVertex3f(x+step, y2, z+step)
                    glVertex3f(x+step, y2, z)
                    glEnd()
        glDisable(GL_BLEND)

    def draw_environment(self):
        """Tiang lampu di bahu jalan (area tanah)"""
        for z in range(-25, 30, 12):
            for side in [-4.5, 4.5]:
                glPushMatrix()
                glTranslatef(side, 0, z)
                # Tiang
                glColor3f(0.3, 0.3, 0.3)
                self.draw_cube(0.15, 4.0, 0.15)
                # Lampu
                glTranslatef(0, 2.0, 0)
                glColor3f(1.0, 1.0, 0.5)
                self.draw_cube(0.3, 0.3, 0.3)
                glPopMatrix()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Camera setup
        cam_x = self.cam_distance * math.sin(math.radians(self.cam_angle))
        cam_y = 3.0
        cam_z = self.cam_distance * math.cos(math.radians(self.cam_angle))
        
        gluLookAt(cam_x, cam_y, cam_z,
                  0, 1, 0,
                  0, 1, 0)
        
        # 0. Draw Sky
        self.draw_sky()

        # 1. Draw Reflection (Robot terbalik)
        glPushMatrix()
        glScalef(1.0, -1.0, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.draw_robot()
        glDisable(GL_BLEND)
        glPopMatrix()

        # 2. Draw Terrain (Road, Dirt, Water) & Environment
        self.draw_terrain()
        self.draw_environment()
        
        # 3. Draw Original Robot
        self.draw_robot()
        
        
        
        glutSwapBuffers()

    def animate(self, value):
        if self.animating:
            self.arm_angle = 30 * math.sin(math.radians(value))
            self.leg_angle = 20 * math.sin(math.radians(value))
        
        glutPostRedisplay()
        glutTimerFunc(16, self.animate, (value + 5) % 360)

    def reshape(self, w, h):
        if h == 0: h = 1
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)

    def keyboard(self, key, x, y):
        key = key.decode()
        
        move_speed = 0.2
        # --- IMPLEMENTASI ROTASI (Logika Arah) ---
        # Mengatur self.rot[1] agar robot menghadap ke arah jalannya
        if key == 'w': 
            self.pos[2] -= move_speed
            self.rot[1] = 180 # Berputar 180 derajat (menghadap ke belakang kamera/maju)
        elif key == 's': 
            self.pos[2] += move_speed
            self.rot[1] = 0   # Hadap depan/kamera (mundur)
        elif key == 'a': 
            self.pos[0] -= move_speed
            self.rot[1] = 270 # Berputar ke kiri
        elif key == 'd': 
            self.pos[0] += move_speed
            self.rot[1] = 90  # Berputar ke kanan
        
        # Rotation
        elif key == 'j': self.rot[1] += 15
        elif key == 'l': self.rot[1] -= 15
        
        # Scale
        elif key == '+': self.scale *= 1.1
        elif key == '-': self.scale *= 0.9
        
        # Arm control
        elif key == '1': self.arm_angle += 15
        elif key == '2': self.arm_angle -= 15
        
        # Animation
        elif key == ' ': self.animating = not self.animating
        
        # Camera
        elif key == 'z': self.cam_angle += 5
        elif key == 'x': self.cam_angle -= 5
        
        # Reset
        elif key == 'r':
            self.pos = [0.0, 2.0, 0.0]
            self.rot = [0.0, 0.0, 0.0]
            self.scale = 0.5
        
        elif key == '\x1b': sys.exit()
        
        glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Aero-Courier Unit X-1")
    
    robot = Robot3D()
    
    glutDisplayFunc(robot.display)
    glutReshapeFunc(robot.reshape)
    glutKeyboardFunc(robot.keyboard)
    glutTimerFunc(0, robot.animate, 0)
    
    robot.init_gl()
    glutMainLoop()

if __name__ == "__main__":
    main()