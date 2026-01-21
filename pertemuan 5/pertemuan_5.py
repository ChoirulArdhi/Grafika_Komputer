import turtle
import math

class GraphicsPrimitives:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Praktikum Grafika Komputer - UNU Blitar")
        self.screen.bgcolor("white")
        self.screen.setup(width=1000, height=700)
        
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.hideturtle()
        
        # Warna untuk berbagai primitif (format yang valid untuk Turtle)
        self.colors = {
            'line': '#0000FF',      # Blue dalam format hex
            'circle': '#FF0000',    # Red dalam format hex  
            'polygon': '#00FF00'    # Green dalam format hex
        }
    
    def draw_pixel(self, x, y, color='#000000'):
        """Menggambar satu pixel di posisi (x, y)"""
        self.t.penup()
        self.t.goto(x, y)
        self.t.pendown()
        # Gunakan pensize 3 untuk dot agar lebih terlihat
        self.t.pensize(3)
        self.t.pencolor(color)
        self.t.forward(0)  # Menggambar titik kecil
        self.t.pensize(1)
    
    def draw_line_dda(self, x1, y1, x2, y2, color=None):
        """
        Menggambar garis menggunakan algoritma DDA (Digital Differential Analyzer)
        """
        if color is None:
            color = self.colors['line']
        
        self.t.pencolor(color)
        self.t.penup()
        
        # Hitung dx dan dy
        dx = x2 - x1
        dy = y2 - y1
        
        # Tentukan jumlah steps
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            self.draw_pixel(x1, y1, color)
            return
        
        # Hitung increment untuk x dan y
        x_increment = dx / steps
        y_increment = dy / steps
        
        # Gambar titik pertama
        x, y = x1, y1
        self.draw_pixel(round(x), round(y), color)
        
        # Gambar titik-titik selanjutnya
        for _ in range(steps):
            x += x_increment
            y += y_increment
            self.draw_pixel(round(x), round(y), color)
    
    def draw_circle_midpoint(self, xc, yc, r, color=None):
        """
        Menggambar lingkaran menggunakan algoritma Midpoint Circle
        """
        if color is None:
            color = self.colors['circle']
        
        self.t.pencolor(color)
        self.t.penup()
        
        # Inisialisasi
        x = 0
        y = r
        
        # Decision parameter awal
        d = 1 - r
        
        # Gambar 8 titik simetris pertama
        self._draw_circle_points(xc, yc, x, y, color)
        
        # Iterasi untuk menggambar 1/8 lingkaran
        while x < y:
            x += 1
            
            # Periksa decision parameter
            if d < 0:
                # Pilih pixel E (East)
                d = d + 2 * x + 1
            else:
                # Pilih pixel SE (South East)
                y -= 1
                d = d + 2 * (x - y) + 1
            
            # Gambar 8 titik simetris
            self._draw_circle_points(xc, yc, x, y, color)
    
    def _draw_circle_points(self, xc, yc, x, y, color):
        """Menggambar 8 titik simetris pada lingkaran"""
        points = [
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x)
        ]
        
        for point in points:
            self.draw_pixel(point[0], point[1], color)
    
    def draw_polygon(self, vertices, color=None):
        """
        Menggambar poligon menggunakan algoritma DDA yang sudah dibuat
        """
        if color is None:
            color = self.colors['polygon']
        
        self.t.pencolor(color)
        self.t.penup()
        
        n = len(vertices)
        if n < 3:
            print("Poligon minimal memiliki 3 titik")
            return
        
        # Gambar garis antara setiap titik berurutan
        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]  # Kembali ke titik awal
            self.draw_line_dda(x1, y1, x2, y2, color)
        
        # Tandai titik-titik sudut dengan warna hitam
        for vertex in vertices:
            self.draw_pixel(vertex[0], vertex[1], '#000000')
    
    def draw_grid(self):
        """Menggambar grid koordinat"""
        self.t.pencolor('#CCCCCC')  # Gray light
        self.t.pensize(1)
        
        # Garis vertikal
        for x in range(-400, 401, 50):
            self.t.penup()
            self.t.goto(x, -300)
            self.t.pendown()
            self.t.goto(x, 300)
        
        # Garis horizontal
        for y in range(-300, 301, 50):
            self.t.penup()
            self.t.goto(-400, y)
            self.t.pendown()
            self.t.goto(400, y)
        
        # Sumbu X dan Y
        self.t.pencolor('#000000')
        self.t.pensize(2)
        
        # Sumbu X
        self.t.penup()
        self.t.goto(-400, 0)
        self.t.pendown()
        self.t.goto(400, 0)
        
        # Sumbu Y
        self.t.penup()
        self.t.goto(0, -300)
        self.t.pendown()
        self.t.goto(0, 300)
        
        # Label sumbu
        self.t.penup()
        for x in range(-400, 401, 100):
            self.t.goto(x, -10)
            self.t.write(str(x), align='center', font=('Arial', 8, 'normal'))
        
        for y in range(-300, 301, 100):
            if y != 0:
                self.t.goto(-15, y)
                self.t.write(str(y), align='right', font=('Arial', 8, 'normal'))
    
    def draw_all_primitives(self):
        """Menggambar semua primitif grafis"""
        self.t.clear()
        
        # Gambar grid
        self.draw_grid()
        
        # Judul
        self.t.penup()
        self.t.goto(0, 320)
        self.t.pencolor('#000000')
        self.t.write("Praktikum Grafika Komputer - UNU Blitar", 
                    align='center', font=('Arial', 14, 'bold'))
        
        self.t.goto(0, 300)
        self.t.write("Algoritma DDA (Garis), Midpoint Circle (Lingkaran)", 
                    align='center', font=('Arial', 10, 'normal'))
        
        # Contoh 1: Garis dengan DDA
        self.t.penup()
        self.t.goto(-350, 250)
        self.t.pencolor(self.colors['line'])
        self.t.write("Garis (Algoritma DDA):", font=('Arial', 10, 'bold'))
        
        # Gambar beberapa garis
        self.draw_line_dda(-300, 200, -150, 200, self.colors['line'])  # Garis horizontal
        self.draw_line_dda(-300, 150, -150, 250, self.colors['line'])  # Garis miring
        self.draw_line_dda(-250, 100, -250, 200, self.colors['line'])  # Garis vertikal
        
        # Contoh 2: Lingkaran dengan Midpoint
        self.t.penup()
        self.t.goto(-50, 250)
        self.t.pencolor(self.colors['circle'])
        self.t.write("Lingkaran (Midpoint Circle):", font=('Arial', 10, 'bold'))
        
        # Gambar beberapa lingkaran
        self.draw_circle_midpoint(0, 175, 50, self.colors['circle'])
        self.draw_circle_midpoint(0, 100, 30, self.colors['circle'])
        
        # Contoh 3: Poligon dengan DDA
        self.t.penup()
        self.t.goto(250, 250)
        self.t.pencolor(self.colors['polygon'])
        self.t.write("Poligon (Menggunakan DDA):", font=('Arial', 10, 'bold'))
        
        # Segitiga
        triangle = [(200, 200), (300, 200), (250, 150)]
        self.draw_polygon(triangle, self.colors['polygon'])
        
        self.t.penup()
        self.t.goto(250, 190)
        self.t.pencolor('#000000')
        self.t.write("Segitiga", align='center', font=('Arial', 8, 'normal'))
        
        # Segi lima
        pentagon = []
        for i in range(5):
            angle = 2 * math.pi * i / 5
            x = 250 + 40 * math.cos(angle - math.pi/2)
            y = 100 + 40 * math.sin(angle - math.pi/2)
            pentagon.append((x, y))
        self.draw_polygon(pentagon, self.colors['polygon'])
        
        self.t.penup()
        self.t.goto(250, 70)
        self.t.pencolor('#000000')
        self.t.write("Segi Lima", align='center', font=('Arial', 8, 'normal'))
        
        # Segi enam
        hexagon = []
        for i in range(6):
            angle = 2 * math.pi * i / 6
            x = 250 + 40 * math.cos(angle)
            y = 10 + 40 * math.sin(angle)
            hexagon.append((x, y))
        self.draw_polygon(hexagon, self.colors['polygon'])
        
        self.t.penup()
        self.t.goto(250, -20)
        self.t.pencolor('#000000')
        self.t.write("Segi Enam", align='center', font=('Arial', 8, 'normal'))
        
        # Contoh 4: Kombinasi untuk membuat bentuk kompleks
        self.t.penup()
        self.t.goto(-250, -50)
        self.t.pencolor('#800080')  # Purple
        self.t.write("Bentuk Kompleks (Rumah):", font=('Arial', 10, 'bold'))
        
        # Gambar rumah sederhana
        # Dinding (persegi panjang)
        house_base = [(-350, -100), (-250, -100), (-250, -200), (-350, -200)]
        self.draw_polygon(house_base, '#8B4513')  # Brown
        
        # Atap (segitiga)
        roof = [(-360, -100), (-240, -100), (-300, -50)]
        self.draw_polygon(roof, '#FF0000')  # Red
        
        # Pintu
        door = [(-310, -200), (-290, -200), (-290, -140), (-310, -140)]
        self.draw_polygon(door, '#0000FF')  # Blue
        
        # Jendela (lingkaran)
        self.draw_circle_midpoint(-300, -120, 10, '#ADD8E6')  # Light blue
        
        # Informasi penulis
        self.t.penup()
        self.t.goto(0, -280)
        self.t.pencolor('#000000')
        self.t.write("Program Studi Ilmu Komputer - Universitas Nahdlatul Ulama Blitar", 
                    align='center', font=('Arial', 10, 'normal'))
        
        self.t.goto(0, -300)
        self.t.write("Praktikum Grafika Komputer - Menggambar Garis, Lingkaran, dan Poligon", 
                    align='center', font=('Arial', 9, 'normal'))
        
        # Tunggu sebelum keluar
        turtle.done()

def main():
    """Fungsi utama program"""
    print("=" * 60)
    print("PRAKTIKUM GRAFIKA KOMPUTER")
    print("Program Studi Ilmu Komputer")
    print("Universitas Nahdlatul Ulama Blitar")
    print("=" * 60)
    print("\nMenggambar Garis, Lingkaran, dan Poligon")
    print("Menggunakan algoritma DDA dan Midpoint Circle")
    print("\nTekan tombol X pada window untuk keluar...")
    
    # Buat objek grafis
    graphics = GraphicsPrimitives()
    
    # Gambar semua primitif
    graphics.draw_all_primitives()

if __name__ == "__main__":
    main()