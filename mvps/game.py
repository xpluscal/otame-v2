import opc
import time
import random

ADDRESS = 'localhost:7890'
MATRIX_SIZE = 8
STRIP_SIZE = 64

def get_neighbors_2d(x, y):
    return [(i % MATRIX_SIZE, j % MATRIX_SIZE) for i in range(x-1, x+2) for j in range(y-1, y+2) if (i, j) != (x, y)]

def get_neighbors_1d(i):
    return [(i-1) % STRIP_SIZE, (i+1) % STRIP_SIZE]

def step_2d(matrix):
    new_matrix = [[0 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            live_neighbors = sum([matrix[x][y] for x, y in get_neighbors_2d(i, j)])
            if matrix[i][j] == 1 and 2 <= live_neighbors <= 3:
                new_matrix[i][j] = 1
            elif matrix[i][j] == 0 and live_neighbors == 3:
                new_matrix[i][j] = 1
    return new_matrix

def step_1d(strip):
    new_strip = [0] * STRIP_SIZE
    for i in range(STRIP_SIZE):
        neighbors = [strip[j] for j in get_neighbors_1d(i)]
        if strip[i] == 0 and sum(neighbors) == 1:
            new_strip[i] = 1
        elif strip[i] == 1 and sum(neighbors) != 1:
            new_strip[i] = 0
    return new_strip

def main():
    client = opc.Client(ADDRESS)

    if not client.can_connect():
        print('Cannot connect to the server at {0}. Exiting.'.format(ADDRESS))
        return

    print('Connected to {0}.'.format(ADDRESS))

    matrix = [[random.choice([0, 1]) for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
    strip = [random.choice([0, 1]) for _ in range(STRIP_SIZE)]

    try:
        while True:
            matrix = step_2d(matrix)
            strip = step_1d(strip)

            pixels_matrix = [(255, 255, 255) if cell else (0, 0, 0) for row in matrix for cell in row]
            pixels_strip = [(255, 255, 255) if led else (0, 0, 0) for led in strip]
            
            client.put_pixels(pixels_matrix + pixels_strip)

            time.sleep(0.5)
    except KeyboardInterrupt:
        print('Animation interrupted. Exiting...')
        pixels = [(0, 0, 0)] * (MATRIX_SIZE * MATRIX_SIZE + STRIP_SIZE)
        client.put_pixels(pixels)

if __name__ == '__main__':
    main()
