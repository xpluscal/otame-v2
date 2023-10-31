import opc
import time
import random

MATRIX_SIZE = 8
STRIP_SIZE = 64
TOTAL_LEDS = MATRIX_SIZE * MATRIX_SIZE + STRIP_SIZE
client = opc.Client('localhost:7890')

def get_neighbors(matrix, x, y):
    neighbors = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i, j) != (0, 0):
                neighbors.append(matrix[(x+i) % MATRIX_SIZE][(y+j) % MATRIX_SIZE])
    return neighbors

def step_matrix(matrix):
    new_matrix = [[0 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            neighbors = get_neighbors(matrix, i, j)
            alive = matrix[i][j]
            alive_neighbors = sum(neighbors)
            if alive and alive_neighbors not in [2, 3]:
                new_matrix[i][j] = 0
            elif not alive and alive_neighbors == 3:
                new_matrix[i][j] = 1
            else:
                new_matrix[i][j] = alive
    return new_matrix

def hue_to_rgb(hue):
    r = int(255 * (1 - hue))
    b = int(255 * hue)
    return r, 0, b

def main():
    matrix = [[random.choice([0, 1]) for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]

    while True:
        pixels = []
        live_cells = sum([sum(row) for row in matrix])
        hue = (time.time() * 0.05) % 1  # Slowly shift hue over time

        for row in matrix:
            for cell in row:
                r, g, b = hue_to_rgb(hue)
                brightness = cell
                pixels.append((int(r * brightness), int(g * brightness), int(b * brightness)))

        # Update the strip based on activity
        activity_level = live_cells / (MATRIX_SIZE * MATRIX_SIZE)
        strip_brightness = int(255 * activity_level)
        strip_color = hue_to_rgb(hue)
        pixels.extend([strip_color] * STRIP_SIZE)
        
        client.put_pixels(pixels)
        time.sleep(0.2)

        matrix = step_matrix(matrix)

if __name__ == "__main__":
    main()

