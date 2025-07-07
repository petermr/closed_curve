"""
hand_drawn_polygons.py

Generative art simulating error transmission by repeated human tracing:

- Start with a circular polygon (radius r, line width w).
- Nested polygons (layers) inside previous one, each with
  - a margin to avoid touching or crossing,
  - small random perturbations (error scale) to simulate hand wobble.
- Sliders to control radius, line width, margin, number of layers, and error scale.
- Points per polygon fixed at 500 for smoothness.
- Rendered with Pillow and Tkinter.

Author: ChatGPT + You
"""

import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math
import random

# --- Configuration ---

CANVAS_SIZE = 700
N_POINTS = 500

# --- Geometry Helpers ---

def generate_circle_polygon(n_points, radius):
    """Generate polygon points approximating a circle."""
    return [
        (radius * math.cos(2 * math.pi * i / n_points),
         radius * math.sin(2 * math.pi * i / n_points))
        for i in range(n_points)
    ]

def perturb_polygon(points, margin, error_scale):
    """
    Perturb each point inward by at least margin + random error.
    Ensures no point crosses or touches the previous polygon boundary.
    """
    new_points = []
    for x, y in points:
        dx, dy = -x, -y  # inward vector toward origin
        dist = math.hypot(dx, dy) or 1.0
        nx, ny = dx / dist, dy / dist

        # Push inward by margin plus some random error between 0 and error_scale
        jitter = random.uniform(0, error_scale)
        total_push = margin + jitter

        new_x = x + nx * total_push
        new_y = y + ny * total_push
        new_points.append((new_x, new_y))
    return new_points

def translate_points(points, cx, cy):
    """Translate points by center (cx, cy)."""
    return [(x + cx, y + cy) for x, y in points]

# --- Drawing Function ---

def draw_all_polygons(radius, line_width, margin, n_layers, error_scale):
    """
    Draw all polygons from outer to inner layers on a PIL image.
    """
    cx, cy = CANVAS_SIZE // 2, CANVAS_SIZE // 2
    background = (255, 255, 255)
    line_color = (20, 20, 20)
    img = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), background)
    draw = ImageDraw.Draw(img)

    # Start outer polygon (perimeter)
    polygon = generate_circle_polygon(N_POINTS, radius)
    polygon_layers = [polygon]

    # Draw perimeter polygon (thicker line)
    perimeter_points = translate_points(polygon, cx, cy)
    draw.line(perimeter_points + [perimeter_points[0]], fill=line_color, width=int(line_width))

    # Generate inner polygons sequentially
    prev_polygon = polygon
    for _ in range(n_layers):
        new_polygon = perturb_polygon(prev_polygon, margin, error_scale)

        # Enforce points remain strictly inside prev_polygon with margin
        # (Handled by pushing inward by margin + jitter in perturb_polygon)

        polygon_layers.append(new_polygon)
        prev_polygon = new_polygon

    # Draw inner polygons (thinner lines)
    for poly in polygon_layers[1:]:
        points = translate_points(poly, cx, cy)
        draw.line(points + [points[0]], fill=line_color, width=1)

    return img

# --- Tkinter GUI ---

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Nested Polygons with Error Transmission")

        # Canvas for drawing
        self.canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.canvas.grid(row=0, column=0, columnspan=5)

        # Sliders
        self.radius_slider = self.make_slider("Radius (r)", 50, 300, 250, 0)
        self.line_width_slider = self.make_slider("Line Width (w)", 1, 10, 2, 1)
        self.margin_slider = self.make_slider("Margin", 1, 10, 3, 2)
        self.layers_slider = self.make_slider("Number of Layers", 1, 50, 10, 3)
        self.error_slider = self.make_slider("Error Scale", 0, 5, 1, 4, resolution=0.1)

        # Image handle
        self.img_on_canvas = None

        # Initial draw
        self.update_drawing()

    def make_slider(self, label, minval, maxval, default, col, resolution=1):
        slider = tk.Scale(
            self.root, from_=minval, to=maxval, orient=tk.HORIZONTAL,
            label=label, resolution=resolution, command=lambda e: self.update_drawing()
        )
        slider.set(default)
        slider.grid(row=1, column=col, sticky="ew", padx=5, pady=5)
        return slider

    def update_drawing(self):
        r = self.radius_slider.get()
        w = self.line_width_slider.get()
        margin = self.margin_slider.get()
        n_layers = self.layers_slider.get()
        error = self.error_slider.get()

        img = draw_all_polygons(r, w, margin, n_layers, error)
        self.tk_img = ImageTk.PhotoImage(img)
        if self.img_on_canvas is None:
            self.img_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        else:
            self.canvas.itemconfig(self.img_on_canvas, image=self.tk_img)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
