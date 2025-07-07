import cv2
import numpy as np

# Step 1: Create a white background image
height, width = 400, 400
image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background

# Step 2: Draw anti-aliased black circle with thickness 3
center = (200, 200)
radius = 100
color = (0, 0, 0)  # Black in BGR
thickness = 3

cv2.circle(image, center, radius, color, thickness, lineType=cv2.LINE_AA)

# Step 3: Apply flood fill with red color inside the circle
flood_fill_img = image.copy()
mask = np.zeros((height + 2, width + 2), np.uint8)  # Required mask
cv2.floodFill(flood_fill_img, mask, seedPoint=center, newVal=(0, 0, 255))  # Red color fill

# Step 4: Save the resulting image as PNG
cv2.imwrite("flood_filled_circle.png", flood_fill_img)
