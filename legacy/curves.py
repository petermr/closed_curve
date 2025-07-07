import cv2
import numpy as np

# Create a white image
size = 1024
image = np.full((size, size, 3), 255, dtype=np.uint8)

# Draw initial black circle of thickness 2
cv2.circle(image, (512, 512), 500, (0, 0, 0), thickness=2)

# Define color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (224, 224, 224)

# Helper: Check 4-neighbors (up, down, left, right)
def get_neighbors(y, x, h, w):
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w:
            yield ny, nx

# Grow a layer inward from all pixels of target_color
def deposit_layer(image, target_color, new_color, thickness=2):
    h, w, _ = image.shape
    current_layer = set()
    
    # Identify edge pixels of target_color
    for y in range(h):
        for x in range(w):
            if tuple(image[y, x]) == target_color:
                for ny, nx in get_neighbors(y, x, h, w):
                    if tuple(image[ny, nx]) == WHITE:
                        current_layer.add((ny, nx))
    
    # Grow the layer by repeating deposition to achieve desired thickness
    for _ in range(thickness):
        next_layer = set()
        for y, x in current_layer:
            if tuple(image[y, x]) == WHITE:
                image[y, x] = new_color
                for ny, nx in get_neighbors(y, x, h, w):
                    if tuple(image[ny, nx]) == WHITE:
                        next_layer.add((ny, nx))
        current_layer = next_layer

# Repeat (a) and (b) five times
for _ in range(5):
    deposit_layer(image, BLACK, GREY, thickness=2)
    deposit_layer(image, GREY, BLACK, thickness=2)

# Save the final image
cv2.imwrite("cellular_deposition.png", image)

