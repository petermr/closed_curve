"""
hand_drawn_polygons.py

Generative art simulating error transmission by repeated human tracing:

- Start with a circular polygon (radius r, line width w).
- Nested polygons (layers) inside previous one, each with
  - a margin to avoid touching or crossing,
  - small random perturbations (error scale) to simulate hand wobble.
- Number of points decreases for inner polygons so average
  point spacing stays roughly constant.
- Sliders to control radius, line width, margin, number of layers, error scale,
  and initial points per polygon.
- Rendered with Pillow and Tkinter.

Author: ChatGPT + You
"""

import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math
import random

CANVAS_SIZE = 700

def generate_circle_polygon(n_points, radius):
    return [
        (radius * math.cos(2 * math.pi * i / n_points),
         radius * math.sin(2 * math.pi * i / n_points))
        for i in range(n_points)
    ]

def polygon_perimeter(points):
    peri = 0
    n = len(points)
    for i in range(n):
        x0, y0 = points[i]
        x1, y1 = points[(i+1) % n]
        peri += math.hypot(x1 - x0, y1 - y0)
    return peri

def resample_polygon(points, n_new):
    """
    Resample polygon to have n_new points spaced evenly along perimeter.
    Uses linear interpolation of points along polygon edges.
    """
    n_old = len(points)
    # Compute cumulative distances
    dists = [0]
    for i in range(n_old):
        x0, y0 = points[i]
        x1, y1 = points[(i+1) % n_old]
        dists.append(dists[-1] + math.hypot(x1 - x0, y1 - y0))
    perimeter = dists[-1]

    # Target spacing
    spacing = perimeter / n_new
    new_points = []
    # Walk along perimeter, adding points every 'spacing'
    current_dist = 0
    seg_index = 0
    while len(new_points) < n_new:
        # Find segment containing current_dist
        while seg_index < n_old and dists[seg_index+1] < current_dist:
            seg_index += 1
        if seg_index == n_old:
            seg_index = 0
        # Interpolate on segment seg_index
        seg_start = dists[seg_index]
        seg_end = dists[seg_index+1]
        t = (current_dist - seg_start) / (seg_end - seg_start) if seg_end > seg_start else 0
        x0, y0 = points[seg_index]
        x1, y1 = points[(seg_index+1) % n_old]
        x = x0 + t * (x1 - x0)
        y = y0 + t * (y1 - y0)
        new_points.append((x, y))
        current_dist += spacing
    return new_points

def perturb_polygon(points, margin, error_scale):
    new_points = []
    for x, y in points:
        dx, dy = -x, -y  # inward vector
        dist = math.hypot(dx, dy) or 1.0
        nx, ny = dx / dist, dy / dist
        jitter = random.uniform(0, error_scale)
        total_push = margin + jitter
        new_x = x + nx * total_push
        new_y = y + ny * total_push
        new_points.append((new_x, new_y))
    return new_points

def translate_points(points, cx, cy):
    return [(x + cx, y + cy) for x, y in points]

def draw_all_polygons(radius, line_width, margin, n_layers, error_scale, n_points_init):
    cx, cy = CANVAS_SIZE // 2, CANVAS_SIZE // 2
    background = (255, 255, 255)
    line_color = (20, 20, 20)
    img = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), background)
    draw = ImageDraw.Draw(img)

    # Outer polygon
    polygon = generate_circle_polygon(n_points_init, radius)
    polygon_layers = [polygon]

    # Draw perimeter polygon thicker
    perimeter_points = translate_points(polygon, cx, cy)
    draw.line(perimeter_points + [perimeter_points[0]], fill=line_color, width=int(line_width))

    # Compute target point spacing from outer polygon
    outer_perimeter = polygon_perimeter(polygon)
    target_spacing = outer_perimeter / n_points_init

    prev_polygon = polygon
    prev_points = n_points_init

    for _ in range(n_layers):
        # Perturb inward first
        perturbed = perturb_polygon(prev_polygon, margin, error_scale)
        # Compute perimeter of perturbed polygon
        peri = polygon_perimeter(perturbed)
        # Compute new number of points maintaining approx spacing
        n_new = max(3, round(peri / target_spacing))
        # Resample polygon to n_new points
        resampled = resample_polygon(perturbed, n_new)
        polygon_layers.append(resampled)
        prev_polygon = resampled
        prev_points = n_new

    # Draw inner polygons thinner
    for poly in polygon_layers[1:]:
        pts = translate_points(poly, cx, cy)
        draw.line(pts + [pts[0]], fill=line_color, width=1)

    return img

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Nested Polygons with Error Transmission")

        self.canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.canvas.grid(row=0, column=0, columnspan=6)

        self.radius_slider = self.make_slider("Radius (r)", 50, 300, 250, 0)
        self.line_width_slider = self.make_slider("Line Width (w)", 1, 10, 2, 1)
        self.margin_slider = self.make_slider("Margin", 1, 10, 3, 2)
        self.layers_slider = self.make_slider("Number of Layers", 1, 50, 10, 3)
        self.error_slider = self.make_slider("Error Scale", 0, 5, 1, 4, resolution=0.1)
        self.points_slider = self.make_slider("Initial Points", 50, 500, 500, 5)

        self.img_on_canvas = None
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
        n_points_init = self.points_slider.get()

        img = draw_all_polygons(r, w, margin, n_layers, error, n_points_init)
        self.tk_img = ImageTk.PhotoImage(img)
        if self.img_on_canvas is None:
            self.img_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        else:
            self.canvas.itemconfig(self.img_on_canvas, image=self.tk_img)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
