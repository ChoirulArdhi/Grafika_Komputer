# representasi_raster.py
def make_grid(width, height, mark=None):
    grid = [['.' for _ in range(width)] for _ in range(height)]
    if mark:
        x,y = mark
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = 'X'
    return grid

def print_grid(grid):
    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    g = make_grid(10, 10, mark=(4,6))
    print("Grid 10x10 dengan X di (4,6):")
    print_grid(g)
