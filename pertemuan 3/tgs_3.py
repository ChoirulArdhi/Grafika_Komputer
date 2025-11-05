# ===========================
# PROGRAM SISTEM KOORDINAT & REPRESENTASI GAMBAR (Tanpa Pandas)
# ===========================

from math import sqrt  # Import fungsi sqrt untuk menghitung akar kuadrat

# Fungsi untuk menghitung jarak Euclidean antara dua titik p1 dan p2
def distance(p1, p2):
    (x1, y1) = p1  # Ambil koordinat x dan y dari titik pertama
    (x2, y2) = p2  # Ambil koordinat x dan y dari titik kedua
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)  # Rumus jarak Euclidean

# Fungsi untuk menentukan kuadran dari sebuah titik dalam sistem koordinat Cartesian
def quadrant_cartesian(point):
    x, y = point  # Ambil koordinat x dan y
    if x == 0 and y == 0:  # Titik berada di origin
        return "Origin (0,0)"
    if x == 0:  # Titik berada di sumbu Y
        return "Di sumbu Y"
    if y == 0:  # Titik berada di sumbu X
        return "Di sumbu X"
    if x > 0 and y > 0:  # Kuadran I
        return "Kuadran I"
    if x < 0 and y > 0:  # Kuadran II
        return "Kuadran II"
    if x < 0 and y < 0:  # Kuadran III
        return "Kuadran III"
    if x > 0 and y < 0:  # Kuadran IV
        return "Kuadran IV"

# Fungsi untuk membuat grid layar dengan tanda titik tertentu
def simulate_screen_grid(width, height, mark=None):
    grid = [["." for _ in range(width)] for _ in range(height)]  # Buat grid dengan '.' sebagai default
    if mark is not None:  # Jika ada titik yang ingin ditandai
        x, y = mark
        if 0 <= x < width and 0 <= y < height:  # Pastikan titik berada di dalam grid
            grid[y][x] = "X"  # Tandai titik dengan 'X'
    return grid

# Fungsi untuk mengubah grid menjadi string teks agar bisa dicetak
def grid_to_text(grid):
    return "\n".join("".join(row) for row in grid)  # Gabungkan setiap baris dan kolom menjadi teks

# Algoritma Bresenham untuk menggambar garis antara dua titik
def bresenham_line(x0, y0, x1, y1):
    points = []  # List untuk menyimpan titik-titik garis
    dx = abs(x1 - x0)  # Selisih absolut koordinat X
    dy = abs(y1 - y0)  # Selisih absolut koordinat Y
    x, y = x0, y0  # Mulai dari titik awal
    sx = 1 if x0 < x1 else -1  # Arah pergerakan X
    sy = 1 if y0 < y1 else -1  # Arah pergerakan Y

    # Jika kemiringan garis <= 1
    if dy <= dx:
        err = dx // 2  # Inisialisasi error
        while True:
            points.append((x, y))  # Tambahkan titik saat ini ke list
            if x == x1 and y == y1:  # Jika sudah sampai titik akhir, hentikan
                break
            x += sx  # Tambah koordinat X sesuai arah
            err -= dy  # Kurangi error dengan dy
            if err < 0:  # Jika error negatif, naikkan Y dan perbaiki error
                y += sy
                err += dx
    # Jika kemiringan garis > 1
    else:
        err = dy // 2
        while True:
            points.append((x, y))
            if x == x1 and y == y1:
                break
            y += sy
            err -= dx
            if err < 0:
                x += sx
                err += dy
    return points

# ====== Bagian Utama ======
p1 = (2, -3)  # Titik pertama
p2 = (-4, 5)  # Titik kedua

# Hitung jarak antara p1 dan p2
dist = distance(p1, p2)

# Tentukan kuadran p1
quad_p1 = quadrant_cartesian(p1)

# Cetak hasil jarak dan kuadran
print("=== Soal 1: Jarak dan Kuadran ===")
print(f"Titik p1 = {p1}, p2 = {p2}")
print(f"Jarak = {dist:.4f}")
print(f"p1 berada pada {quad_p1}")

# Simulasikan grid 10x5 dengan titik (3,2) ditandai
grid_10x5 = simulate_screen_grid(10, 5, mark=(3, 2))
print("\n=== Soal 2: Grid Layar 10x5 ===")
print(grid_to_text(grid_10x5))

# Tabel perbandingan format raster vs vektor
print("\n=== Tabel Perbandingan Raster vs Vektor ===")
print("Aspek                 | Raster                      | Vektor")
print("----------------------|-----------------------------|-------------------------------")
print("Elemen dasar          | Piksel (titik warna)        | Titik, garis, kurva")
print("Resolusi              | Tetap (mis. 1920x1080)      | Tidak tergantung ukuran")
print("Saat diperbesar       | Pecah / blur                | Tetap tajam")
print("Jenis file umum       | JPG, PNG, BMP, GIF          | SVG, EPS, AI, PDF")
print("Kelebihan             | Realistis, cocok foto        | Fleksibel, ringan, skalabel")
print("Kelemahan             | File besar, tak fleksibel    | Kurang cocok untuk foto")
print("Contoh                | Foto, screenshot             | Logo, ikon, teks")

# Simulasikan grid 10x10 dengan titik (4,6) ditandai
grid_10x10 = simulate_screen_grid(10, 10, mark=(4, 6))
print("\n=== Grid 10x10 (Titik (4,6)) ===")
print(grid_to_text(grid_10x10))

# Gambar garis dari (0,0) ke (5,3) menggunakan algoritma Bresenham
line_points = bresenham_line(0, 0, 5, 3)

# Tentukan ukuran grid berdasarkan titik-titik garis
width_line = max(p[0] for p in line_points) + 1
height_line = max(p[1] for p in line_points) + 1

# Buat grid untuk garis
grid_line = simulate_screen_grid(width_line, height_line)
for x, y in line_points:
    grid_line[y][x] = "X"  # Tandai titik-titik garis

# Cetak hasil garis
print("\n=== Garis dari (0,0) ke (5,3) ===")
print("Titik garis:", line_points)
print(grid_to_text(grid_line))
