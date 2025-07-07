import cv2
import numpy as np
import random
from copy import deepcopy

# Create initial white image
size = 1024
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (224, 224, 224)

def create_base_image():
    img = np.full((size, size, 3), 255, dtype=np.uint8)
    cv2.circle(img, (512, 512), 500, BLACK, thickness=2)
    return img

# Use flood fill to find interior (white) pixels
def compute_interior_mask(image):
    mask = np.zeros((size + 2, size + 2), np.uint8)  # OpenCV needs border
    floodfilled = image.copy()
    cv2.floodFill(floodfilled, mask, seedPoint=(512, 512), newVal=(200, 200, 200))
    interior_mask = (floodfilled[:, :, 0] == 200)  # Only look at one channel
    return interior_mask

# Neighborhoods
def get_neighbors(y, x, conn):
    if conn == 4:
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    else:
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dy, dx in deltas:
        yield y + dy, x + dx

# Cellular deposition inside a shape
def deposit_layer(image, target_color, new_color, interior_mask, conn=4, thickness=2, rand=0.01):
    h, w = image.shape[:2]
    current_layer = set()
    
    for y in range(h):
        for x in range(w):
            if tuple(image[y, x]) == target_color:
                for ny, nx in get_neighbors(y, x, conn):
                    if (0 <= ny < h and 0 <= nx < w and
                        interior_mask[ny, nx] and
                        tuple(image[ny, nx]) == WHITE):
                        if random.random() > rand:
                            current_layer.add((ny, nx))

    for _ in range(thickness):
        next_layer = set()
        for y, x in current_layer:
            if tuple(image[y, x]) == WHITE:
                image[y, x] = new_color
                for ny, nx in get_neighbors(y, x, conn):
                    if (0 <= ny < h and 0 <= nx < w and
                        interior_mask[ny, nx] and
                        tuple(image[ny, nx]) == WHITE):
                        if random.random() > rand:
                            next_layer.add((ny, nx))
        current_layer = next_layer

# Run deposition and save result
def run_and_save(conn_type, layers=80):
    img = create_base_image()
    interior = compute_interior_mask(img)
    for _ in range(layers):
        deposit_layer(img, BLACK, GREY, interior, conn=conn_type, thickness=2)
        deposit_layer(img, GREY, BLACK, interior, conn=conn_type, thickness=2)
    filename = f"raster_deposition_conn{conn_type}_{layers}_r.png"
    cv2.imwrite(filename, img)
    print(f"Saved: {filename}")

# Run both 4-connected and 8-connected versions
run_and_save(4)
run_and_save(8)