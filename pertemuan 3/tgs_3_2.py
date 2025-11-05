# garis_bresenham.py
def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x1 >= x0 else -1
    sy = 1 if y1 >= y0 else -1
    if dy <= dx:
        err = dx // 2
        while x != x1:
            points.append((x,y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
        points.append((x1,y1))
    else:
        err = dy // 2
        while y != y1:
            points.append((x,y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
        points.append((x1,y1))
    return points

if __name__ == "__main__":
    pts = bresenham_line(0,0,5,3)
    print("Titik pada garis dari (0,0) ke (5,3):")
    print(pts)
    # visualisasi dalam grid kecil:
    W, H = 6, 4
    grid = [['.' for _ in range(W)] for _ in range(H)]
    for x,y in pts:
        if 0 <= x < W and 0 <= y < H:
            grid[y][x] = 'X'
    print()
    for row in grid:
        print(''.join(row))
