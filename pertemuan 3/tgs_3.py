# ===========================
# PROGRAM SISTEM KOORDINAT & REPRESENTASI GAMBAR (Tanpa Pandas)
# ===========================
from math import sqrt  # Import fungsi akar kuadrat

# Fungsi jarak dua titik
def distance(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Fungsi menentukan kuadran
def quadrant_cartesian(point):
    x, y = point
    if x == 0 and y == 0:
        return "Origin (0,0)"
    if x == 0:
        return "Di sumbu Y"
    if y == 0:
        return "Di sumbu X"
    if x > 0 and y > 0:
        return "Kuadran I"
    if x < 0 and y > 0:
        return "Kuadran II"
    if x < 0 and y < 0:
        return "Kuadran III"
    if x > 0 and y < 0:
        return "Kuadran IV"

# Fungsi membuat grid layar
def simulate_screen_grid(width, height, mark=None):
    grid = [["." for _ in range(width)] for _ in range(height)]
    if mark is not None:
        x, y = mark
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = "X"
    return grid

# Fungsi ubah grid ke teks
def grid_to_text(grid):
    return "\n".join("".join(row) for row in grid)

# Algoritma Bresenham untuk menggambar garis
def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    if dy <= dx:
        err = dx // 2
        while True:
            points.append((x, y))
            if x == x1 and y == y1:
                break
            x += sx
            err -= dy
            if err < 0:
                y += sy
                err += dx
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
p1 = (2, -3)
p2 = (-4, 5)
dist = distance(p1, p2)
quad_p1 = quadrant_cartesian(p1)

print("=== Soal 1: Jarak dan Kuadran ===")
print(f"Titik p1 = {p1}, p2 = {p2}")
print(f"Jarak = {dist:.4f}")
print(f"p1 berada pada {quad_p1}")

grid_10x5 = simulate_screen_grid(10, 5, mark=(3, 2))
print("\n=== Soal 2: Grid Layar 10x5 ===")
print(grid_to_text(grid_10x5))

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

grid_10x10 = simulate_screen_grid(10, 10, mark=(4, 6))
print("\n=== Grid 10x10 (Titik (4,6)) ===")
print(grid_to_text(grid_10x10))

line_points = bresenham_line(0, 0, 5, 3)
width_line = max(p[0] for p in line_points) + 1
height_line = max(p[1] for p in line_points) + 1
grid_line = simulate_screen_grid(width_line, height_line)
for x, y in line_points:
    grid_line[y][x] = "X"
print("\n=== Garis dari (0,0) ke (5,3) ===")
print("Titik garis:", line_points)
print(grid_to_text(grid_line))
